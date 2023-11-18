import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

import argparse
import importlib

from .plugin_manager import load_plugins, initialize_plugins

def main():
    logger.debug("Initializing main parser")
    parser = argparse.ArgumentParser(description="AWS Janitor CLI")
    subparsers = parser.add_subparsers(dest="resource", help="Resource types")

    load_plugins()
    initialize_plugins(subparsers)

    args = parser.parse_args()
    # Handle the arguments and invoke the appropriate plugin logic

if __name__ == "__main__":
    main()
