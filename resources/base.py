import logging

logger = logging.getLogger(__name__)

import boto3
from abc import ABC, abstractmethod

class AWSResource(ABC):
    def __init__(self, resource_type):
        self.resource_type = resource_type
        self.client = boto3.client(resource_type)

    @abstractmethod
    def scan(self):
        pass

    @abstractmethod
    def report(self):
        pass

    @abstractmethod
    def take_action(self):
        pass

class AWSResourceCLI(ABC):
    @abstractmethod
    def configure(self):
        pass

class Plugin(ABC):
    cli_cls = None

    def initialize(self, subparsers):
        logger.debug(f"Initializing plugin {self.cli_cls.__name__}")
        self.cli_cls.configure(subparsers)
