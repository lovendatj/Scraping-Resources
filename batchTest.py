from Taps.GoogleRSS.GoogleRSS import GoogleRSS
from Resources.BatchHandler import BatchHandler


query = ['Apples phone']
when = '24h'
opath = '../output/google-rss'
with (GoogleRSS(out_path=opath) as goog,
      BatchHandler(out_path=opath) as bh):
    results = goog.get_xml(query=query, when=when)
