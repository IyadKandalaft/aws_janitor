import logging

logger = logging.getLogger(__name__)

import importlib
import pkgutil
import resources  # Import your resources package

# Maintains the list of loaded plugins
plugin_registry = {}

def initialize_plugins(subparsers):
    logger.debug("Initializing plugins")
    for _, plugin_cls in plugin_registry.items():
        print(plugin_cls)
        plugin = plugin_cls()
        plugin.register(subparsers)

def load_plugins():
    package = resources
    prefix = package.__name__ + "."

    for loader, name, is_pkg in pkgutil.iter_modules(package.__path__, prefix):
        if not is_pkg:
            importlib.import_module(name)

def register_plugin(cls):
    """ A decorator for registering plugin classes. """
    logger.debug("Registering plugin %s", cls.__name__)
    
    # Add the plugin to the registry
    plugin_registry[cls.__name__] = cls
    return cls