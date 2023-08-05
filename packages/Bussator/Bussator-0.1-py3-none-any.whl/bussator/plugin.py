# -*- coding: utf-8 -*-

import os.path

class Plugin:

    def __init__(self, config):
        self.config = config

    def process_webmention(self, source, target, post_data):
        pass


class PluginLoader:

    def __init__(self):
        pass

    def load(self, plugin_name, config):
        import importlib, inspect
        module = importlib.import_module('bussator.plugins.' + plugin_name)

        plugin_class = None
        for member_name, member in inspect.getmembers(module):
            if member_name != 'Plugin' and \
                    inspect.isclass(member) and \
                    issubclass(member, Plugin):
                plugin_class = member
                break

        return plugin_class(config) if plugin_class else None
