# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['contxt',
 'contxt.auth',
 'contxt.cli',
 'contxt.models',
 'contxt.services',
 'contxt.utils']

package_data = \
{'': ['*']}

install_requires = \
['argcomplete>=1.10,<2.0',
 'auth0-python>=3.9,<4.0',
 'pyjwt>=1.7,<2.0',
 'python-dateutil>=2.8,<3.0',
 'pytz>=2019.2,<2020.0',
 'requests>=2.22,<3.0',
 'tabulate>=0.8.3,<0.9.0',
 'tqdm>=4.36,<5.0',
 'tzlocal>=2.0,<3.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.6.0,<0.7.0'],
 'server': ['python-jose-cryptodome>=1.3,<2.0']}

entry_points = \
{'console_scripts': ['contxt = contxt.__main__:main']}

setup_kwargs = {
    'name': 'contxt-sdk',
    'version': '1.0.0b8',
    'description': 'Contxt SDK from ndustrial.io',
    'long_description': '# Contxt Python SDK\n[![pypi version](https://pypip.in/v/contxt-sdk/badge.png)](https://pypi.org/project/contxt-sdk/)\n[![wercker status](https://app.wercker.com/status/960b7b32c2d94d12a3a5c89ca17e13ba/s/ "wercker status")](https://app.wercker.com/project/byKey/960b7b32c2d94d12a3a5c89ca17e13ba)\n\n## Dependencies\nThis project **requires** Python 3.6+.\n\n## Installation \nTo install `contxt-sdk`, just use pip:\n\n```\n$ pip install contxt-sdk\n```\n\nThis also installs a command line interface (cli) available via `contxt`, as long as your active python environment has installed the package. To see the list of supported commands, run the following:\n\n```\n$ contxt -h\n```\n\n Additionally, there is support for command line tab completion via [argcomplete](https://github.com/kislyuk/argcomplete). To active, run the following and refresh your bash environment:\n\n```\n$ activate-global-python-argcomplete\n```\n\n## Contributing\nPlease refer to the [release guide](docs/release.md).\n\n## Command Line Interface\n\n### Getting Started\nIn order to access any Contxt API, we first need to login. To do so, run the following:\n\n```\n$ contxt auth login\n```\n\nIt will prompt you for your username and password, which is the same login you use for your Contxt applications.\n\n### Available Commands\n\n#### Auth\n```\n$ contxt auth -h\nusage: contxt auth [-h] {login,logout} ...\n\noptional arguments:\n  -h, --help      show this help message and exit\n\nsubcommands:\n  {login,logout}\n    login         Login to contxt\n    logout        Logout of contxt\n```\n\n#### IOT\n\n```\n$ contxt iot -h \nusage: contxt iot [-h] {groupings,feeds,fields,unprovisioned,field-data} ...\n\noptional arguments:\n  -h, --help            show this help message and exit\n\nsubcommands:\n  {groupings,feeds,fields,unprovisioned,field-data}\n    groupings           Get groupings\n    feeds               Get feeds\n    fields              Get fields\n    unprovisioned       Unprovisioned fields\n    field-data          Get field data\n```\n\n#### EMS\n```\n$ contxt ems -h \nusage: contxt ems [-h]\n                  {util-spend,util-usage,util-spend-metrics,util-usage-metrics}\n                  ...\n\noptional arguments:\n  -h, --help            show this help message and exit\n\nsubcommands:\n  {util-spend,util-usage,util-spend-metrics,util-usage-metrics}\n    util-spend          Utility spend\n    util-usage          Utility usage\n    util-spend-metrics  Utility spend metrics\n    util-usage-metrics  Utility usage metrics\n```\n\n#### Assets\n```\n$ contxt assets -h \nusage: contxt assets [-h]\n                     {facilities,types,assets,attr,attr-vals,metrics,metric-vals}\n                     ...\n\noptional arguments:\n  -h, --help            show this help message and exit\n\nsubcommands:\n  {facilities,types,assets,attr,attr-vals,metrics,metric-vals}\n    facilities          Get facility assets\n    types               Get asset types\n    assets              Get assets\n    attr                Get asset attributes\n    attr-vals           Get asset attribute values\n    metrics             Get asset metrics\n    metric-vals         Get asset metric values\n\n```\n\n#### Contxt\n```\n$ contxt contxt -h\nusage: contxt contxt [-h] {orgs,mk-org,users,add-user} ...\n\noptional arguments:\n  -h, --help            show this help message and exit\n\nsubcommands:\n  {orgs,mk-org,users,add-user}\n    orgs                Get organizations\n    mk-org              Create organization\n    users               Get users\n    add-user            Add user to an organization\n```\n\n#### Bus\n```\n$ contxt bus -h\nusage: contxt bus [-h] {channels} ...\n\noptional arguments:\n  -h, --help  show this help message and exit\n\nsubcommands:\n  {channels}\n    channels  Get channels\n```\n\n## Workers \n\n### Machine Authentication\nSince the CLI interface is just a wrapper around different functions in the SDK, users can also leverage these\nfunctions in their own code. Within Contxt we have a concept of a machine user that is identified by a unique\nclient_id / client_secret pair (instead of a user/pass combination like regular users). When writing code that\nwill eventually go to production that will need to call other APIs (this is obviously quite common), your service\nwill automatically be given a unique client_id / client_secret pair within Contxt. When you create this service,\nyou can use these credentials in your local development environment as well.\n\n### Base Worker Class\nIn order to make development easier, we have a Worker Base Class we provide in the SDK to abstract away the\nnuance of the authentication process (if you\'re curious, [here](https://contxt.readme.io/docs/machine-to-machine-authentication) is a link to the documentation on this process, in\ncase you\'re really REALLY bored and looking for some "light" reading). In the root path of this SDK, you\'ll\nsee an "examples" directory that contains a few example of how to do various tasks. In the file "sample_worker.py",\nyou will see a very simple example of how to implement the BaseWorker class.\n\nIn this sample worker file, you will see just a few lines of code, to get started. It is vitally important, however,\nto set your environment variables for CLIENT_ID and CLIENT_SECRET. We provide these in the environment for 2\nreasons:\n- You never want to put your client_id / client_secret pair in your code to be committed anywhere. This is a\nmajor no-no as these should be regarded the same as user credentials\n- Contxt will automatically set these in the environment upon deployment to a Contxt environment (staging, prod, etc.)\nso setting this up in development will make it seamless upon deployment\n\nLooking at this [example](examples/worker.py), you can see that we\'re implementing the `BaseWorker` class. Behind\nthe scenes, that class is doing all the work around getting tokens, refreshing tokens, etc. so you don\'t have to. In\nthis example, we\'re going to make a call to the Contxt Facilities (Assets) Service to get a list of facilities available\nto this worker (machine user). To do so, we must instantiate the Facilities class and pass in `self.auth`.\n\nNext, in the `do_work` method, it\'s just making a simple\ncall to `get_facilities`. You can iterate over this list, or just print it to\nthe console (like we\'ve done here).\n\nFrom here, you can continue to code up your application logic to perform whatever tasks you need using all the SDK\nfunctions available to you.\n\n## CLI Examples\n\n#### Exporting IOT Data\n\nYou can export field data from the IOT service with the following command:\n\n```\n$ contxt iot field-data -h\nusage: contxt iot field-data [-h] [-e END_DATE] [-p]\n                             grouping_id start_date {0,60,900,3600}\n```\n\nFor example:\n```\n$ contxt iot field-data "09d26434-7b5b-448f-911c-2deb5e9a78ce" "2019-02-01" 60\n```\n\nThis command will create the directory `export_<grouping_slug>_<current_time>` with csv files of the associated records each field within the grouping and within the specified time range. There is also a `meta.json` file which contains specific information about the export like row counts, field ids, and units.\n',
    'author': 'ndustrial.io',
    'author_email': 'dev@ndustrial.io',
    'url': 'https://github.com/ndustrialio/contxt-sdk-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
