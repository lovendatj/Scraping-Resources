from Taps.GoogleRSS.GoogleRSS import GoogleRSS
from Taps.RedditScraping.RedditData import RedditData


# Data output path
opath = '../Taps/GoogleRSS/output'
with GoogleRSS(out_path=opath) as goog:
    results = goog.get_xml(
        query=['APPL new phone', 'GME stock'], when='24h')
    goog.file_out(results)

# Data output path
opath = '../Taps/RedditScraping/output'
# Any subreddit
sub = ['WallStreetbets']
# The queue parameter takes options 'submissions' or comments'
queue = 'comments'
with RedditData(sub=sub, queue=queue, out_path=opath) as reddit:
    results = reddit.data_dump()
    reddit.file_out(results)
