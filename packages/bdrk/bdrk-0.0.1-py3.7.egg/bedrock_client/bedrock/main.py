# isort:skip_file
import pkg_resources

for entry_point in pkg_resources.iter_entry_points("console_scripts", "bedrock"):  # noqa
    entry_point.require()  # noqa

import logging
import os
from pathlib import Path

import click

import docker
from docker.types import Mount
from spanlib.common.exceptions import ConfigInvalidError
from spanlib.infrastructure.span_config.config_objects.command import (
    ShellCommand,
    SparkSubmitCommand,
)
from spanlib.utils.command import generate_command, make_spark_run_steps
from spanlib.utils.paths import training

from .config import BedrockConfig, get_bedrock_config

CONTAINER_AUTH_FILE = "/credentials/application_default_credentials.json"
HADOOP_NAMESPACE_PREFIX = "spark.hadoop.google.cloud.auth.service.account"


@click.group()
def main():
    logging.basicConfig(level=logging.INFO)


def get_gcloud_keyfile_path() -> str:
    """Getting gcloud keyfile path

    Reading from a bunch of environment variables to find a keyfile path
    Precedence is taken from
    https://www.terraform.io/docs/providers/google/provider_reference.html

    :return: path to auth_file
    :rtype: str
    """

    env_vars = [
        "GOOGLE_CREDENTIALS",
        "GOOGLE_CLOUD_KEYFILE_JSON",
        "GCLOUD_KEYFILE_JSON",
        "GOOGLE_APPLICATION_CREDENTIALS",
    ]
    for var in env_vars:
        auth_file_path = os.getenv(var, None)
        if auth_file_path:
            break
    if not auth_file_path:
        logging.warning(
            "No env var found specifying credentials, "
            "fallback to user's Google Application Default Credential."
        )
        auth_file_path = str(
            Path.joinpath(Path.home(), ".config/gcloud/application_default_credentials.json")
        )

    assert os.path.isfile(
        auth_file_path
    ), f"Google credential file at {auth_file_path} does not exist"
    return auth_file_path


@main.command()
@click.argument("target_dir")
@click.option(
    "--mock-feature-store",
    help="Use an in memory mock instead of the real feature store",
    is_flag=True,
)
def train(target_dir: str, mock_feature_store: bool):
    gcloud_keyfile = get_gcloud_keyfile_path()
    docker_client = docker.from_env()
    config = get_bedrock_config(os.path.join(target_dir, "bedrock.hcl"))
    if config.train_config is None:
        raise ConfigInvalidError(resp_details="Train stanza is missing from config file")
    command = make_training_command_from_config(config)
    container = docker_client.containers.run(
        image=config.train_config.image,
        mounts=[
            Mount(source=target_dir, target=training.APP_VOL_MOUNT_PATH, type="bind"),
            Mount(source=target_dir, target=training.ARTEFACT_VOL_MOUNT_PATH, type="bind"),
            Mount(source=gcloud_keyfile, target=CONTAINER_AUTH_FILE, type="bind"),
        ],
        environment=[
            f"GOOGLE_APPLICATION_CREDENTIALS={CONTAINER_AUTH_FILE}",
            f"FEATURE_STORE_MOCK={1 if mock_feature_store else 0}",
        ],
        # FIXME: [BDRK-340] using host network. Should be fixed when we have feature store as a
        # service
        network_mode="host",
        entrypoint=["/bin/bash", "-x", "-c"],
        command=[command],
        working_dir=training.APP_VOL_MOUNT_PATH,
        detach=True,
        remove=True,
    )
    for line in container.logs(stream=True):
        logging.info(line.strip().decode("utf-8"))


def make_training_command_from_config(config: BedrockConfig):
    if config.train_config is None:
        raise ConfigInvalidError(resp_details="Train stanza is missing from config file")
    config_command = config.train_config.script_commands[0]
    if isinstance(config_command, ShellCommand):
        command = generate_command([config.train_config.install, config_command.content])
    elif isinstance(config_command, SparkSubmitCommand):
        command = generate_command(
            make_spark_run_steps(
                spark_system_config={
                    HADOOP_NAMESPACE_PREFIX + ".enable": "true",
                    HADOOP_NAMESPACE_PREFIX + ".json.keyfile": CONTAINER_AUTH_FILE,
                },
                spark_system_settings={},
                install_script=config.train_config.install,
                command=config_command,
            )
        )
    else:
        raise ConfigInvalidError
    return command


@main.command()
@click.argument("target_dir")
@click.option(
    "--mock-feature-store",
    help="Use an in memory mock instead of the real feature store",
    is_flag=True,
)
def deploy(target_dir: str, mock_feature_store: bool):
    gcloud_keyfile = get_gcloud_keyfile_path()
    docker_client = docker.from_env()
    config = get_bedrock_config(os.path.join(target_dir, "bedrock.hcl"))
    if config.serve_config is None:
        raise ConfigInvalidError(resp_details="Serve stanza is missing from config file")
    command = generate_command([config.serve_config.install, config.serve_config.script_commands])
    container = docker_client.containers.run(
        image=config.serve_config.image,
        mounts=[
            Mount(source=target_dir, target=training.APP_VOL_MOUNT_PATH, type="bind"),
            Mount(source=target_dir, target=training.ARTEFACT_VOL_MOUNT_PATH, type="bind"),
            Mount(source=gcloud_keyfile, target=CONTAINER_AUTH_FILE, type="bind"),
        ],
        environment=[
            f"GOOGLE_APPLICATION_CREDENTIALS={CONTAINER_AUTH_FILE}",
            f"GRPC_VERBOSITY=INFO",
            f"FEATURE_STORE_MOCK={1 if mock_feature_store else 0}",
        ],
        # FIXME: [BDRK-340] using host network. Should be fixed when we have feature store as a
        # service
        network_mode="host",
        entrypoint=["/bin/bash", "-x", "-c"],
        command=[command],
        working_dir=training.APP_VOL_MOUNT_PATH,
        detach=True,
        remove=True,
    )
    for line in container.logs(stream=True):
        logging.info(line.strip().decode("utf-8"))
