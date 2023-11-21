import logging

logger = logging.getLogger(__name__)

from cli.plugin_manager import register_plugin
from .base import AWSResource, AWSResourceCLI, Plugin
from datetime import datetime, timedelta
import re

class RDS(AWSResource):
    def __init__(self):
        super().__init__('rds')

    @property
    def connections(self):
        return self._connections

    @connections.setter
    def connections(self, value):
        self._connections = value
    
    @property
    def since(self):
        return self._since
    
    @since.setter
    def since(self, value):
        self._since = value

    def scan(self):
        now = datetime.now()
        cutoff_date = now - self.since

        #TODO

        return None

    def clean(self):
        pass

class RDSCLIConfig(AWSResourceCLI):
    def __init__(self, resource_subparsers):
        self.command_name = 'rds'
        self.resource = RDS()

        super().__init__(resource_subparsers)

    def configure_cli(self):
        self.resource_parser.add_argument('--connections', type=int, default=1, required=True, help='Number of database connections to consider the database active')
        self.resource_parser.add_argument('--since', type=self._parse_relative_date, default=30, required=True, help='Relative days or months to check')

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
            return datetime.timedelta(days=value * 30)  # Approximation for a month
        else:
            raise argparse.ArgumentTypeError("Invalid date unit. Use 'd' for days or 'm' for months.")

    def configure_args(self, args):
        self.resource.since = args.since
        self.resource.connections = args.connections

@register_plugin
class RDSPlugin(Plugin):
    def __init__(self, resource_subparsers):
        super().__init__(resource_subparsers)
        self.cli = RDSCLIConfig(resource_subparsers)
