# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['remotedata']
install_requires = \
['cmdy', 'requests']

entry_points = \
{'console_scripts': ['remotedata-hash = remotedata:console']}

setup_kwargs = {
    'name': 'remotedata',
    'version': '0.1.0',
    'description': 'Accessing and caching remote data.',
    'long_description': "# remotedata\n\nAccessing and caching remote data for python.\nMay be used in the cases that:\n1. The remote data is being updated frequently\n2. You don't want to sync all the data but just per your request\n3. You want to cache the data locally for some time\n4. Especially, when the files are used for testing\n\n## Installation\n\n```shell\npip install remotedata\n```\n\n## Usage\n\nCurrently, data from `github` and `dropbox` are supported\n\n### Github\n\n```python\nfrom remotedata import remotedata\nrdata = remotedata(dict(\n\tsource = 'github',\n\tcachedir = '/tmp/cached/',\n\t## if branch is not master: pwwang/remotedata/branch\n\trepos  = 'pwwang/remotedata',\n\t## optional, default is first part of repos\n\t# user = 'pwwang',\n\t## github token, in case you have > 60 requests per hours to github API\n\t# token = 'xxx',\n))\nreadme = rdata.get('README.md')\n# README.md is downloaded to /tmp/cache/github/pwwang.remotedata@master/README.md\n# Now you can use it as a local file\n\n# readme will be cached, we don't have to download it again,\n# until it has been changed remotely.\n\n# remove cached file\nrdata.remove('README.md')\n# clear up all caches\nrdata.clear()\n```\n\n### Dropbox\n\n```python\nfrom remotedata import remotedata\nrdata = remotedata(dict(\n\tsource = 'dropbox',\n\tcachedir = '/tmp/cached/',\n\tdropbox_token = 'xxx'\n))\nrdata.get('/somefile') # or\nrdata.get('somefile')\n```",
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'url': 'https://github.com/pwwang/remotedata',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
