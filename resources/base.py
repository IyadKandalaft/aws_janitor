import logging

logger = logging.getLogger(__name__)

import boto3
from abc import ABC, abstractmethod

class AWSResource(ABC):
    @property
    def client(self):
        return self._client
    
    @client.setter
    def client(self, client):
        self._client = client

    @property
    def resource_type(self):
        return self._resource_type
    
    @resource_type.setter
    def resource_type(self, resource_type):
        self._resource_type = resource_type

    def __init__(self, resource_type):
        self.resource_type = resource_type
        self.client = boto3.client(resource_type)

    @abstractmethod
    def scan(self):
        pass

    @abstractmethod
    def clean(self):
        pass

class AWSResourceCLI(ABC):
    @property
    def command_name(self):
        return self._command_name
    
    @command_name.setter
    def command_name(self, command_name):
        self._command_name = command_name

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, resource):
        self._resource = resource

    @property
    def resource_parser(self):
        return self._resource_parser
    
    @resource_parser.setter
    def resource_parser(self, resource_parser):
        self._resource_parser = resource_parser

    @property
    def action_parser(self):
        return self._action_parser

    @action_parser.setter
    def action_parser(self, action_parser):
        self._action_parser = action_parser
    

    def __init__(self, resource_subparsers):
        logger.debug(f"Initializing {self.__class__.__name__}")
        self.resource_parser = resource_subparsers.add_parser(self.command_name)
        self.action_parser = self.resource_parser.add_subparsers(dest="action")
        self.action_parser.add_parser("scan")
        self.action_parser.add_parser("clean")

        self.configure_cli()

    @abstractmethod
    def configure_cli(self):
        pass

    @abstractmethod
    def configure_args(self, args):
        pass

    def invoke(self, args):
        self.configure_args(args)
        if hasattr(args, 'action'):
            if args.action == "clean":
                self.resource.clean()
            elif args.action == "scan":
                self.resource.scan()

class Plugin(ABC):
    def __init__(self, resource_subparsers):
        logger.debug(f"Initializing plugin {self.__class__.__name__}")
   
    @property
    def cli(self):
        return self._cli
    
    @cli.setter
    def cli(self, cli):
        self._cli = cli
