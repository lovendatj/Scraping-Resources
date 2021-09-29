# Scraping-Resources
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

Scraping Resources is a one-stop-shop for data from individuals taps. Current taps support include: [Reddit](https://www.reddit.com/), [Google RSS Feed](https://news.google.com/rss/search?q=News&hl=en-US&gl=US&ceid=US:en)

Install the dependencies using the following command:
```bash
pip install -r requirements.txt 
```
## Quick Start
To run the project, use the following command:
```bash
python3 test.py
```
> Note: Add string elements to the `query` parameter to change searched results within the Google RSS Feed. Similary, changing the `sub`  and `queue` (restricted to 'submissions' or 'comments') will effect the Reddit Scraping.
## Data Output

Each tap will have a `Log` and `Data` folder with JSON formatted files with task output. The sample directory output can be found here:

| Tap | Sample Output |
| ------ | ------ |
| Reddit | [output](https://github.com/lovendatj/Scraping-Resources/tree/main/Taps/RedditScraping/output) |
| Google RSS | [output](https://github.com/lovendatj/Scraping-Resources/tree/main/Taps/GoogleRSS/output) |

