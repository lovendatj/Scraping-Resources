## The Google RSS Tap
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

#### What is it?
The Google RSS News Feed utilizes Google Search with up-to date articles published across the web. We can customize our search by providing a `query` parameter to the URL along with some additional paramters, such as `when`, `before`, and `after`.
> ##### An example of a URL
> [https://news.google.com/rss/search?q=`term`&hl=en-US&gl=US&ceid=US:en](https://news.google.com/rss/search?q=`term`&hl=en-US&gl=US&ceid=US:en)

#### Sample code
To customize the GoogleRSS Object, add string elements to the `query` parameter to change searched results from the Google RSS Feed. Adding the when parameter (e.g. "3hr") to restrict the time frame. 
```python
from Taps.GoogleRSS.GoogleRSS import GoogleRSS

# Output file path
opath = '../Taps/GoogleRSS/output'
# Search Term
query = ['GME stock']
# Time Bound
when = '3hr'
with GoogleRSS(out_path=opath) as goog:
    results = goog.get_xml(
        query=query, when=when)
    goog.file_out(results)
```

Refer to the file output for examples of the [data](https://github.com/lovendatj/Scraping-Resources/blob/main/Taps/GoogleRSS/output/data/) and [logs](https://github.com/lovendatj/Scraping-Resources/blob/main/Taps/GoogleRSS/output/logs/) generated.