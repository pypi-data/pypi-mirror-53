from setuptools import setup, find_packages
setup(
        name='Bussator',
        version='0.1',
        description="A webmention receiver and publisher, written in Python (WSGI application)",
        author='Alberto Mardegan',
        author_email='mardy@users.sourceforge.net',
        packages=find_packages(),
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU Affero General Public License v3',
            'Programming Language :: Python :: 3',
            'Topic :: Internet',
            'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
            'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        ],
        install_requires=[
            'beautifulsoup4',
            'html5lib',
            'mf2py',
            'python-dateutil',
            'requests',
        ],
)

