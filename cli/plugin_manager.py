import logging

logger = logging.getLogger(__name__)

import importlib
import pkgutil
import resources  # Import your resources package

# Maintains the list of loaded plugins
plugin_registry = {}

def initialize_plugins(subparsers):
    logger.debug("Initializing all plugins in registry")
    for _, plugin_cls in plugin_registry.items():
        plugin = plugin_cls()
        plugin.initialize(subparsers)

def load_plugins():
    package = resources
    prefix = package.__name__ + "."

    for loader, name, is_pkg in pkgutil.iter_modules(package.__path__, prefix):
        if not is_pkg:
            logger.debug("Loading plugin %s", name)
            # Import the plugin module
            importlib.import_module(name)

def register_plugin(cls):
    """ A decorator for registering plugin classes. """
    logger.debug(f"Adding plugin {cls.__name__} to plugin resgistry")
    
    # Add the plugin to the registry
    plugin_registry[cls.__name__] = cls
    return cls
