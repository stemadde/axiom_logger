import atexit
import threading
import time
import warnings
from datetime import datetime
import requests
from logging import LogRecord, Formatter, Handler
from typing import Literal
from requests.adapters import HTTPAdapter, Retry

AXIOM_V1 = 'https://api.axiom.co/v1/datasets'
_defaultFormatter = Formatter()


class AxiomHandler(Handler):
    def __init__(
            self,
            dataset: str,
            api_token: str,
            api_url=AXIOM_V1,
            mode: Literal['elapsed_time', 'log_count'] = 'elapsed_time',
            elapsed_time: float = 10,
            log_count: int = 5
    ):
        """
        :param dataset: Name of the remote dataset to log to
        :param api_token: API token used for authentication against the Axiom remote service
        :param api_url: Override this value if you are using a different version of the Axiom API
        :param mode: Defaults to "elapsed_time" which will send logs every elapsed_time seconds.
            Can be changed to "log_count" which will send logs every log_count sent logs.
        :param elapsed_time: Time in seconds to wait before sending logs. Only used if mode is "elapsed_time"
        :param log_count: Count of logs to wait before sending logs. Only used if mode is "log_count"
        """
        # Assertion checks
        assert api_token, 'api_token is required for AXIOM logging'
        assert dataset, 'a dataset name is required for AXIOM logging'
        if mode == 'elapsed_time' and not elapsed_time:
            raise AssertionError('elapsed_time is required for mode elapsed_time')
        if mode == 'log_count' and not log_count:
            raise AssertionError('log_count is required for mode log_count')

        # Sets up the handler
        self.endpoint = f'{api_url}/{dataset}/ingest'
        self.api_token = api_token
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

        # Sets up the mode
        self.record_pool = []
        self.mode = mode
        self.elapsed_time = elapsed_time
        self.log_count = log_count
        self.is_sending = False

        if self.mode == 'elapsed_time':
            self.timer = None

        atexit.register(self.send)
        super().__init__()

    def emit(self, record: LogRecord) -> None:
        while True:
            if self.is_sending:
                time.sleep(0.2)
                continue
            break

        log_entry = self.axiom_format(record)
        self.record_pool.append(log_entry)

        if self.mode == 'log_count':
            if len(self.record_pool) >= self.log_count:
                self.send()
        else:
            if not self.timer or not self.timer.is_alive():
                self.timer = threading.Timer(self.elapsed_time, self.send)
                self.timer.start()

    def axiom_format(self, record: LogRecord) -> dict:
        dict_ = {
            "_time": record.created,
            "formatted_message": self.format(record),
        }
        dict_.update(record.__dict__)
        return dict_

    def send(self) -> None:
        if not self.record_pool:
            return
        self.is_sending = True
        res = self.session.post(self.endpoint, json=self.record_pool)
        if not res.status_code == 200:
            not_logged_records = '\n'.join(
                f"{datetime.fromtimestamp(record['_time'])} -> {record['data']}" for record in self.record_pool
            )
            warnings.warn(
                f'Failed to send logs to Axiom.\n'
                f'Status code: {res.status_code}\n'
                f'Response: {res.text}\n'
                f'==== Begin of unsent records ===='
                f'\n{not_logged_records}\n'
                f'==== End of unsent records ====',
                RuntimeWarning
            )
        self.record_pool = []
        self.is_sending = False
