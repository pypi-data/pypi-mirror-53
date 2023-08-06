from zookeeper import registry, cli, build_train, HParams, data, Preprocessing
from click.testing import CliRunner
import click
from unittest import mock
from os import path
import tensorflow as tf
import tensorflow_datasets as tfds


class ImageClassification(Preprocessing):
    @property
    def kwargs(self):
        return {
            "input_shape": self.features["image"].shape,
            "num_classes": self.features["label"].num_classes,
        }

    def inputs(self, data):
        return tf.cast(data["image"], tf.float32)

    def outputs(self, data):
        return tf.one_hot(data["label"], self.features["label"].num_classes)


@registry.register_preprocess("mnist")
class default(ImageClassification):
    def inputs(self, data):
        return super().inputs(data) / 255


@registry.register_preprocess("mnist")
class raw(ImageClassification):
    decoders = {"image": tfds.decode.SkipDecoding()}

    def inputs(self, data):
        return tf.cast(tf.image.decode_image(data["image"]), tf.float32)


@registry.register_model
def foo(hparams, **kwargs):
    return "foo-model"


@registry.register_hparams(foo)
class bar(HParams):
    baz = 3
    baz_overwrite = 0


@cli.command()
@click.option("--custom-opt", type=str, required=True)
@build_train()
def train(build_model, dataset, hparams, output_dir, custom_opt):
    assert isinstance(hparams, HParams)
    assert isinstance(dataset, data.Dataset)
    assert isinstance(output_dir, str)
    assert isinstance(custom_opt, str)

    model = build_model(hparams, **dataset.preprocessing.kwargs)
    assert model == "foo-model"
    assert dataset.dataset_name == "mnist"
    assert dataset.train_examples == 60000
    assert hparams.baz == 3
    assert hparams.baz_overwrite == 42
    assert custom_opt == "passed"
    print("TESTS PASSED")


@cli.command()
@build_train()
def train_val(build_model, dataset, hparams, output_dir):
    assert isinstance(hparams, HParams)
    assert isinstance(dataset, data.Dataset)
    assert isinstance(output_dir, str)

    model = build_model(hparams, **dataset.preprocessing.kwargs)
    assert model == "foo-model"
    assert dataset.dataset_name == "mnist"
    assert dataset.train_examples == 54000
    assert hparams.baz == 3
    print("TESTS PASSED")


@cli.command()
@build_train()
def train_fail(build_model, dataset, hparams, output_dir):
    pass


runner = CliRunner(mix_stderr=False)


def test_cli(tmp_path):
    result = runner.invoke(cli, ["prepare", "mnist"])
    assert result.exit_code == 0

    result = runner.invoke(
        cli,
        [
            "train",
            "foo",
            "--hparams-set",
            "bar",
            "--dataset",
            "mnist",
            "--hparams",
            "baz_overwrite=42",
            "--custom-opt",
            "passed",
        ],
    )
    assert result.exit_code == 0
    assert result.output.splitlines()[-1] == "TESTS PASSED"

    result = runner.invoke(
        cli,
        [
            "train-val",
            "foo",
            "--hparams-set",
            "bar",
            "--dataset",
            "mnist",
            "--validationset",
            "--preprocess-fn",
            "raw",
        ],
    )
    assert result.exit_code == 0
    assert result.output.splitlines()[-1] == "TESTS PASSED"


def test_cli_wrong_data():
    result = runner.invoke(
        cli, ["train-fail", "foo", "--hparams-set", "bar", "--dataset", "raise-error"]
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, registry.DatasetNotFoundError)


def test_cli_wrong_prepro():
    result = runner.invoke(
        cli,
        [
            "train-fail",
            "foo",
            "--hparams-set",
            "bar",
            "--dataset",
            "mnist",
            "--preprocess-fn",
            "raise-error",
        ],
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, registry.PreprocessNotFoundError)


def test_cli_wrong_model():
    result = runner.invoke(
        cli, ["train-fail", "raise-error", "--hparams-set", "bar", "--dataset", "mnist"]
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, registry.ModelNotFoundError)


def test_cli_wrong_hparams():
    result = runner.invoke(
        cli, ["train-fail", "foo", "--hparams-set", "raise-error", "--dataset", "mnist"]
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, registry.HParamsNotFoundError)


@mock.patch("os.system")
def test_tensorboard(os_system):
    result = runner.invoke(cli, ["tensorboard", "foo", "--dataset", "bar"])
    assert result.exit_code == 0
    logdir = path.expanduser("~/zookeeper-logs/bar/foo")
    os_system.assert_called_once_with(f"tensorboard --logdir={logdir}")


@mock.patch("os.system")
def test_tensorboard_logdir(os_system):
    result = runner.invoke(cli, ["tensorboard", "--logdir", "foo"])
    assert result.exit_code == 0
    os_system.assert_called_once_with(f"tensorboard --logdir=foo")


if __name__ == "__main__":
    cli()
