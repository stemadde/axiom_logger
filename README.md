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
