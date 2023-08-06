# Bussator

[![pipeline status](https://gitlab.com/mardy/bussator/badges/master/pipeline.svg)](https://gitlab.com/mardy/bussator/commits/master)
[![coverage report](https://gitlab.com/mardy/bussator/badges/master/coverage.svg)](https://gitlab.com/mardy/bussator/commits/master)

Bussator is a WSGI application which implements a
[webmention](https://www.w3.org/TR/webmention/) receiver. Webmentions can then
be published through dedicated plugins; currently, a plugin for publishing
webmentions as [Isso](https://posativ.org/isso/) comments exists.

I've written Bussator to handle webmentions in [my static
blog](http://www.mardy.it), written with the [Nikola](https://getnikola.com)
site generator and having the comments handled by Isso. It's all served by a
cheap shared hosting solution, so you shouldn't need any special hosting in
order to run a similar setup.


## Installation

Bussator can be installed via [PIP](https://pypi.org/project/Bussator/):

    pip install bussator

will install the module with all its dependencies. If you plan to stay up on
the bleeding edge, you can also install the latest master branch:

    pip install -e git+https://gitlab.com/mardy/bussator.git#egg=bussator

When you wish to update it, just run `git pull` from within the directory where
the code was checked out (if using virtualenv, this should be
`<virtualenv>/src/bussator`).


## Deployment

Once the Bussator module has been installed and can be found by your python
interpreter, you need to instruct your webserver to use it. Given that the
module provides a `make_app()` method which creates the WSGI application, its
deployment with `mod_wsgi` or `mod_fastcgi` should be relatively easy. If you
have been able to run Bussator on other types of deployment, you are warmly
invited to share your success story with us by [opening an
issue](https://gitlab.com/mardy/bussator/issues/new).

- `mod_wsgi`: I haven't tested this, but the [instructions from the isso
  project](https://github.com/posativ/isso/blob/master/docs/docs/extras/deployment.rst#mod-wsgi)
  should work for Bussator too, with the obvious adaptations.

- `mod_fastcgi`: install flup (`pip install flup-py3`), then create a
  `bussator.fcgi` file in your server's `cgi-bin/` directory (don't forget to
  make it executable!):

```
#!/usr/bin/env python
#: uncomment if you're using a virtualenv
#import sys
#sys.path.insert(0, '<your-virtualenv>/lib/python3.6/site-packages')
import os
from bussator import make_app
from flup.server.fcgi import WSGIServer

application = make_app('<path-to-your-config>/config.ini')
WSGIServer(application).run()
```


## Configuration

Bussator won't work unless a configuration file has been created. The
configuration file is a `.ini` style document; it's recommended that you copy
the [template](config.ini) from this repository and modify it as needed. The
comments in the file should be explanative enough.


## Integration with Twitter, Flickr and other online services

The excellent [Brid.gy](https://brid.gy) service can be used to forward
comments and likes from your social networks into Bussator (and hence into your
blog). Just tell it the exact URL of your Bussator endpoint and it should all
work.
