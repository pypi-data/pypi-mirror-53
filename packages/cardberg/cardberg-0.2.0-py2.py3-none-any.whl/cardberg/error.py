# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


class CardbergError(Exception):
    def __init__(self, message=None, http_body=None):
        super(CardbergError, self).__init__(message)

        self.http_body = http_body


class APIError(CardbergError):
    pass


class APIConnectionError(APIError):
    pass
