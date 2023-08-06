# flake8-bandit
[![Build Status](https://travis-ci.org/tylerwince/flake8-bandit.svg?branch=master)](https://travis-ci.org/tylerwince/flake8-bandit)

Automated security testing built right into your workflow!

You already use flake8 to lint all your code for errors, ensure docstrings are formatted correctly, sort your imports correctly, and much more... so why not ensure you are writing secure code while you're at it? If you already have flake8 installed all it takes is `pip install flake8-bandit`.

## How's it work?

We use the [bandit](https://github.com/PyCQA/bandit) package from [PyCQA](http://meta.pycqa.org/en/latest/) for all the security testing.
