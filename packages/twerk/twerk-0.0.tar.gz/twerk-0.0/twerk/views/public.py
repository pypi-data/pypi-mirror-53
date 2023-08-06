"""Page objects for Twitter views accessible without authentication."""

from __future__ import annotations

import re
from datetime import datetime

import log
from splinter import Browser

from .base import View


class Public(View):  # pylint: disable=abstract-method
    def __init__(self, browser: Browser, *, username: str, goto: bool = True):
        self.username = username
        super().__init__(browser, goto=goto)

    @property
    def _active(self) -> bool:
        return self._browser.url == self._url and bool(
            self._browser.find_by_id("signin-link")
        )


class Profile(Public):
    @property
    def _url(self) -> str:
        return f"https://twitter.com/{self.username}"

    def _goto(self) -> Profile:
        self._browser.visit(self._url)
        return self

    @property
    def tweets(self) -> int:
        match = re.search(r"([\d,]+) Tweets", self._browser.html)
        assert match
        text = match.group(1)
        log.debug(f"Tweets count: {text!r}")
        return int(text.replace(",", ""))

    @property
    def following(self) -> int:
        match = re.search(r"([\d,]+) Following", self._browser.html)
        assert match
        text = match.group(1)
        log.debug(f"Following count: {text!r}")
        return int(text.replace(",", ""))

    @property
    def followers(self) -> int:
        match = re.search(r"([\d,]+) Followers", self._browser.html)
        assert match
        text = match.group(1)
        log.debug(f"Followers count: {text!r}")
        return int(text.replace(",", ""))

    @property
    def likes(self) -> int:
        match = re.search(r"([\d,]+) Likes", self._browser.html)
        assert match
        text = match.group(1)
        log.debug(f"Likes count: {text!r}")
        return int(text.replace(",", ""))

    @property
    def joined(self) -> datetime:
        span = self._browser.find_by_css(".ProfileHeaderCard-joinDateText").first
        return datetime.strptime(span["title"], "%I:%M %p - %d %b %Y")
