# Scraping-Resources
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## What is it?
Scraping Resources is a one-stop-shop for data from individuals taps. Current taps support include: [Reddit](https://github.com/lovendatj/Scraping-Resources/blob/main/Taps/RedditScraping/README.md) and [Google RSS Feed](https://github.com/lovendatj/Scraping-Resources/blob/main/Taps/GoogleRSS/README.md). Refer to the previous links for more detailed utilization of each class.

Install the dependencies using the following commands for deployment. 
```bash
virtualenv <venv name>
source <venv name>/Scripts/activate
pip install -r requirements.txt 
```
To leave the virtual environment use the following command
```bash
deactivate <venv name>
```
## Quick Start
Clone the repository and use the following command to run the project,:
```bash
python3 test.py
```
> Note: Add string elements to the `query` parameter to change searched results within the Google RSS Feed. Similary, changing the `sub`  and `queue` (restricted to 'submissions' or 'comments') will effect the Reddit Scraping.

## Data Output
Each tap will have a respective *Logs* and *Data* folder with JSON formatted files. An example of the data output from the application can be found here:

| Tap        | Sample Output                                                                                  |
| ---------- | ---------------------------------------------------------------------------------------------- |
| Reddit     | [output](https://github.com/lovendatj/Scraping-Resources/tree/main/Taps/RedditScraping/output) |
| Google RSS | [output](https://github.com/lovendatj/Scraping-Resources/tree/main/Taps/GoogleRSS/output)      |

## License
This project uses the [GPL v3 License](https://www.gnu.org/licenses/gpl-3.0.en.html)
