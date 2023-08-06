# Cardberg Bindings for Python

Python library for [Cardberg](https://www.cardberg.com)'s API to work with gift cards.

The bindings currently allow you to:

1. Get information on a specific card
2. Create a transaction on a specific card

Detailed information of Cardberg's API can be found at [their website](http://loyal.cardberg.com/api/). If you feel like you need covering additional API methods, please open an issue or create a pull request.

## Setup

You can install this package by using `pip`:

	pip install cardberg

If you fancy `pipenv` use:

	pipenv install cardberg

To install from source, run:

	python setup.py install

For the API client to work you would need Python 2.7+ or Python 3.4+.

To install via `requirements` file from your project, add the following for the moment before updating dependencies:

	git+git://github.com/palosopko/cardberg-python.git#egg=cardberg

## Usage

First off, you need to require the library and set the authentication information by providing your user handle and shared secret you got from the provider.

	import cardberg
	cardberg.api_credentials = ("partner_id", "shared_secret")

**Getting card information** is accomplished by calling `cardberg.Card.get()`. The method returns a `Card` object that includes `id`, `name`, `surname`, `status` and available `credits` and `points`. On this `Card` object we may **create a transaction** (whether positive or negative) by calling `create_transaction()` method with transaction type, decimal value of the transaction and optional bill ID for further reference.

Possible transaction types are either "credits" or "points" depending on what budget do we use. If you want to make a debit (for example your user is buying something) then provide a negative value.

Example:

    import cardberg
    from decimal import Decimal

    cardberg.api_credentials = ("partner_id", "shared_secret")

    card = cardberg.Card.get("D1nd17h")

    card.create_transaction(
        cardberg.Card.TRANSACTION_CREDITS,
        Decimal("-1.00")
    )

## Contributing

1.  Check for open issues or open a new issue for a feature request or a bug.
2.  Fork the repository and make your changes to the master branch (or branch off of it).
3.  Send a pull request.

## Development

Run all tests on all supported Python versions:

	make test

Run the linter with:

	make lint

The client library uses Black for code formatting. Code must be formatted with Black before PRs are submitted. Run the formatter with:

	make fmt

## Changelog

### v0.2.0: 03/10/2019

Python 3 compatibility, code formatting covered by Black and various small fixes and formal changes to make everything better.

### v0.1.1: 21/03/2016

Added rounding to two decimal places on credits and points returned from Cardberg's API.

### v0.1.0: 14/03/2016

Initial version with support for `card_info` and `create_transaction` API methods.
