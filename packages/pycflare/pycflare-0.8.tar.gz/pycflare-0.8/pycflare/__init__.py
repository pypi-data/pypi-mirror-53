# -*- coding: utf-8 -*-
# Copyright (C) 2019 by Bill Schumacher
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby
# granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

import json
import simplejson

import requests

from .account import Account
from .kv import Storage


class CloudFlare(object):
    api_base = "https://api.cloudflare.com/client/v4"
    since_param = "{base}&since={since}"
    until_param = "{base}&until={until}"
    metrics_param = "{base}&metrics={metrics}"
    dimensions_param = "{base}&dimensions={dimensions}"
    sort_param = "{base}&sort={sort}"
    filters_param = "{base}&filters={filters}"
    cursor_param = "{base}&cursor={cursor}"
    prefix_param = "{base}&prefix={prefix}"
    expiration_and_ttl_params = "{base}?expiration={expiration}&expiration_ttl={expiration_ttl}"
    expiration_param = "{base}?expiration={expiration}"
    expiration_ttl_param = "{base}?expiration_ttl={expiration_ttl}"

    def __init__(self, auth_email=None, auth_key=None, enable_redis_compatibility=False):
        self.auth_email = auth_email
        self.auth_key = auth_key
        self.redis_compat = enable_redis_compatibility
        self.storage = Storage(self)
        self.kv = self.storage
        self.accounts = {}

    def register_account(self, account_id, name):
        try:
            self.__getattribute__(name)
            print("Error: Could not register account, name already in use.")
        except AttributeError:
            self.__setattr__(name, Account(identifier=account_id, name=name, cf=self))
            self.accounts[account_id] = self.__getattribute__(name)
            return self.accounts[account_id]

    @staticmethod
    def try_get_request(request_url, headers):
        try:
            response = requests.get(request_url, headers=headers)
            try:
                r = response.json()
                if type(r) == list:
                    return dict(result=r, success=True)
                if not r.get("result"):
                    return dict(result=r, success=True)
                return r
            except json.decoder.JSONDecodeError:
                return dict(result=response.content, success=True)
            except simplejson.errors.JSONDecodeError:
                return dict(result=response.content, success=True)

        except requests.exceptions.ConnectionError as ex:
            return dict(error="Unable to connect to CloudFlare, max retries exceeded.")

    @staticmethod
    def try_put_request(request_url, headers, data):
        try:
            response = requests.put(request_url, headers=headers, data=data)
            return response.json()
        except requests.exceptions.ConnectionError as ex:
            return dict(error="Unable to connect to CloudFlare, max retries exceeded.")

    @staticmethod
    def try_post_request(request_url, headers, data):
        try:
            response = requests.post(request_url, headers=headers, data=data)
            return response.json()
        except requests.exceptions.ConnectionError as ex:
            return dict(error="Unable to connect to CloudFlare, max retries exceeded.")

    @staticmethod
    def try_delete_request(request_url, headers, data=None):
        try:
            response = requests.delete(request_url, headers=headers, data=data)
            return response.json()
        except requests.exceptions.ConnectionError as ex:
            return dict(error="Unable to connect to CloudFlare, max retries exceeded.")

    def get_headers(self):
        return {
            "X-Auth-Email": self.auth_email,
            "X-Auth-Key": self.auth_key,
            "Content-Type": "application/json"
        }

    def apply_filters(self, base_url, since=None, until=None, metrics=None, dimensions=None, sort=None, filters=None,
                      cursor=None, prefix=None, expiration=None, expiration_ttl=None):
        if since is not None:
            base_url = self.since_param.format(base=base_url, since=since)
        if until is not None:
            base_url = self.until_param.format(base=base_url, until=until)
        if metrics is not None:
            base_url = self.metrics_param.format(base=base_url, metrics=metrics)
        if dimensions is not None:
            base_url = self.dimensions_param.format(base=base_url, dimensions=dimensions)
        if sort is not None:
            base_url = self.sort_param.format(base=base_url, sort=sort)
        if filters is not None:
            base_url = self.filters_param.format(base=base_url, filters=filters)
        if cursor is not None:
            base_url = self.cursor_param.format(base=base_url, cursor=cursor)
        if prefix is not None:
            base_url = self.prefix_param.format(base=base_url, prefix=prefix)
        if expiration is not None and expiration_ttl is not None:
            base_url = self.expiration_and_ttl_params.format(
                base=base_url,
                expiration=expiration,
                expiration_ttl=expiration_ttl
            )
        else:
            if expiration is not None:
                base_url = self.expiration_param.format(
                    base=base_url,
                    expiration=expiration
                )
            if expiration_ttl is not None:
                base_url = self.expiration_ttl_param.format(
                    base=base_url,
                    expiration_ttl=expiration_ttl
                )
        return base_url
