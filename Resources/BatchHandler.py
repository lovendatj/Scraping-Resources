from __future__ import annotations

import uuid

from Resources.LogEvent import LogEvent
from typing import Dict, List


class BatchHandler:

    def __init__(self, *args, **kwargs) -> None:
        self.process = self._type()
        self.verbose = bool(
            kwargs['verbose']) if 'verbose' in kwargs.keys() and kwargs['verbose'] is not None else False
        self.out_path = str(
            kwargs['out_path']) if 'out_path' in kwargs.keys() and kwargs['out_path'] is not None else None

    def __enter_(self, *args, **kwargs) -> BatchHandler:
        self.logger = LogEvent(self.process)
        self.logger.log_info(
            f'[{self.process}] Process started.')
        return self

    def __exit__(self, type, value, traceback) -> None:
        print(
            f'Completed {self.process}. Total Time: {self.logger.delta_timestrf()}')
        if self.file_handler is not None:
            fname = f"logs/{self.queue}-{self.file_handler.generate_file_name()}.json"
            self.logger.log_info(f'[FILE] Logs written to {fname}.')
            self.logger.log_info(
                f'[{self.process}] Process Completed.')
            self.file_handler.write_file(
                file_name=fname,
                data=self.logger.dump_logs(),
                indent=4)
        else:
            return

    def split_results(self, data: dict, bsize: int = 5) -> List:
        pass

    def _type(self) -> str:
        return self.__class__.__name__

    def generate_uuid4(self) -> str:
        return str(uuid.uuid4())
