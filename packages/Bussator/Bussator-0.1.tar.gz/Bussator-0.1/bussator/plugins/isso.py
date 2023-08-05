# -*- coding: utf-8 -*-

from bussator.plugin import Plugin

import logging

import requests
from urllib.parse import urlsplit

class IssoPublisher(Plugin):

    def __init__(self, config):
        super().__init__(config)
        self.publish_uri = self.config.get('server_url') + '/new'
        self.headers = {
                'User-Agent': self.config.get('user_agent', 'Bussator'),
        }
        self.max_words = int(self.config.get('max_words', -1))
        self.redirection_message = self.config.get('redirection_message',
                'I wrote a reply [in my blog]({post_url})')
        self.full_message = self.config.get('full_message',
                '{post_content_html}\n\n[Source link]({post_url})')

    def process_webmention(self, source, target, post_data):
        logging.debug('process_webmention {source}, target is {target}'.format(source=source,target=target))

        if post_data.post_content_html and \
            (self.max_words < 0
                    or len(post_data.post_content_text.split()) < self.max_words):
                text = self.full_message.format(**post_data.__dict__)
        else:
            text = self.redirection_message.format(**post_data.__dict__)


        body = {
                'text': text,
                'author': post_data.author_name,
                'website': post_data.author_url,
                'email': post_data.author_email,
                'title': post_data.post_title,
        }

        uri = urlsplit(target)[2]
        params = {
                'uri': uri,
        }
        req = requests.post(self.publish_uri,
                headers=self.headers,
                params=params,
                json=body)
        logging.debug('Requesting {0}, body: {1}'.format(req, req.request.body))
        logging.debug('Request reply: {}'.format(req.content))
