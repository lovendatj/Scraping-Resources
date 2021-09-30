import json
from typing import Tuple, List, Dict


def data_alias(type: str, data: Dict) -> List[Tuple[str, List]]:
    raise Exception('Not Implement')
    # if type == 'reddit':
    #     return [(sub, data['data'][sub]['data']) for sub in data[]
