import os
import json
import uuid
from datetime import datetime
from typing import Tuple


class FileHandler:

    def __init__(self, path) -> None:
        self.path = path

    def mkdir(self, path: str, overwrite: bool = False) -> Tuple[int, str]:
        if overwrite and os.path.exists(path):
            os.remove(path)
        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.exists(path+'/data'):
            os.makedirs(path+'/data')
        if not os.path.exists(path+'/logs'):
            os.makedirs(path+'/logs')
        return (200, f"{path} created.")

    def write_file(self, file_name: str, data: dict, *args, **kwargs) -> Tuple[int, str]:
        try:
            with open(f'~/{self.path}/{file_name}', 'w+', encoding='utf-8') as outfile:
                if kwargs['indent'] is not None:
                    json.dump(data, outfile, indent=kwargs['indent'])
                    return (200, f"Data written to {file_name}.")
                else:
                    json.dump(data, outfile)
                    return (200, f"Data written to {file_name}.")
        except:
            return (500, f"Could not write to {file_name}.")

    def generate_file_name(self) -> str:
        return str(datetime.now().strftime('%m%d%Y')+'-'+self.generate_uuid4())

    def _path(self) -> str:
        return self.path

    def generate_uuid4(self) -> str:
        return str(uuid.uuid4())
