from __future__ import annotations

from Resources.LogEvent import LogEvent

from typing import Dict, List


class BatchHandler:

    def __init__(self, *args, **kwargs) -> None:
        pass

    def __enter_(self, *args, **kwargs) -> BatchHandler:
        return self

    def __exit__(self, type, value, traceback) -> None:
        pass

    def split_results(self, data: dict, bsize: int = 5) -> List:
        pass
