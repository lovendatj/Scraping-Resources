import uuid
import time
import functools
import json
from datetime import timedelta, datetime
import os

class LogEvent():
    class LogException(Exception):
        def __init__(self, message):
            super().__init__(message)

    def __init__(self, process:str):        
        self.start_time = time.perf_counter()
        self.logs = []
        self.process = process
        self.secret = "lovendatj"
        
    def _add_logs(log_type) -> None:
        def decorator(func):
            @functools.wraps(func)
            def log_message(self, message, *args, **kwargs):
                self.logs.append({
                    'timestamp': str( self._delta_time() ),
                    'type': log_type,
                    'message':message
                })
                return func(self, message, *args, **kwargs)
            return log_message
        return decorator

    @_add_logs(log_type="DEBUG")
    def log_debug(self, message: str) -> None:
        print(f'[{self._delta_time()}] DEBUG:: {message}')
       
    @_add_logs(log_type="LOG")
    def log_info(self, message: str) -> None:
        pass

    @_add_logs(log_type="ERROR")
    def log_error(self, message: str, quit: bool=False) -> None:
        if quit:
            raise self.LogException(message)

    def dump_logs(self):
        date_stamp = datetime.now().strftime('%m/%d/%Y-%H:%M:%S')
        return {
            "process": self.process,
            "file-name": self._uuid5(date_stamp),
            "date": date_stamp,
            "logs":self.logs
        }
    
    def log_file(self, path: str, filename: str=None, indent: int=None) -> None:
        data = self.dump_logs()
        filename = f"{path}/{data['file-name']}.json"
        if not os.path.exists(path):
            os.makedirs(path)
        with open(filename, 'w', encoding='utf-8') as outfile:
            if indent is not None:
                json.dump(data, outfile, indent=indent)
            else:
                json.dump(data, outfile)

    def _delta_time(self) -> float:
        end_time = time.perf_counter()
        return timedelta(seconds=end_time - self.start_time)
    def _uuid5(self, string:str) -> str:
        return str(uuid.uuid4())

# le = LogEvent(process="test")
# le.log_info('testing')
# le.log_file(indent=4)