# -*- coding: utf-8 -*-
from typing import Generator

from bumpv import BumpClient

from . import docker
from . import helm
from .config import Config, HelmConfig
from .logging import get_logger


class DeployClient:
    def __init__(self, conf_path: str = ".deploy.yaml", allow_dirty: bool = False, verbosity: int = 0):
        self.logger = get_logger(level=verbosity)
        self.config = Config.from_file(conf_path)
        self.bumpv = BumpClient(allow_dirty=allow_dirty)
        self.docker = docker.Client(verbosity=verbosity)
        self.helm = helm.Client(verbosity=verbosity)

    def deploy(self, release_type: str, target: str, do_cleanup: bool = True, dry_run: bool = False):
        deployment = self.config.get_deployment(target)

        if do_cleanup:
            previous_tag = self.docker.get_tag(
                repo=deployment.docker.repo,
                app=self.config.app,
                version=self.bumpv.current_version.serialize()
            )
            self.cleanup(target, previous_tag)

        if release_type == "rebuild":
            version = self.bumpv.current_version
        else:
            version = self.bumpv.bump(release_type, dry_run)

        docker_tag = self.docker.get_tag(repo=deployment.docker.repo, app=self.config.app, version=version.serialize())
        image, _ = self.build_image(deployment.docker.context, docker_tag, quiet=False)
        self.package(
            self.config.app,
            version.serialize(),
            config=deployment.helm,
            dry_run=dry_run
        )
        self.helm.update_release(
            self.config.app,
            version.serialize(),
            deployment.helm.chart_dir,
            helm.ChartKinds.directory,
            deployment.context
        )
        self.update_helm_repo(deployment.helm.chart_dir, deployment.helm.repo)

    def build_image(self, build_ctx: str, tag: str, push: bool = True, **kwargs) -> (docker.Image, Generator):
        return self.docker.build_image(build_ctx, tag, push, **kwargs)

    def cleanup(self, target: str, previous_tag: str):
        deployment = self.config.get_deployment(target)
        self.helm.delete_chart(deployment.helm.repo, self.config.app, self.bumpv.current_version.serialize())

        self.docker.delete_image(previous_tag)

    def package(self, app: str, version: str, chart_dir: str = None,
                dest_dir: str = None, repo: str = None, config: HelmConfig = None, dry_run=False) -> str:
        if config is not None:
            chart_dir = config.chart_dir
            dest_dir = config.dest_dir
            repo = config.repo

        chart_path = self.helm.package(
            app,
            version,
            chart_dir,
            dest_dir
        )

        if not dry_run:
            self.helm.upload(repo, chart_path)
        return chart_path

    def update_helm_repo(self, chart_dir: str, repo_name: str):
        self.helm.update_index(chart_dir, repo_name)
