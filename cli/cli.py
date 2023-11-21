import logging

logger = logging.getLogger(__name__)

import argparse
import importlib

from .plugin_manager import load_plugins, initialize_plugins

def setup_logging(debug=False):
    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    # Create a parser for global arguments
    global_parser = argparse.ArgumentParser(description="AWS Janitor CLI", add_help=False)
    global_parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')

    global_args, remaining_argv = global_parser.parse_known_args()
    setup_logging(global_args.debug)

    logger.debug("Initializing main parser")
    parser = argparse.ArgumentParser(description="AWS Janitor CLI")
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    resource_subparsers = parser.add_subparsers(dest="resource", help="Resource types")
    
    load_plugins()
    command_map = initialize_plugins(resource_subparsers)

    args = parser.parse_args(remaining_argv)

    # Execute the plugin based on the command used
    if hasattr(args, 'resource') and args.resource in command_map:
        cli = command_map[args.resource]
        cli.invoke(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
