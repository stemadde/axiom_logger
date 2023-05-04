# axiom_logger
Python logging handler for the Axiom service (https://axiom.co/)


## Installation

```
pip install axiom-logger
```

## Usage
The handler overwrites the standard python Handler class from the logging module.
As such it can be used in the same way as any other handler.

When instanciating the handler, you must pass the following arguments:
- `AXIOM_DATASET`: The name of the dataset you want to push logs to
- `AXIOM_API_KEY`: The API key for your Axiom account

```python
import logging
import os
from axiom_logger import AxiomHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ah = AxiomHandler(
    os.environ.get('AXIOM_DATASET', 'test'),
    os.environ.get('AXIOM_API_TOKEN', 'xxxx-api-key-xxxx')
)
ah.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ah.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ah)
```

## Configuration options
The axiom logger provides some configuration options to customize the behaviour of the handler.
While instantiating the handler the following additional parameters can be passed

* `api_url`: String representing the URL of the Axiom API. Defaults to https://api.axiom.co/v1/datasets
* `mode`: Either one of ['elapsed_time' | 'log_count']. Defaults to 'elapsed time'. Customizes the behaviour of the 
logger to send records every _elapsed_time_ seconds or every _log_count_ records.
* `elapsed_time`: Float representing the number of seconds to wait before sending records to Axiom. Defaults to 10.
* `log_count`: Integer representing the number of records to wait before sending records to Axiom. Defaults to 5.

To send a log to the Axiom service each time a record is emitted (sync procedure) the following configuration can be used:

```python
AxiomHandler(
    os.environ.get('AXIOM_DATASET', 'test'),
    os.environ.get('AXIOM_API_TOKEN', None),
    mode='log_count',
    log_count=1
)
```

__WARNING:__ If an async procedure is used an unexpected shutdown of the application may result in the loss of 
the logs contained in the record pool of the handler.  

__NOTE:__ If the procedure used to send logs to Axiom fails for any reason, the handler will issue a system warning 
stating the error occurred with the Axiom backend, and will also print the log records that failed to be sent.

## Django integration
Since the handler is a standard python logging handler, it can be used in any python application.
A worth mentioning example is the integration with Django.

To use the handler in a Django application, the following configuration can be used:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'axiom': {
            'class': 'axiom_logger.AxiomHandler',
            'dataset': os.getenv('AXIOM_DATASET', 'dataset-name'),
            'api_token': os.getenv('AXIOM_API_KEY', None)
        }
    },
    'root': {
        'handlers': ['axiom'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['axiom'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
```