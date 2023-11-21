import logging

logger = logging.getLogger(__name__)

import importlib
import pkgutil
import resources
import argparse


# Maintains the list of loaded plugins
plugin_registry = {}

def initialize_plugins(resource_subparser: argparse.ArgumentParser):
    """Initializes all the plugins in the registry.
    
    This function is called after the plugin manager has loaded all the plugins
    
    Args:
        subparsers (argparse.ArgumentParser): The subparser to pass to plugins
    
    Returns:
        _type_: _description_
    
    Raises:
        AttributeError: If the plugin does not have a `register_plugin` method.
    """

    command_map = {}

    logger.debug("Initializing all plugins in registry")
    for _, plugin_cls in plugin_registry.items():
        plugin = plugin_cls(resource_subparser)
        command_map[plugin.cli.command_name] = plugin.cli

    return command_map

def load_plugins():
    """Imports all the plugins within the resources package.
    
    This function is called when the plugin manager is initialized.
    It imports all the plugins within the resources package.
    
    Args:
        None
    
    Returns:
        _type_: _description_
    
    Raises:
        ImportError: If the plugin could not be imported.
        AttributeError: If the plugin does not have a `register_plugin` method.
    """
    logger.debug("Loading plugins from resources package")

    package = resources
    prefix = package.__name__ + "."

    for loader, name, is_pkg in pkgutil.iter_modules(package.__path__, prefix):
        if is_pkg:
            continue

        logger.debug(f"Loading plugin {name}")
        importlib.import_module(name)

def register_plugin(cls):
    """A decorator for registering plugin classes when they are imported.

    Returns:
        resources.base.Plugin: A plugin class that is decorated
    """
    logger.debug(f"Adding plugin {cls.__name__} to plugin resgistry")
    
    # Add the plugin to the registry
    plugin_registry[cls.__name__] = cls
    return cls
