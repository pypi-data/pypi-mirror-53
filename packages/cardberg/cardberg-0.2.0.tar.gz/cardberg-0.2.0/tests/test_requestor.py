# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import pytest
import cardberg

from cardberg.resource import Requestor


class TestRequestor(object):
    def test_invalid_requestor_instantiation_with_no_credentials(self):
        with pytest.raises(cardberg.APIError):
            cardberg.api_credentials = None
            client = Requestor()
            client.request("card_info", params=[("id", "D123abc")])

    def test_invalid_auth_instantiation_with_empty_credentials(self):
        with pytest.raises(cardberg.APIError):
            cardberg.api_credentials = ()
            client = Requestor()
            client.request("card_info", params=[("id", "D123abc")])

    def test_invalid_auth_instantiation_with_incomplete_credentials(self):
        with pytest.raises(cardberg.APIError):
            cardberg.api_credentials = ("partner_id",)
            client = Requestor()
            client.request("invalid")

    def test_unsupported_request_method(self):
        with pytest.raises(cardberg.APIError):
            cardberg.api_credentials = ("partner_id", "shared_secret")
            client = Requestor()
            client.request("ping")
