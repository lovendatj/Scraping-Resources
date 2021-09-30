from Taps.GoogleRSS.GoogleRSS import GoogleRSS
from Resources.BatchHandler import BatchHandler


query = ['Apples phone']
when = '24h'
with GoogleRSS() as goog:
    results = goog.get_xml(query=query, when=when)
