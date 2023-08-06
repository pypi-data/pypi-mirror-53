# acrawler-cfscrape

The handler works with [aCrawler](https://github.com/wooddance/aCrawler) and [cloudscraper](https://github.com/VeNoMouS/cloudscraper)

## Installation

```bash
$ pip install acrawler_cfscrape
```

## Usage

Add Handler:

```python
class MyCrawler(Crawler):
    middleware_config = {
        "acrawler_cfscrape.CfscrapeHandler": True,
    }

    config = {
        "CFS_COOKIES_FILE": Path.home() / ".cfscookies",
        "CFS_URL": "http://www.example.com",
        "CFS_PROXIES": None,
    }
```
