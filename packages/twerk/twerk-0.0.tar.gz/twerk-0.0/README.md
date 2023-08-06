# Twerk

This is a Selenium-powered tool to browse Twitter and automatically block fake accounts.

This project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).

[![Unix Build Status](https://img.shields.io/travis/jacebrowning/twerk/master.svg?label=unix)](https://travis-ci.org/jacebrowning/twerk)
[![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/twerk/master.svg?label=window)](https://ci.appveyor.com/project/jacebrowning/twerk)
[![Coverage Status](https://img.shields.io/coveralls/jacebrowning/twerk/master.svg)](https://coveralls.io/r/jacebrowning/twerk)
[![PyPI Version](https://img.shields.io/pypi/v/twerk.svg)](https://pypi.org/project/twerk)
[![PyPI License](https://img.shields.io/pypi/l/twerk.svg)](https://pypi.org/project/twerk)

# Setup

## Requirements

* Python 3.7+
* Poetry

# Usage

To run this program from source:

```text
$ git clone https://github.com/jacebrowning/twerk
$ cd twerk
$ poetry install
$ poetry run twerk
```

# Configuration

The `$TWITTER_USERNAME` and `$TWITTER_PASSWORD` environment variables can be set to avoid manually typing account credentials.

The `$TWITTER_SEED_USERNAME` can be set to override the default starting account when searching for fake accounts.

---

> **Disclaimer**: I am by no means responsible for any usage of this tool. Please consult the [full license](https://github.com/jacebrowning/twerk/blob/master/LICENSE.md) for details.
