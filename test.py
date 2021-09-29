from Taps.GoogleRSS.GoogleRSS import GoogleRSS
from Taps.RedditScraping.RedditData import RedditData


opath = '../Taps/GoogleRSS/output'
with GoogleRSS(out_path=opath) as goog:
    results = goog.get_xml(
        query=['APPL new phone', 'GME stock'], when='24h')
    goog.file_out(results)

opath = '../Taps/RedditScraping/output'
sub = ['WallStreetbets']
queue = 'comments'
with RedditData(sub=sub, queue=queue, out_path=opath) as reddit:
    results = reddit.data_dump()
    print(results)
    reddit.file_out(results)
