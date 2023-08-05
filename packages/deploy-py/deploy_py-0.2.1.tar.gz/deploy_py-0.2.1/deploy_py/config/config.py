import json
from typing import ForwardRef

import yaml
from jinja2 import Template

from . import exceptions


class DockerConfig:
    def __init__(self, repo, creds="docker-credential-gcr", context="./", file="./Dockerfile"):
        self.creds = creds
        self.context = context
        self.file = file
        self.repo = repo


class HelmConfig:
    def __init__(self, kind: str = "repo", chart_dir: str = "./deploy/{app}",
                 dest_dir: str = "./deploy", save: bool = True, repo: str = "test", args: dict = None):
        if args is None:
            args = {}

        self.kind = kind
        self.chart_dir = chart_dir
        self.dest_dir = dest_dir
        self.save = save
        self.repo = repo
        self.args = args


class Defaults:
    def __init__(self, project, context, docker, helm):
        self.project = project
        self.context = context
        self.docker = DockerConfig(**docker)
        self.helm = HelmConfig(**helm)


class Deployment:
    def __init__(self, name: str, app: str, defaults: Defaults, project=None, context=None, docker=None, helm=None):
        if docker is None:
            docker = {}
        if helm is None:
            helm = {}

        self.name = name
        self.project = project or defaults.project
        self.context = context or defaults.context
        self.docker = DockerConfig(
            repo=docker.get("repo", defaults.docker.repo),
            creds=docker.get("creds", defaults.docker.creds),
            context=docker.get("context", defaults.docker.context),
            file=docker.get("file", defaults.docker.file),
        )
        self.helm = HelmConfig(
            kind=helm.get("kind", defaults.helm.kind),
            chart_dir=helm.get("chart_dir", defaults.helm.chart_dir),
            dest_dir=helm.get("dest_dir", defaults.helm.dest_dir),
            save=helm.get("save", defaults.helm.save),
            repo=helm.get("repo", defaults.helm.repo),
            args=helm.get("args", defaults.helm.args),
        )


class Config:
    def __init__(self, app: str, deployments: dict, defaults: dict = None):
        self.app = app
        self.defaults = Defaults(**defaults)
        self.deployments = {name: Deployment(name, app, self.defaults, **dep) for name, dep in deployments.items()}

    @classmethod
    def from_file(cls, path: str = ".deploy.yaml") -> ForwardRef("Config"):
        with open(path, "r") as conf_file:
            data = yaml.load(conf_file, Loader=yaml.SafeLoader)
        return Config(
            data["app"],
            deployments=data["deployments"],
            defaults=data.get("defaults", {})
        )

    def get_deployment(self, name: str) -> Deployment:
        try:
            return self.deployments[name]
        except KeyError:
            raise exceptions.DeploymentNotFoundError(name)
