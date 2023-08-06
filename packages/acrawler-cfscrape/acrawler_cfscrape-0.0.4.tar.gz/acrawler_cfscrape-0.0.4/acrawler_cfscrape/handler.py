import json
from pathlib import Path

import cloudscraper
from yarl import URL

from acrawler import ReScheduleImmediatelyError, get_logger
from acrawler.handlers import ExpiredWatcher


logger = get_logger("cfscrape")


class CfscrapeHandler(ExpiredWatcher):
    """Bypass the cloudflare.
    """

    family = "Request"
    priority = 500
    ttl = 20

    async def custom_on_start(self):
        """Load local token and update cookies if it is possible.
        """

        self.p = Path(
            self.crawler.config.get("CFS_COOKIES_FILE", Path.home() / ".cfscookies")
        )
        self.proxies = self.crawler.config.get("CFS_PROXIES", None)
        self.url = URL(self.crawler.config.get("CFS_URL"))
        self.ua = self.crawler.config.get(
            "CFS_USERAGENT",
            self.crawler.request_config.get("headers").get("User-Agent"),
        )

        logger.info("Cloudflare Bypass Handler starts.")
        if self.p.exists():
            logger.info("Find cookies file. Try to load...")
            with self.p.open("r") as f:
                tokens = json.load(f)
            self.crawler.session.cookie_jar.update_cookies(tokens, self.url)

    async def custom_expired_worker(self):
        tokens = self.get_tokens()
        self.crawler.session.cookie_jar.update_cookies(tokens, self.url)

    async def handle_after(self, request):
        if request.url.host == self.url.host and request.response:
            if request.response.status == 503:
                self.expired.set()
                raise ReScheduleImmediatelyError(defer=2)

    def get_tokens(self) -> dict:
        """Call cfscrape

        Returns:
            dict: cookies
        """

        tokens, user_agent = cloudscraper.get_tokens(
            self.url, headers={"User-Agent": self.ua}, proxies=self.proxies
        )
        logger.warning(tokens)
        with self.p.open("w") as f:
            json.dump(tokens, f)
        return tokens
