"""Page objects for Twitter views that require authentication."""

from __future__ import annotations

import re
import time

import log
from splinter import Browser
from splinter.driver import ElementAPI

from ..models import Credentials
from .base import View


class Private(View):  # pylint: disable=abstract-method
    def __init__(
        self,
        browser: Browser,
        *,
        username: str,
        credentials: Credentials,
        goto: bool = True,
    ):
        self.username = username
        self._credentials = credentials
        super().__init__(browser, goto=goto)

    @property
    def _active(self) -> bool:
        return self._browser.url == self._url and not bool(self._signin_link)

    @property
    def _signin_link(self) -> ElementAPI:
        return self._browser.find_by_id("signin-link")


class Profile(Private):
    @property
    def _url(self) -> str:
        return f"https://twitter.com/{self.username}"

    def _goto(self) -> Profile:
        log.info(f"Visiting {self._url}")
        self._browser.visit(self._url)
        time.sleep(0.5)

        if not bool(self._signin_link):
            log.info(f"Assuming {self._credentials} is already logged in")
            return self

        if not self._browser.is_text_present("Have an account?"):
            log.info("Expanding login form")
            self._signin_link.first.click()
            time.sleep(0.5)

        log.info(f"Submitting credentials for {self._credentials}")
        self._browser.fill("session[username_or_email]", self._credentials.username)
        self._browser.fill("session[password]", self._credentials.password)
        self._browser.find_by_css(".js-submit").click()

        return self

    @property
    def tweets(self) -> int:
        match = re.search(r"([\d.]+)(K?) Tweets", self._browser.html)
        assert match
        count = float(match.group(1))
        if match.group(2):
            count *= 1000
        return int(count)

    def more(self) -> ProfileMore:
        self._browser.find_by_css('[aria-label="More"]').click()
        return ProfileMore(
            self._browser,
            username=self.username,
            credentials=self._credentials,
            goto=False,
        )


class ProfileMore(Private):
    @property
    def _url(self) -> str:
        return f"https://twitter.com/{self.username}"

    @property
    def _active(self) -> bool:
        return self._browser.url == self._url and self._browser.is_text_present(
            "Add/remove from Lists"
        )

    def _goto(self) -> ProfileMore:
        return Profile(
            self._browser, username=self.username, credentials=self._credentials
        ).more()

    def block(self) -> ProfileBlock:
        self._browser.find_by_text(f"Block @{self.username}").click()
        return ProfileBlock(
            self._browser,
            username=self.username,
            credentials=self._credentials,
            goto=False,
        )


class ProfileBlock(Private):
    @property
    def _url(self) -> str:
        return f"https://twitter.com/{self.username}"

    @property
    def _active(self) -> bool:
        return self._browser.url == self._url and self._browser.is_text_present(
            "They will not be able to follow you"
        )

    def _goto(self) -> ProfileBlock:
        return ProfileMore(
            self._browser, username=self.username, credentials=self._credentials
        ).block()

    def cancel(self):
        self._browser.find_by_text("Cancel").click()
        return Profile(
            self._browser,
            username=self.username,
            credentials=self._credentials,
            goto=False,
        )

    def block(self):
        self._browser.find_by_text("Block").click()
        return Profile(
            self._browser,
            username=self.username,
            credentials=self._credentials,
            goto=False,
        )
