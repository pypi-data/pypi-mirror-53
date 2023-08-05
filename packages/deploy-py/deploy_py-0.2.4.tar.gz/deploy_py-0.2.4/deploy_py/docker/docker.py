from typing import Generator

import docker
from docker.errors import ImageNotFound
from docker.models.images import Image

from . import exceptions
from ..logging import get_logger


DEFAULT_BASIC_TAG_TEMPLATE = "{app}:{version}"
DEFAULT_REPO_TAG_TEMPLATE = "{repo}/{app}:{version}"


class Client:
    ImageNotFound = exceptions.ImageNotFoundError

    def __init__(self, verbosity: int = 0):
        self.logger = get_logger("deploy.docker.Client", verbosity)
        self.docker = docker.from_env()

    @staticmethod
    def get_tag(template: str = DEFAULT_REPO_TAG_TEMPLATE, **kwargs):
        return template.format(**kwargs)

    def build_image(self, build_ctx: str, tag: str, push: bool = False, **kwargs) -> (Image, Generator):
        self.logger.info(f"building image with tag {tag}")
        image, logs = self.docker.images.build(
            path=build_ctx,
            tag=tag,
            buildargs=kwargs.get("buildargs", None),
            cache_from=kwargs.get("cache_from", None),
            container_limits=kwargs.get("container_limits", None),
            custom_context=kwargs.get("custom_context", False),
            dockerfile=kwargs.get("dockerfile", "Dockerfile"),
            encoding=kwargs.get("encoding", "gzip"),
            extra_hosts=kwargs.get("extra_hosts", None),
            forcerm=kwargs.get("forcerm", True),
            isolation=kwargs.get("isolation", None),
            labels=kwargs.get("labels", None),
            network_mode=kwargs.get("network_mode", None),
            nocache=kwargs.get("nocache", False),
            platform=kwargs.get("platform", None),
            pull=kwargs.get("pull", True),
            quiet=kwargs.get("quiet", True),
            rm=kwargs.get("rm", True),
            shmsize=kwargs.get("shmsize", 64),
            squash=kwargs.get("squash", True),
            target=kwargs.get("target", None),
            timeout=kwargs.get("timeout", 30),
            use_config_proxy=kwargs.get("use_config_proxy", False),
        )

        if push:
            self.logger.info(f"pushing image with tag {tag}")
            self.push_image(tag)

        return image, logs

    def push_image(self, tag: str, stream: bool = False, decode: bool = False):
        self.docker.images.push(tag, stream=stream, decode=decode)

    def delete_image(self, image: str, force: bool = False, noprune: bool = False):
        self.logger.info(f"deleting image: {image}")
        try:
            self.docker.images.remove(image, force=force, noprune=noprune)
        except ImageNotFound:
            raise exceptions.ImageNotFoundError(image)

