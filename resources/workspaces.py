import logging

logger = logging.getLogger(__name__)

from cli.plugin_manager import register_plugin
from .base import AWSResource, AWSResourceCLI, Plugin
from datetime import datetime, timedelta
import re

class Workspaces(AWSResource):
    def __init__(self):
        super().__init__('workspaces')

    @property
    def last_used(self):
        return self._last_used

    @last_used.setter
    def last_used(self, value):
        self._last_used = value

    def scan(self):
        now = datetime.now()
        cutoff_date = now - self.last_used

        workspaces = self.client.describe_workspaces()

        return workspaces

    def clean(self):
        pass

class WorkspacesCLIConfig(AWSResourceCLI):
    def __init__(self, resource_subparsers):       
        self.command_name = 'workspaces'
        self.resource = Workspaces()

        super().__init__(resource_subparsers)

    def configure_cli(self):
        self.resource_parser.add_argument('--last-used', type=self._parse_relative_date, default='30d', help='Days or months since last used',)

    def _parse_relative_date(self, arg_value):
        # Regular expression to match the pattern
        match = re.match(r"(\d+)([dm])", arg_value)
        if not match:
            raise argparse.ArgumentTypeError("Invalid format for date. Use '10d' for 10 days or '1m' for 1 month.")

        value, unit = match.groups()
        value = int(value)

        if unit == 'd':
            return timedelta(days=value)
        elif unit == 'm':
            return timedelta(days=value * 30)  # Approximation for a month
        else:
            raise argparse.ArgumentTypeError("Invalid date unit. Use 'd' for days or 'm' for months.")

    def configure_args(self, args):
        self.resource.last_used = args.last_used

@register_plugin
class WorkspacesPlugin(Plugin):
    def __init__(self, resource_subparsers):
        super().__init__(resource_subparsers)
        self.cli = WorkspacesCLIConfig(resource_subparsers)
