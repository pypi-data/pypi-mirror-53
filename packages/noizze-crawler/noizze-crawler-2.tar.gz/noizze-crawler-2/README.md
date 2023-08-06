[![Latest Version](https://img.shields.io/pypi/v/noizze-crawler.svg)](https://pypi.org/project/noizze-crawler/)

# NOIZZE Crawler

A web page crawler PyPI Package which returns (title, og:image, og:description).

## Dependency
* BeautifulSoup4

## Installation
Run the folowing to install:

```shell
pip install noizze-crawler
```

## Usage

```python
from noizze_crawler import crawler

if __name__ == '__main__':
    url = 'https://dvdprime.com/g2/bbs/board.php?bo_table=comm&wr_id=20525678'
    title, desc, image_url, html = crawler(url)
    print(title, desc, image_url)  # html
```
