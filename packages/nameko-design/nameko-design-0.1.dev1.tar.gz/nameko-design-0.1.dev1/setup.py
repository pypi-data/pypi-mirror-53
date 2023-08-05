# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nameko_design']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.10,<3.0']

entry_points = \
{'console_scripts': ['nameko-design = nameko_design.main:main']}

setup_kwargs = {
    'name': 'nameko-design',
    'version': '0.1.dev1',
    'description': 'Generate http files from design schema inspired by goa',
    'long_description': '# nameko-design\n\n![logo](./logo.png)\n\nGenerate [Nameko](https://www.nameko.io/) http files from design schema inspired by [goa](https://goa.design/)\n\n## Dependencies\n\n- Python3.6\n- [Poetry](https://github.com/sdispater/poetry)\n\n## Installation\n\n```bash\ncd nameko-design\npoetry install\n```\n\n## Usage\n\n```bash\ncd nameko-design\npoetry run nameko-design nameko_design/sample.py\n```\n\n## Design\n\nThis API design schema\n\n```python\nwith Service(\'http_service\'):\n    Title(\'This is a http service\')\n\n    with Method(\'liveness\'):\n        Description(\'liveness probe\')\n        Result(str)\n        HTTP(GET, \'/liveness\')\n\n    with Method(\'readiness\'):\n        Description(\'readiness probe\')\n        Result(str)\n        HTTP(GET, \'/readiness\')\n```\n\nwill generate the below nameko file\n\n```python\nfrom nameko.web.handlers import http\n\n\nclass HttpService:\n    name = \'http service\'\n\n    @http(\'GET\', \'/liveness\')\n    def liveness(self, request) -> str:\n        pass\n\n    @http(\'GET\', \'/readiness\')\n    def readiness(self, request) -> str:\n        pass\n```\n\n## TODO\n\n- [ ] Configure http url and port\n- [ ] Add URL parameter and type\n- [ ] Add payload (name, type, description, position etc)\n- [ ] Add validation\n- [ ] Add gRPC server\n- [ ] Generate proto files\n- [ ] Generate swagger json\n\nWhat I want:\n\n```python\nwith Service(\'example_service\'):\n    Title(\'This is an example service\')\n\n    with Method(\'liveness\'):\n        Description(\'liveness probe\')\n        Result(str)\n        HTTP(GET, \'/liveness\')\n\n    with Method(\'add\'):\n        Description(\'a + b\')\n        with Payload():                         # Not yet implemented\n            Field(1, "a", int, "left operand")  # Not yet implemented\n            Field(2, "b", int, "right operand") # Not yet implemented\n            Required("a", "b")                  # Not yet implemented\n        Result(int)\n        HTTP(GET, \'/add/{a}/{b}\')               # Not yet implemented\n        GRPC()                                  # Not yet implemented\n```\n',
    'author': 'yukinagae',
    'author_email': 'yuki.nagae1130@gmail.com',
    'url': 'https://github.com/yukinagae/nameko-design',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
