# Grow Recipe Python SDK

A python package to provide functionality to the [Grow Recipe Schema](https://github.com/njason/grow-recipe-schema)

NOTE: [lxml](https://lxml.de/) is not a requirement, however grow recipes cannot be validated against a schema without it. To validate grow recipes during run time, install lxml through pip:

`$ pip install lxml`

Alternatively, you can manually validate grow recipes using a XML Schema validator, such as [xmllint](http://xmlsoft.org/xmllint.html). Refer [here](https://github.com/njason/grow-recipe-schema#install-xmllint) for installation instructions.

## Installation

[pip](https://pip.pypa.io/en/stable/):

`$ pip install grow-recipe`


## Usage

```
from datetime import datetime

import grow_recipe

# keep track of the start of the grow
start_time = datetime(2018, 12, 17)

with open('some_file.xml') as xml_file:
    temperature_range = grow_recipe.get_metric(
        xml_file, 'air', 'temperature', start_time, datetime.now())

print('Temperature minimum ' + temperature_range.min)
print('Temperature maximum ' + temperature_range.max)
```


## Development

Setup with pip:
`$ pip install -r requirements.txt`

To test schema support, install lxml through pip, or run:
`$ pip install -r optional-requirements.txt`

Also, include the `grow_recipe` package in editable mode by running `$ pip install -e .` in the repository root.

To run tests, run `$ pytest`

Unfortunately, setuptools does not support submodules. So the [XML schema](grow_recipe/grow-recipe.xsd) must be kept updated with the [source](https://github.com/njason/grow-recipe-schema/blob/master/grow-recipe.xsd)
