# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['doccli']

package_data = \
{'': ['*']}

install_requires = \
['decli>=0.5.1,<0.6.0', 'docstring-parser>=0.3,<0.4']

setup_kwargs = {
    'name': 'doc-cli',
    'version': '0.0.1',
    'description': 'Build Config classes that can be quickly turned into CLI specifications',
    'long_description': '# DocCli\n\nPython 3.6+ utility to build Classes that can be easily modified to create a Python\nArgparse specification. The goal of this is to couple a CLI specification to a config \nclass, making them quicker to build and less likely to break.\n\nThis leans heavily on the [Decli](https://github.com/Woile/decli) library \nto generate Argparse specifications.\n\n```python\nfrom doccli import DocliParser\n\nclass CliTool:\n    def __init__(self, _non_cli_param: str, param_a: str, param_b: int = 5):\n        """Some CLI Tool description. \n\n        Note that only the short description is included in the parser description\n        \n        Args:\n            _non_cli_param (str): Underscore leading params aren\'t included in the\n                                  CLI specs\n            param_a (str): A required parameter \n            param_b (int, optional): This one has a default\n        """\n\n        self.param_a = param_a\n        self.param_b = param_b\n\n        self.non_cli_param = non_cli_param\n\n# This creates a Decli Specification \nparser_spec = DocliParser.create_decli_spec(CliTool)\n\nassert parser_spec == {\n    "prog": "CliTool",\n    "description": "Some CLI Tool description",\n    "arguments": [\n        {\n            "name": "--param-a",\n            "type": str,\n            "help": "A required parameter",\n        },\n        {\n            "name": "--param-b",\n            "type": int,\n            "default": 5,\n            "help": "This one has a default",\n        },\n    ],\n}\n\n# To create the argparse object:\nparser = DocliParser(CliTool)\n```\n\nSee [examples](examples/) for more examples.',
    'author': 'mayansalama',
    'author_email': 'micsalama@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mayansalama/doc-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
