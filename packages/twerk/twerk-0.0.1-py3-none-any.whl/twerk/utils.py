import os
from getpass import getpass

import log
from splinter import Browser
from webdriver_manager.firefox import GeckoDriverManager

from .models import Credentials


def get_browser() -> Browser:
    try:
        return Browser("firefox", wait_time=1.0)
    except Exception as e:  # pylint: disable=broad-except
        log.debug(str(e))
        if "geckodriver" in str(e):
            path = GeckoDriverManager().install()
            return Browser("firefox", wait_time=1.0, executable_path=path)
        raise e from None


def get_credentials() -> Credentials:
    username = os.getenv("TWITTER_USERNAME") or input("Twitter username: ")
    password = os.getenv("TWITTER_PASSWORD") or getpass("Twitter password: ")
    return Credentials(username, password)


def get_seed_username() -> str:
    return os.getenv("TWITTER_SEED_USERNAME", "realDonaldTrump")
