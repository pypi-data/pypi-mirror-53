"""A sample CLI."""

import click
import log
from splinter import Browser

from .models import Account, Blocklist, Credentials
from .utils import get_browser
from .views.private import Profile as PrivateProfile
from .views.public import Profile as PublicProfile


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main():
    pass


@main.command(help="Verify browser automation is working.")
@click.option(
    "--username",
    envvar="TWITTER_USERNAME",
    prompt="Twitter username",
    help="Username of Twitter account to automate.",
)
@click.option(
    "--password",
    envvar="TWITTER_PASSWORD",
    prompt="Twitter password",
    hide_input=True,
    help="Password of twitter account to automate.",
)
@click.option("--debug", is_flag=True, help="Start debugger on exceptions.")
def check(username: str, password: str, debug: bool):
    log.init(debug=debug)
    log.silence("datafiles")

    with get_browser() as browser:
        try:
            run_check(browser, username, password)
        except Exception as e:  # pylint: disable=broad-except
            if debug:
                import ipdb  # pylint: disable=import-outside-toplevel

                log.exception(e)

                ipdb.post_mortem()
            else:
                raise e from None


def run_check(browser: Browser, username: str, password):
    credentials = Credentials(username, password)
    profile = PrivateProfile(browser, username=username, credentials=credentials)
    account = Account(username, tweets=profile.tweets)
    click.echo(f"{account} has tweeted {account.tweets} times")


@main.command(help="Crawl for bots starting from seed account.")
@click.argument("username", envvar="TWITTER_SEED_USERNAME")
def crawl(username: str):
    log.init()
    log.silence("datafiles")

    with get_browser() as browser:
        profile = PublicProfile(browser, username=username)
        account = Account.from_profile(profile)
        Blocklist().bots.append(account)  # pylint: disable=no-member


if __name__ == "__main__":  # pragma: no cover
    main()
