# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import cardberg
import requests

from decimal import Decimal
from numbers import Number
from .error import APIConnectionError, APIError
from .version import VERSION


class Requestor:
    def request(self, method, data={}, params=[]):
        if (
            not isinstance(cardberg.api_credentials, tuple)
            or len(cardberg.api_credentials) != 2
        ):
            raise APIError(
                "Invalid credentials to Cardberg service provided (expected two-part "
                "tuple with `partner_id` and `shared_secret`)."
            )

        if method not in ["card_info", "create_transaction"]:
            raise APIError(
                "Unsupported Cardberg method `%s`" "requested." % method
            )

        url = "%s%s/%s" % (
            cardberg.CARDBERG_API_ENDPOINT,
            cardberg.api_credentials[0],
            method,
        )

        params.append(("api_key", cardberg.api_credentials[1]))

        headers = {
            "User-Agent": "cardberg-python/" + VERSION,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            if data:
                response = requests.post(
                    url=url,
                    headers=headers,
                    data=data,
                    params=params,
                    timeout=cardberg.timeout,
                )
            else:
                response = requests.get(
                    url=url,
                    headers=headers,
                    params=params,
                    timeout=cardberg.timeout,
                )
        except Exception as e:
            self._handle_request_error(e)

        data = response.json()

        try:
            result = data["result"]
            content = data["data"]
        except (KeyError, TypeError):
            raise APIError(
                "Invalid response object from API: %s" % (response.text),
                response.text,
            )

        if result is not True:
            raise APIError(
                "Invalid response object from API: %s" % data, response.text
            )

        return content

    def _handle_request_error(self, e):
        if isinstance(e, requests.exceptions.RequestException):
            err = "%s: %s" % (type(e).__name__, str(e))
        else:
            err = "A %s was raised" % (type(e).__name__,)

            if str(e):
                err += " with error message %s" % (str(e),)
            else:
                err += " with no error message"

        msg = "Network error: %s" % (err,)

        raise APIConnectionError(msg)


class Card:
    STATUS_ACTIVE = "active"
    STATUS_BLOCKED = "blocked"
    STATUS_EXPIRED = "expired"

    TRANSACTION_CREDITS = "credits"
    TRANSACTION_POINTS = "points"

    def __init__(self, data={}):
        self.id = data.get("id")
        self.name = data.get("name")
        self.surname = data.get("surname")

        status = int(data.get("status", 0))

        if status == 1:
            self.status = self.STATUS_ACTIVE
        elif status == -1:
            self.status = self.STATUS_EXPIRED
        else:
            self.status = self.STATUS_BLOCKED

        self.points = Decimal(data.get("points", 0)).quantize(Decimal(".01"))
        self.credits = Decimal(data.get("credits", 0)).quantize(Decimal(".01"))

    @classmethod
    def get(self, card_id):
        client = Requestor()
        return Card(client.request("card_info", params=[("id", card_id)]))

    def create_transaction(self, transaction_type, value, order_id=None):
        if self.status != Card.STATUS_ACTIVE:
            raise APIError(
                "Expired or blocked card cannot be used in transactions"
            )

        if transaction_type not in [
            self.TRANSACTION_CREDITS,
            self.TRANSACTION_POINTS,
        ]:
            raise APIError(
                'The type of the transaction has to be either "%s" (or '
                '`Card.TRANSACTION_CREDITS`) or "%s" (or '
                "`Card.TRANSACTION_POINTS`)"
                % (self.TRANSACTION_CREDITS, self.TRANSACTION_POINTS)
            )

        if not isinstance(value, Number):
            raise APIError(
                "The value of the transaction has " "to be of type `Decimal`"
            )

        client = Requestor()
        transaction = client.request(
            "create_transaction",
            data={
                "id": self.id,
                "type": transaction_type,
                "value": value,
                "bill_id": order_id if order_id else None,
            },
        )

        try:
            self.credits = Decimal(transaction["credits_after"])
            self.points = Decimal(transaction["points_after"])
        except KeyError:
            pass

        return self
