from __future__ import annotations

import requests
import urllib.parse as urlf
import xml.etree.cElementTree as ET
import time

from Resources.FileHandler import FileHandler
from Resources.LogEvent import LogEvent
from typing import Dict, List


class GoogleRSS:

    class DeepSearch:
        pass

    def __init__(self, *args, **kwargs) -> None:
        self.verbose = bool(
            kwargs['verbose']) if 'verbose' in kwargs.keys() and kwargs['verbose'] is not None else False
        self.out_path = str(
            kwargs['out_path']) if 'out_path' in kwargs.keys() and kwargs['out_path'] is not None else None
        self.default_link = 'https://news.google.com/rss/search?'
        self.process = self._type()

    def __enter__(self, *args, **kwargs) -> GoogleRSS:
        self.logger = LogEvent(self.process, verbose=self.verbose)
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
            fname = f"logs/{self.file_handler.generate_file_name()}.json"
            self.logger.log_info(f'[FILE] Logs written to {fname}.')
            self.logger.log_info(
                f'[{self.process}] Process Completed.')
            self.file_handler.write_file(
                file_name=fname,
                data=self.logger.dump_logs(),
                indent=4)
        else:
            return

    def get_xml(self, query: List, *args, **kwargs) -> Dict:
        return_data = {}
        for term in query:
            url_builder = f'{self.default_link}'
            try:
                if kwargs['when'] is not None:
                    url_builder += f'q={urlf.quote(term)}+when={ str(kwargs["when"]) }'
                elif kwargs['utc_time'] is not None:
                    _start, _end = kwargs['utc_time']
                    url_builder += f'q={urlf.quote(term)}+before={ _start }+after={ _end }'
                else:
                    url_builder += f'q={urlf.quote(term)}'
                url_builder += '&ceid=US:en&hl=en-US&gl=US'

                self.logger.log_info(
                    f'[Term] {term}: [Request]: {url_builder}')

                results = self._parse_xml(
                    requests.get(url_builder).text)
                return_data[term] = {
                    'info': {
                        'timedelta': self.logger.delta_timestrf(),
                        'total-obj': len(results)
                    },
                    'data': results
                }
                self.logger.log_info(
                    f'[Term] {term}: Completed request.')
                # Avoid Spamming, will get blocked.
                time.sleep(.5)

            except Exception as error:
                self.logger.log_error(
                    message=f'Error occured creating request. REQ: {url_builder}', quit=False)
        return return_data

    def _parse_xml(self, xml_str: str) -> List:
        out_data = []
        root = ET.fromstring(xml_str).find('channel')
        for ele in root.findall('item'):
            out_data.append({
                'source': ele.find('source').text,
                'source-url': ele.find('source').attrib['url'],
                'url': ele.find('link').text,
                'pub-date': ele.find('pubDate').text,
                'title': ele.find('title').text
            })
        return out_data

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

        fname = f"data/{output['file-name']}.json"
        self.logger.log_info(
            f"[FILE] Writing to {self.file_handler._path()}/{fname} file.")
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
