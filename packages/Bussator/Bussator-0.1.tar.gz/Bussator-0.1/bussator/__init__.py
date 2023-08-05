# -*- coding: utf-8 -*-

from bussator import application

def make_app(config_file):
    app = application.App(config_file)
    return app
