## The Reddit Scraping Tap
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

#### What is it?
The Reddit Scraping utilizes the submissions and comments feed to scrape data from a given subreddit. We can customize our search by providing a `subreddit` parameter to the URL along with some additional parameters, such as `new|hot|top` (to indicate a feed) and `after` (to specify an index on a page).
> ##### An example of a URL
> [https://www.reddit.com/r/`subreddit`/`new|hot|top`.json?size=100&`after`=pn1234](https://www.reddit.com/r/`subreddit`/`new|hot|top`.json?size=100&`after`=pn1234)

#### Sample code
To customize the RedditScraping Object, add string subreddits to the `sub` list and 'submissions' or 'comments' to `queue` parameter to change searched results from the RedditScraping object.

```python
# Data output path
opath = '../Taps/RedditScraping/output'
# Any subreddit
sub = ['WallStreetbets']
# The queue parameter takes options 'submissions' or comments'
queue = 'comments'
with RedditData(sub=sub, queue=queue, out_path=opath) as reddit:
    results = reddit.data_dump()
    reddit.file_out(results)

```

Refer to the file output for examples of the [data](https://github.com/lovendatj/Scraping-Resources/blob/main/Taps/GoogleRSS/output/data/) and [logs](https://github.com/lovendatj/Scraping-Resources/blob/main/Taps/GoogleRSS/output/logs/) generated.