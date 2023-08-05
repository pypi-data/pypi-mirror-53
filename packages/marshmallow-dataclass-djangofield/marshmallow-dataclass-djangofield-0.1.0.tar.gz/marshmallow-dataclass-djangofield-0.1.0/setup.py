# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['marshmallow_dataclass_djangofield']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<3.0',
 'marshmallow>=3.0.3,<4.0.0',
 'marshmallow_dataclass>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'marshmallow-dataclass-djangofield',
    'version': '0.1.0',
    'description': 'Use marshmallow-dataclass as a Django Field',
    'long_description': "Use [marshmallow-dataclass](https://github.com/lovasoa/marshmallow_dataclass)es as [Django](https://github.com/django/django) Fields.\n\n## Usage\n```python\nfrom marshmallow_dataclass_djangofield import *\n\n\n\nclass MyModel(Model):\n    \n    @marshmallow_dataclass_djangofield(model_name='MyModel')\n    @marshmallow_dataclass.dataclass\n    class MyDataClass:\n        foo: str\n        bar: int\n\n    foobars = MarshmallowField(many=True, schema=MyDataClass)\n```\n",
    'author': 'Oliver Ford',
    'author_email': 'dev@ojford.com',
    'url': 'https://github.com/OJFord/marshmallow-dataclass-djangofield',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
