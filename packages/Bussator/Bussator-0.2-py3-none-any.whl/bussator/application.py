# -*- coding: utf-8 -*-

import bussator.globals

from urllib.parse import parse_qs, urlsplit

import logging

from bs4 import BeautifulSoup
import requests
import mf2py

import dateutil.parser


logging.basicConfig(level=logging.DEBUG)


class PostData:

    def __init__(self, mf):
        self.mf = mf
        items = mf.get('items', [])
        item = items[0].get('properties', {}) if items else {}
        authors = item.get('author', [])
        author = authors[0].get('properties', {}) if authors else {}
        self.author_name = author.get('name', [None])[0]
        self.author_email = author.get('email', [None])[0]
        self.author_photo = author.get('photo', [None])[0]
        self.author_url = author.get('url', [None])[0]
        self.post_url = item.get('url', [None])[0]
        self.post_title = item.get('name', [''])[0]
        date = item.get('published', [None])[0]
        if not date:
            date = item.get('updated', [None])[0]
        self.post_date = dateutil.parser.parse(date) if date else None
        content = item.get('content', [None])[0]
        if content:
            self.post_content_html = content.get('html')
            self.post_content_text = content.get('value')
        else:
            self.post_content_html = ''
            self.post_content_text = ''
        self.is_like = len(item.get('like-of', [])) > 0

        # Some heuristics to fill the blanks
        if not self.author_email or not self.author_url:
            mes = mf.get('rels', {}).get('me', [])
            for me in mes:
                if (not self.author_email) and me.startswith('mailto:'):
                    self.author_email = me[7:]
                if (not self.author_url) and me.startswith('http://'):
                    self.author_url = me

    def __str__(self):
        return ('Name: {author_name}\n'
                'Photo: {author_photo}\n'
                'Homepage: {author_url}\n'
                'E-mail: {author_email}\n'
                'Title: {post_title}\n'
                'Date: {post_date}\n').format(**self.__dict__)


class Request:

    user_agent = bussator.globals.user_agent

    def __init__(self, fields, start_response):
        logging.debug('Input: {}'.format(fields))

        def extract_url(fields, name):
            value = fields.get(name)
            if not value:
                return None
            url = value[0]
            parts = urlsplit(url)
            return url if parts[0].startswith('http') else None

        self.target = extract_url(fields, 'target')
        self.source = extract_url(fields, 'source')
        logging.debug(self.__dict__)
        self.start_response = start_response

    def is_valid(self):
        return self.target and self.source

    def make_error(self, status):
        self.start_response(status, [])
        return []

    def parse_source(self):
        req = requests.get(self.source, headers={
            'User-Agent': self.user_agent,
        })
        soup = BeautifulSoup(req.content, 'html5lib')

        # check for target link in source post
        links = soup.find_all('a')
        urls = [l.get('href') for l in links]
        if self.target not in urls:
            logging.debug('Target link not found ({})'.format(self.target))
            return False

        logging.debug('link found')

        mf = mf2py.parse(doc=soup, url=self.source)
        import json
        logging.debug(json.dumps(mf, indent=2))

        self.post_data = PostData(mf)
        logging.debug(self.post_data)
        return True

    def process(self):
        if not self.is_valid():
            return self.make_error('400 Bad Request')

        response_headers = [
                ('Content-type', 'text/plain; charset=utf-8')
        ]
        status = '202 Accepted'
        self.start_response(status, response_headers)

        response_text = ('Processing webmention request:\n'
                         '  target: {target}\n'
                         '  source: {source}\n').format(**self.__dict__)
        return bytes(response_text, 'utf-8')


class App:

    def __init__(self, config_file):
        self.config_file = config_file
        self.enabled_plugins = []
        self.plugin_config = {}
        self.active_plugins = []

    def __call__(self, environ, start_response):
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 512))
        except (ValueError):
            request_body_size = 512
        body = environ['wsgi.input'].read(request_body_size)
        if isinstance(body, bytes):
            body = body.decode('utf-8')

        fields = parse_qs(body)
        req = Request(fields, start_response)
        yield req.process()

        if not req.parse_source():
            return  # Nothing to do

        self.load_config()

        from bussator.plugin import PluginLoader
        pl = PluginLoader()
        for plugin_name in self.enabled_plugins:
            plugin = pl.load(plugin_name, self.plugin_config[plugin_name])
            self.active_plugins.append(plugin)
            plugin.process_webmention(req.source, req.target, req.post_data)

    def load_config(self):
        if self.enabled_plugins:
            return

        import configparser
        config = configparser.ConfigParser(default_section='General')
        config.read(self.config_file)

        enabled_plugins = config.get('General', 'enabled_plugins').split(',')
        self.enabled_plugins = [p.strip() for p in enabled_plugins]
        for plugin_name in self.enabled_plugins:
            try:
                self.plugin_config[plugin_name] = \
                        dict(config.items(plugin_name))
            except configparser.NoSectionError:
                logging.warning('No section for plugin {}'.format(plugin_name))
                self.plugin_config[plugin_name] = {}
