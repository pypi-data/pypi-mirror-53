[![Documentation Status](https://readthedocs.org/projects/ez-logger/badge/?version=latest)](https://ez-logger.readthedocs.io/en/latest/?badge=latest)
[![Pipeline Status](https://gitlab.com/varmarakesh/simple-logger/badges/master/pipeline.svg)](https://gitlab.com/varmarakesh/simple-logger/pipelines)
[![PyPI](https://img.shields.io/pypi/v/ez-logger.svg)](https://pypi.org/project/ez-logger/)
[![PyPI](https://img.shields.io/pypi/l/ez-logger.svg)](https://pypi.org/project/ez-logger/)

ez-logger 
==

`ez-logger` is a python module that offers easy to use API's for performing common logging operations.

This library has been tested on the following platforms.
* Windows
* Linux
* Mac OSX

It also works on both python major versions.

* python 2.7
* python 3.6

API Docs
--

API docs are maintained [here](https://ez-logger.readthedocs.io/en/latest/index.html)

Usage
--

```bash
pip install ez-logger
```

```python
from ez_logger.console_logger import ConsoleLogger
logger = ConsoleLogger()
logger.error('some error occurred')
```

```bash
from ez_logger.file_logger import FileLogger
logger = FileLogger(
   log_file='test.log',
   log_dir='/tmp'
)
logger.error('some error occurred')
```

Refer to [API Docs](https://ez-logger.readthedocs.io/en/latest/index.html) for detailed documentation.

Development
--

```bash
virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
```

Run Tests
--

```bash
python -m pytest -v tests/unit/*.py --spec
```
