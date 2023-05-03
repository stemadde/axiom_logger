import time
import requests
from logging import LogRecord, Formatter
from logging import Handler

from requests.adapters import HTTPAdapter, Retry

AXIOM_V1 = 'https://api.axiom.co/v1/datasets'
_defaultFormatter = Formatter()


class AxiomHandler(Handler):
    def __init__(self, dataset: str, api_token: str, api_url=AXIOM_V1):
        assert api_token, 'api_token is required for AXIOM logging'
        assert dataset, 'a dataset name is required for AXIOM logging'
        self.endpoint = f'{api_url}/{dataset}/ingest'
        self.api_token = api_token

        # sets up a session with the server
        self.MAX_POOLSIZE = 100
        self.session = session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % self.api_token
        })
        self.session.mount('https://', HTTPAdapter(
            max_retries=Retry(
                total=5,
                backoff_factor=0.5,
                status_forcelist=[403, 500]
            ),
            pool_connections=self.MAX_POOLSIZE,
            pool_maxsize=self.MAX_POOLSIZE
        ))

        super().__init__()

    def emit(self, record: LogRecord) -> None:
        try:
            log_entry = self.axiom_format(record)
            res = self.session.post(self.endpoint, json=log_entry)
            print(res.status_code)
            print(res.text)
        except Exception:
            self.handleError(record)

    def axiom_format(self, record: LogRecord) -> list:
        return [{
            "_time": record.created,
            "data": record.getMessage(),
        }]

    async def wait(self):
        time.sleep(10)
        self.send()
        return True
