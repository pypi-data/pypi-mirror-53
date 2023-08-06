# -*- coding: utf-8 -*-

import pkg_resources

dist = pkg_resources.get_distribution("bussator")

version = dist.version
user_agent = 'Bussator - version {0}'.format(version)
