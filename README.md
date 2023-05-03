# axiom_logger
Python logging handler for the Axiom service


## Installation

```
pip install axiom_logger
```

## Usage
The handler overwrites the standard python Handler class from the logging module.
As such it can be used in the same way as any other handler.

When instanciating the handler, you must pass the following arguments:
- `AXIOM_DATASET`: The name of the dataset you want to push logs to
- `AXIOM_API_KEY`: The API key for your Axiom account

```python
import logging
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
