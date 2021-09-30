from Taps.GoogleRSS.GoogleRSS import GoogleRSS
from Taps.RedditScraping.RedditData import RedditData

# Output file path
opath = '../output/google-rss'
# Search Term
query = ['Apples new phone', 'Adventures of Mr. Bean']
# Time Bound
when = '24h'

with GoogleRSS(out_path=opath) as goog:
    results = goog.get_xml(
        query=query, when=when)
    goog.file_out(results)

# Data output path
opath = '../output/reddit'
# Any subreddit
sub = ['WallStreetbets']
# The queue parameter takes options 'submissions' or comments'
queue = 'comments'

with RedditData(sub=sub, queue=queue, out_path=opath) as reddit:
    results = reddit.data_dump()
    reddit.file_out(results)
