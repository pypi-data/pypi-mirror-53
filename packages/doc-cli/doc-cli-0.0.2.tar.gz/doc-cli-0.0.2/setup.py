# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['doccli']

package_data = \
{'': ['*']}

install_requires = \
['decli>=0.5.1,<0.6.0', 'docstring-parser>=0.3,<0.4', 'pyyaml>=5.1.2,<6.0.0']

setup_kwargs = {
    'name': 'doc-cli',
    'version': '0.0.2',
    'description': 'Build Config classes that can be quickly turned into CLI specifications',
    'long_description': '# DocCli\n\nPython 3.6+ utility to build Classes that can be easily modified to create a Python\nArgparse specification. The goal of this is to couple a CLI specification to a config\nclass, making them quicker to build and less likely to break.\n\nThis leans heavily on the [Decli](https://github.com/Woile/decli) library\nto generate Argparse objects.\n\n## Creating CLI Objects\n\nCLI objects can be created automatically from a class definition, reading in default\nvalues and descriptions from type hints and the docstring. \n\n```python\nfrom doccli import DocCliParser\n\nclass CliTool:\n    command_name = "cli-tool"\n    def __init__(self, _non_cli_param: str, param_a: str, param_b, param_c: int = 5):\n        """This is the command description\n\n        Args:\n            _non_cli_param (str): Underscore leading params aren\'t included in the\n                                  CLI specs\n            param_a: A required parameter\n            param_b: Note that the type needs to come from the annotation\n            param_c: This one has a default\n        """\n\n        self.param_a = param_a\n        self.param_b = param_b\n        self.param_c = param_c\n\n        self.non_cli_param = non_cli_param\n\n# To create the argparse object:\nif __name__ == "__main__":\n    args = DocliParser(CliTool).parse_args()\n    ...\n```\n\nSee [examples](examples/) for more examples, including how to create CLIs with subcommands.\n\n## Config File Helpers\n\nDocCli also provides the `ConfigUtil` class which can be used to automatically\ncreate Python [configparser](https://docs.python.org/3/library/configparser.html)\nfiles. This functionality includes:\n\n- Inferring config specifications from the `__init__` method\n- Converting an instantiated object into a valid `configparser` dictionary\n  - This will ignore config values that have the same value as their default\n- Instantiating a class from an existing CFG file\n- Ability to nest Config objects in other objects, to create centralised config files\n\nObjects inheriting from the `ConfigUtil` class can set the following class level \nvariables:\n\n- config_key: str\n  - Parameters for this object. Defaults to the class name\n- sub_config_list: List<ConfigUtil>\n  - A list of Config Classes that also inherit from ConfigUtil, and are children of this class\n- flatten_sub_configs: bool\n  - Defaults to True. When reading from/writing to a dict, sub_configs will either be recorded\nas sub-dictionaries, or at the same level as the config items for the current dictionary.\n\n## Using them together\n\nThese tools can be used together to create a config class that can:\n- Generate a CLI parser \n- Initiate from a CLI parser, while also filling in unsupplied values from a Config file\n\nDocliParser has the method `parse_args_with_config_file`, which will attempt to \nfill in any unprovided arguments with values provided in the Config File. Note that \nthis will only work if:\n- The variables are stored as top-level keys in the file\n- The variables are stored in a sub-dictionary under the same key as the subcommand name\n- If the subcommand class inherits from `ConfigUtil` and the variables are stored in a \nsub-dictionary under the same key as the ConfigUtil.config_key variable\n',
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
