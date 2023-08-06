# -*- coding: utf-8 -*-

from bussator.plugin import Plugin


class DummyPlugin(Plugin):
    """ Dummy plugin, for testing only """

    def __init__(self, config):
        super().__init__(config)
        self.process_webmention_calls = []

    def process_webmention(self, source, target, post_data):
        cleaned_data = post_data.__dict__
        if 'mf' in cleaned_data:
            del cleaned_data['mf']
            cleaned_data['has_mf'] = True
        else:
            cleaned_data['has_mf'] = False

        obj = {
                'source': source,
                'target': target,
                'post_data': cleaned_data,
        }
        self.process_webmention_calls.append(obj)
