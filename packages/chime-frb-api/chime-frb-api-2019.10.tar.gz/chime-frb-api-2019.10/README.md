# CHIME/FRB API

|   **`Build`**   | **`Coverage`**  |   **`Docs`**    |  **`Release`**  |   **`Style`**    |
|-----------------|-----------------|-----------------|-----------------| -----------------|
|[![Build Status](https://travis-ci.com/CHIMEFRB/frb-api.svg?token=mRNzzrGmJQewCpZQsov9&branch=master)](https://travis-ci.com/CHIMEFRB/frb-api)| [![Coverage Status](https://coveralls.io/repos/github/CHIMEFRB/frb-api/badge.svg?branch=master&t=uYdqsa)](https://coveralls.io/github/CHIMEFRB/frb-api?branch=master) | `Soon!`   | [![PyPI version](https://img.shields.io/pypi/v/chime-frb-api.svg)](https://pypi.org/project/chime-frb-api/) | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

--------

`chime-frb-api` is a Python 3 library to access the all components spread throught the CHIME/FRB project. This library enables you interact with resources such as databases, event headers, calibration products, cluster jobs and the CHIME/FRB backend.

## Install
```
pip install chime-frb-api
```

## Usage
```python
from chime_frb_api import distributor

# Create a distributor instance
distributor = distributor.Distributor(base_url="http://frb-vsop.chime:8002")

# Create distributor
distributor.create_distributor("test")

# Get status of the distributor
status = distributor.get_status("test")
print(status)
```

## Documentation
More information will be added here soon.

## Development
Coming Soon!


