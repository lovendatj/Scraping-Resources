
import time
import functools
import json
import os

from datetime import timedelta, datetime
from typing import Dict, Any


class LogEvent():
    class LogException(Exception):
        def __init__(self, message):
            super().__init__(message)

    def __init__(self, process: str, *args, **kwargs):
        self.start_time = time.perf_counter()
        self.logs = []
        self.process = process
        if kwargs['verbose'] is not None:
            self.verbose = kwargs['verbose']

    def _add_logs(log_type) -> Any:
        def decorator(func):
            @functools.wraps(func)
            def log_message(self, message, *args, **kwargs):
                if self.verbose is not None and self.verbose:
                    print(f'[DEBUG] {log_type}: {message}')
                self.logs.append({
                    'timestamp': str(self._delta_time()),
                    'type': log_type,
                    'message': message
                })
                return func(self, message, *args, **kwargs)
            return log_message
        return decorator

    @_add_logs(log_type="LOG")
    def log_info(self, message: str) -> None:
        pass

    @_add_logs(log_type="ERROR")
    def log_error(self, message: str, quit: bool = False) -> None:
        if quit:
            raise self.LogException(message)

    def dump_logs(self) -> Dict:
        return {
            "process": self.process,
            "date": self.time_stamp(),
            "logs": self.logs
        }

    def _delta_time(self) -> float:
        end_time = time.perf_counter()
        return timedelta(seconds=(end_time - self.start_time))

    def time_stamp(self) -> str:
        return datetime.now().strftime('%m/%d/%Y-%H:%M:%S')
