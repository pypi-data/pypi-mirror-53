Use [marshmallow-dataclass](https://github.com/lovasoa/marshmallow_dataclass)es as [Django](https://github.com/django/django) Fields.

## Usage
```python
from marshmallow_dataclass_djangofield import *



class MyModel(Model):
    
    @marshmallow_dataclass_djangofield(model_name='MyModel')
    @marshmallow_dataclass.dataclass
    class MyDataClass:
        foo: str
        bar: int

    foobars = MarshmallowField(many=True, schema=MyDataClass)
```
