from __future__ import annotations

import requests as req

from Resources.FileHandler import FileHandler
from Resources.LogEvent import LogEvent
from datetime import datetime
from typing import Dict, List


class RedditData:
    class RequestBreak(Exception):
        def __init__(self):
            super().__init__()


# , log_func: dict = None, monitor: dict = None, time_interval: int = 15,
# Change Time Interval to Environment Variable
# self.time_interval = datetime.now().timestamp()-time_interval*60
# API Request Limit
# self.lim = 100
# verbose: bool = False, out_path: str = None

    def __init__(self, sub: List[str], queue: str, *args, **kwargs) -> None:
        self.verbose = bool(
            kwargs['verbose']) if 'verbose' in kwargs.keys() and kwargs['verbose'] is not None else False
        self.out_path = str(
            kwargs['out_path']) if 'out_path' in kwargs.keys() and kwargs['out_path'] is not None else None
        self.time_interval = int(
            kwargs['time_interval']) if 'time_interval' in kwargs.keys() and kwargs['time_interval'] is not None else 15
        self.time_interval = datetime.now().timestamp()-self.time_interval*60

        self.lim = int(kwargs['lim']) if 'lim' in kwargs.keys(
        ) and kwargs['lim'] is not None else 100

        # Subreddits List
        self.sub = sub
        # Scrape Type
        self.queue = queue
        # Default endpoint
        self.default_endpoint = 'https://www.reddit.com/r'
        self.process = self._type()

    def __enter__(self, *args, **kwargs) -> RedditData:
        self.logger = LogEvent(self.process, verbose=self.verbose)

        # Operations Handling (e.g., Comments vs Submissions Scraping)
        if self.queue not in ['comments', 'submissions']:
            self.logger.log_error(
                f'{self.queue} is not a valid scraping operation.', True)

        self.logger.log_info(
            f'[{self.process}] Process started.')
        if self.out_path is not None:
            self.file_handler = FileHandler(path=self.out_path)
            _, message = self.file_handler.mkdir(
                f'{str(self.process)}/{self.out_path}')
            self.logger.log_info(
                f'[{self.process}] Output path: \'{self.out_path}\'')
        else:
            self.file_handler = None
            self.logger.log_info(
                f'[{self.process}] Output path not provided.')
        return self

    def __exit__(self, type, value, traceback):
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

    def data_dump(self):
        if self.queue == 'submissions':
            return self._get_post()
        elif self.queue == 'comments':
            return self._get_comments()

    # Wrapper function, executes _post_body_builder
    def _get_post(self):
        return_data = {}
        for sub in self.sub:
            results = self._post_body_builder(sub=sub)
            return_data[sub] = {
                'info': {
                    'timedelta': self.logger.delta_timestrf(),
                    'total-obj': len(results)
                },
                'data': results
            }
        return return_data
    # Return list of dictionary with post data for passed subreddit

    def _post_body_builder(self, sub: str):
        data = []
        targeting_data = True
        after = ''
        while targeting_data:
            # Build requests
            url_builder = f'{self.default_endpoint}/{sub}/new.json?size={str(self.lim)}&after={after}'
            self.logger.log_info(
                f'[{sub}] Starting request: [Request]: {url_builder}')
            try:
                # Response
                res = req.get(url_builder, headers={
                              'User-agent': f'{self.process}/0.1'}).json()
                after = res['data']['after']
                # Append child if within time interval
                for child in res['data']['children']:
                    if child['data']['created_utc'] > float(self.time_interval):
                        data.append(child)
                    else:
                        # Break out of Loop when comments are outside of time interval
                        raise self.RequestBreak()
            except self.RequestBreak:
                targeting_data = False
            except Exception:
                self.logger.log_error(
                    f'[{sub}] Error creating submission request. REQ: {url_builder}')
                return
            self.logger.log_info(f'[{sub}] Comment requests complete.')
        return data

    # Wrapper function, executes _comment_body_builder
    def _get_comments(self):
        return_data = {}
        for sub in self.sub:
            results = self._comment_body_builder(sub=sub)
            return_data[sub] = {
                'info': {
                    'elapsed': self.logger.delta_timestrf(),
                    'total-obj': len(results)
                },
                'data': results
            }
        return return_data

    # Return list of dictionary with comment data for passed subreddit
    def _comment_body_builder(self, sub: str):
        data = []
        targeting_data = True
        after = ''
        while targeting_data:
            # Build requests
            url_builder = f'{self.default_endpoint}/{sub}/comments/.json?size={str(self.lim)}&after={after}&sort=desc'
            self.logger.log_info(
                f'[{sub}] Starting request: [Request]: {url_builder}')
            try:
                # Response
                res = req.get(url_builder, headers={
                              'User-agent': 'Darwinism/0.1'}).json()
                after = res['data']['after']
                # Append child if within time interval
                for child in res['data']['children']:
                    if child['data']['created_utc'] > float(self.time_interval):
                        data.append(child)
                    else:
                        # Break out of Loop when comments are outside of time interval
                        raise self.RequestBreak()
            except self.RequestBreak:
                targeting_data = False
            except Exception:
                self.logger.logger(
                    f'[{sub}] Error creating comment request. REQ: {url_builder}')
                return
            self.logger.log_info(f'[{sub}] Comment requests complete.')
        return data

    def file_out(self, data: Dict) -> None:
        if self.file_handler is None:
            self.logger.log_error(
                "Output path not provided during initialization.")
            return
        output = {
            "process": self.process,
            "file-name": self.file_handler.generate_file_name(),
            "date": self.logger.time_stamp(),
            "data": data
        }

        fname = f"data/{self.queue}-{output['file-name']}.json"
        self.logger.log_info(
            f"[FILE] Writing to {self.file_handler._path()}/{fname} file..")
        status, message = self.file_handler.write_file(
            file_name=fname,
            data=output,
            indent=4
        )
        if status != 200:
            self.logger.log_error(f'[FILE] {message}')
        else:
            self.logger.log_info(f'[FILE] {message}')

    def _type(self):
        return self.__class__.__name__
