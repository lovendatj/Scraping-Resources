import requests
import time
import urllib.parse as urlf
import xml.etree.cElementTree as ET
import os 
import json
from datetime import datetime
from Resources.LogEvent import LogEvent

class GoogleRSS:
    def __init__(self, verbose: bool=False, outpath: str='.') -> None:
        self.process=self._type()
        self.logger = LogEvent (self.process)
        self.verbose = verbose
        self.outpath = outpath
        self.default_link = 'https://news.google.com/rss/search?'
        self._output_handler('Initializing GoogleRSS Tap')

    def __enter__(self, *args, **kwargs):
        return self
    def __exit__(self, type, value, traceback):
        self.logger.log_file(path=f'{self.outpath}/logs', indent=4)
    
    def get_xml(self, query: list, when: str=None, utc_time: tuple=None, dump_file: bool= False) -> dict:
        return_data = {}
        for term in query:
            url_builder = f'{self.default_link}'
            try:
                if when is not None:
                    url_builder += f'q={urlf.quote(term)}+when={when}'    
                elif utc_time is not None:
                    url_builder += f'q={urlf.quote(term)}+before={utc_time[0]}+after={utc_time[1]}'
                else: 
                    url_builder += f'q={urlf.quote(term)}'
                url_builder += '&ceid=US:en&hl=en-US&gl=US'

                self._output_handler(f'[Term]: {term} [Request]: {url_builder}')
                    
                return_data[term] = self._parse_xml(return_data, requests.get(url_builder).text)
            
                time.sleep(.5)

            except Exception as error:
                self.logger.log_error(message=f'Error occured creating request. REQ: {url_builder}', quit=False) 
        if dump_file:
            self.dump_data(data=return_data, path=f'{self.outpath}/data', indent=4)
        return return_data
        
    def _output_handler(self, message):
        if self.verbose:
            self.logger.log_debug(message)
        else:
            self.logger.log_info(message)

    def _parse_xml(self, return_data:dict, xml_str:str) -> list:
        out_data = []
        root = ET.fromstring(xml_str).find('channel')
        for ele in root.findall('item'):
            out_data.append({
                'source':ele.find('source').text,
                'source-url':ele.find('source').attrib['url'],
                'url':ele.find('link').text,
                'pub-date':ele.find('pubDate').text,
                'title':ele.find('title').text
            })            
        return out_data

    def _type(self):
        return self.__class__.__name__
    
    def dump_data(self, data: dict, path: str, indent: int=None) -> None:
        date_stamp = datetime.now().strftime('%m/%d/%Y-%H:%M:%S')
        output = {
            "process": self.process,
            "file-name": self.logger._uuid5(date_stamp),
            "date": date_stamp,
            "data": data
        }
        filename = f"{path}/{output['file-name']}.json"
        if not os.path.exists(path):
            os.makedirs(path)
        with open(filename, 'w', encoding='utf-8') as outfile:
            if indent is not None:
                json.dump(output, outfile, indent=indent)
            else:
                json.dump(output, outfile)