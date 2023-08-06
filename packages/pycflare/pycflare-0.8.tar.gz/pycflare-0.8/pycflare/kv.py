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


class Namespace(object):
    def __init__(self, account_id, id=None, title=None, cf=None, account=None, *args, **kwargs):
        self.id = id
        self.title = title
        self.cf = cf
        if account is not None:
            self.account_id = account.identifier
            self.account = account
        else:
            self.account_id = account_id
            account = self.cf.accounts.get(account_id)
            if account is None:
                from .account import Account
                account = Account(identifier=account_id, name=account_id, cf=cf)
                self.cf.accounts[account_id] = account
                self.account = self.cf.accounts[account_id]
            else:
                self.account = account
        if self.account.namespaces.get(self.id) is None:
            self.account.namespaces[self.id] = self

    def __repr__(self):
        return "Namespace(id='{id}', title='{title}')".format(id=self.id, title=self.title)

    def delete_namespace(self):
        """
        Deletes a Namespace from the account.

        :return: A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """

        result = self.account.delete_namespace(namespace_id=self.id)
        if result is not None:
            if result.get('success'):
                try:
                    self.account.namespaces.pop(self.id)
                    del self
                except KeyError:
                    pass
        return result

    # It is pretty ambiguous on what would be deleted, for the sake of preventing a critical mistake this function shall
    # not be implemented. Although, perhaps the absence of a key_name parameter makes that clear. Best to avoid for now.
    #
    # def delete(self):
    #     return self.delete_namespace()

    def namespace_keys(self, limit=1000, cursor=None, prefix=None):
        """
        Gets a list of Keys in the Namespace for the account.

        :param limit: The maximum number of results.
        :param cursor: The key name to start from.
        :param prefix: The prefix to filter by.
        :return: A list of strings or None on failure.
        """

        return self.account.namespace_keys(namespace_id=self.id, limit=limit, cursor=cursor, prefix=prefix)

    def keys(self, limit=1000, cursor=None, prefix=None):
        """
        Gets a list of Keys in the Namespace for the account.

        :param limit: The maximum number of results.
        :param cursor: The key name to start from.
        :param prefix: The prefix to filter by.
        :return: A list of strings or None on failure.
        """

        return self.namespace_keys(limit=limit, cursor=cursor, prefix=prefix)

    def rename_namespace(self, title):
        """
        Rename's a Namespace for the account.

        :param title: The new title.
        :return: Returns the Namespace or None on failure.
        """

        result = self.account.rename_namespace(namespace_id=self.id, title=title)
        if result is not None:
            self.title = title
        return result

    def rename(self, title):
        """
        Rename's a Namespace for the account.

        :param title: The new title.
        :return: Returns the Namespace or None on failure.
        """

        return self.rename_namespace(title=title)

    def get_key(self, key_name):
        """
        Get a key-value pair from the Namespace for the account.

        :param key_name: The name of the Key in the Namespace.
        :return: A Key object.
        """

        return self.account.get_key(namespace_id=self.id, key_name=key_name)

    def get(self, key_name):
        """
        Get a key-value pair from the Namespace for the account.

        :param key_name: The name of the Key in the Namespace.
        :return: A Key object.
        """

        return self.get_key(key_name=key_name)

    def write_key(self, key_name, data, expiration=None, expiration_ttl=None):
        """
        Creates or updates a Key-Value pair in the Namespace for the account.

        :param key_name: The name of the Key in the Namespace.
        :param data: The value to write.
        :param expiration: The expiration in time since EPOCH in seconds.
        :param expiration_ttl: The expiration in seconds.
        :return:A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """

        return self.account.write_key(namespace_id=self.id, key_name=key_name, data=data, expiration=expiration,
                                      expiration_ttl=expiration_ttl)

    def write(self, key_name, data, expiration=None, expiration_ttl=None):
        """
        Creates or updates a Key-Value pair in the Namespace for the account.

        :param key_name: The name of the Key in the Namespace.
        :param data: The value to write.
        :param expiration: The expiration in time since EPOCH in seconds.
        :param expiration_ttl: The expiration in seconds.
        :return:A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """

        return self.write_key(key_name=key_name, data=data, expiration=expiration, expiration_ttl=expiration_ttl)

    def bulk_write(self, data):
        """
        Write multiple Key-Value pairs to the Namespace for the account.

        :param data: A list Key names, values and options to write.
        Example: [{"key": "hello", "value": "world"}, ...]
        :return:
        """

        return self.account.bulk_write(namespace_id=self.id, data=data)

    def delete_key(self, key_name):
        """
        Delete a Key-Value pair from the Namespace for the account.

        :param key_name:
        :return:A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """

        return self.account.delete_key(namespace_id=self.id, key_name=key_name)

    def bulk_delete(self, keys):
        """
        Delete multiple Key-Value pairs from the Namespace for the account.

        :param keys: The keys to delete, example ["Hello", "World", ...]
        :return: A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """

        return self.account.bulk_delete(namespace_id=self.id, keys=keys)


class RedisCompatibilityNamespace(Namespace):
    """
        A helper class that provides basic redis-like functionality for easy transitioning.

    """
    def sadd(self, key, value):
        data = self.get_key(key)
        if data is None:
            the_set = set()
        else:
            try:
                the_set = set(data.value)
            except TypeError:
                return None
        the_set.add(value)
        self.write_key(key, json.dumps(list(the_set)))
        return the_set

    def srem(self, key, value):
        data = self.get_key(key)
        if data is None:
            return None
        try:
            the_set = set(data.value)
        except TypeError:
            return None
        try:
            the_set.remove(value)
            self.write_key(key, json.dumps(list(the_set)))
        except KeyError:
            return None
        return the_set

    def smembers(self, key):
        data = self.get_key(key)
        if data is None:
            return []
        try:
            the_set = set(data.value)
        except TypeError:
            return None
        return list(the_set)

    def sismember(self, key, value):
        data = self.get_key(key)
        if data is None:
            return None
        try:
            the_set = set(data.value)
        except TypeError:
            return None
        return value in the_set

    def hset(self, key, hash_key, value):
        data = self.get_key(key)
        if data is None:
            data = {hash_key: value}
            self.write_key(key, json.dumps(data))
            return data
        if type(data.value) != dict:
            return None
        data.value[hash_key] = value
        self.write_key(key, json.dumps(data.value))
        return data.value

    def hdel(self, key, value):
        data = self.get_key(key)
        if data is None:
            return None
        try:
            data.value.pop(value)
            self.write_key(key, json.dumps(data.value))
            return data.value
        except KeyError:
            return data.value
        except AttributeError:
            return None
        return None

    def hmset(self, key, values):
        data = self.get_key(key)
        if data is None:
            self.write_key(key, json.dumps(values))
            return values
        try:
            data.value.update(values)
            self.write_key(key, json.dumps(data.value))
            return data.value
        except TypeError:
            pass
        except AttributeError:
            return None
        return None

    def hgetall(self, key):
        data = self.get_key(key)
        if data is not None:
            return data.value
        return None

    def hget(self, key, value):
        data = self.get_key(key)
        if data is None:
            return None
        try:
            return data.value.get(value)
        except AttributeError:
            return None

    def set(self, key, value):
        self.write_key(key, value)
        return value

    def get(self, key):
        data = self.get_key(key)
        return data.value

    def delete(self, key):
        self.delete_key(key)


class Key(object):
    def __init__(self, account_id, namespace_id, name=None, value=None, account=None, namespace=None, cf=None,
                 *args, **kwargs):
        self.name = name
        self.value = value
        self.cf = cf

        if account is not None:
            self.account_id = account.identifier
            self.account = account
        else:
            self.account_id = account_id
            account = self.cf.accounts.get(account_id)
            if account is None:
                from .account import Account
                account = Account(identifier=account_id, name=account_id, cf=cf)
                self.cf.accounts[account_id] = account
                self.account = self.cf.accounts[account_id]
            else:
                self.account = account
        if namespace is not None:
            self.namespace_id = namespace.id
            self.namespace = namespace
        else:
            self.namespace_id = namespace_id
            namespace = self.account.namespaces.get(namespace_id)
            if namespace is None:
                namespace = self.cf.kv.namespace_class(self.account_id, identifier=namespace_id,
                                                       title=namespace_id, cf=cf, account=self.account)
                self.account.namespaces[namespace_id] = namespace
                self.namespace = self.account.namespaces[namespace_id]
            else:
                self.namespace = namespace

    def __repr__(self):
        return "Key(name='{name}', value='{value}')".format(name=self.name, value=self.value)

    def __str__(self):
        return "{data}".format(data=self.value)

    def write_key(self, data, expiration=None, expiration_ttl=None):
        """
        Creates or updates a Key-Value pair in the Namespace for the account.

        :param data: The value to write.
        :param expiration: The expiration in time since EPOCH in seconds.
        :param expiration_ttl: The expiration in seconds.
        :return:A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """
        result = self.namespace.write_key(data=data, key_name=self.name, expiration=expiration,
                                          expiration_ttl=expiration_ttl)

        if result is not None:
            if result.get("success"):
                self.value = data
        return result

    def write(self, data, expiration=None, expiration_ttl=None):
        """
        Creates or updates a Key-Value pair in the Namespace for the account.

        :param data: The value to write.
        :param expiration: The expiration in time since EPOCH in seconds.
        :param expiration_ttl: The expiration in seconds.
        :return:A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """

        return self.write_key(data=data, expiration=expiration, expiration_ttl=expiration_ttl)

    def delete_key(self):
        """
        Delete a Key-Value pair from the Namespace for the account.

        :return:A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """

        result = self.namespace.delete_key(key_name=self.name)
        if result is not None:
            if result.get("success"):
                del self
        return result

    def delete(self):
        """
        Delete a Key-Value pair from the Namespace for the account.

        :return:A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """

        return self.delete_key()


class Storage(object):
    """
        CloudFlare Workers Key-Value storage module.

        Provides methods to interact with the CloudFlare Workers KV API.
    """
    create_namespace_url = "{base}/accounts/{account_id}/storage/kv/namespaces"
    get_namespaces_url = "{base}/accounts/{account_id}/storage/kv/namespaces?page={page}&per_page={per_page}"
    delete_namespace_url = "{base}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}"
    namespace_keys_url = "{base}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/keys?limit={limit}"
    rename_namespace_url = "{base}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}"
    get_key_url = "{base}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key_name}"
    write_key_url = "{base}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key_name}"
    bulk_write_url = "{base}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/bulk"
    bulk_delete_url = "{base}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/bulk"
    query_request_analytics_url = "{base}/accounts/{account_id}/storage/analytics?limit={limit}"

    def __init__(self, cf):
        """
        Initializes the CloudFlare Workers Key-Value storage module.

        This class should not need to be initialized manually.

        :param cf: The CloudFlare instance, stores commonly used methods and data.
        """
        self.cf = cf
        if cf.redis_compat:
            self.namespace_class = RedisCompatibilityNamespace
        else:
            self.namespace_class = Namespace

    def create_namespace(self, account_id, title):
        """
        Creates a new Namespace.

        :param account_id: Your CloudFlare account ID.
        :param title: The title or name of your new Namespace.
        :return: Returns a Namespace class or None on failure.
        """
        request_url = self.create_namespace_url.format(base=self.cf.api_base, account_id=account_id)
        headers = self.cf.get_headers()
        response = self.cf.try_post_request(request_url, headers=headers, data=json.dumps(dict(title=title)))
        result = response.get("result")
        if result is not None:
            return self.namespace_class(account_id, cf=self.cf, **result)
        return None

    def get_namespaces(self, account_id, page=1, per_page=20):
        """
        Returns a paginated list of Namespaces for the account.

        :param account_id: Your CloudFlare account ID.
        :param page: The page you want to view.
        :param per_page: The number of results per page.
        :return: Returns a list of Namespace objects or None on failure.
        """
        request_url = self.get_namespaces_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            page=page,
            per_page=per_page
        )
        headers = self.cf.get_headers()
        response = self.cf.try_get_request(request_url, headers=headers)
        results = response.get("result")
        if results is not None:
            if type(results) == list:
                namespaces = []
                for result in results:
                    namespaces.append(self.namespace_class(account_id, cf=self.cf, **result))
                return namespaces
            return None
        return None

    def delete_namespace(self, account_id, namespace_id):
        """
        Deletes a Namespace from the account.

        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :return: A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """
        request_url = self.delete_namespace_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id
        )
        headers = self.cf.get_headers()
        result = self.cf.try_delete_request(request_url, headers=headers)
        if result is not None:
            if result.get('success'):
                account = self.cf.accounts.get(account_id)
                if account:
                    namespace = account.namespaces.pop(namespace_id)
                    del namespace
        return result

    def rename_namespace(self, account_id, namespace_id, title):
        """
        Rename's a Namespace for the account.

        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :param title: The new title.
        :return: Returns the Namespace or None on failure.
        """
        request_url = self.rename_namespace_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id
        )
        headers = self.cf.get_headers()
        result = self.cf.try_put_request(request_url, headers=headers, data=json.dumps(dict(title=title)))
        if result is not None:
            if result.get('success'):
                account = self.cf.accounts.get(account_id)
                if account:
                    namespace = account.namespaces.get(namespace_id)
                    if namespace is not None:
                        namespace.title = title
        return result

    def namespace_keys(self, account_id, namespace_id, limit=1000, cursor=None, prefix=None):
        """
        Gets a list of Keys in the Namespace for the account.

        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :param limit: The maximum number of results.
        :param cursor: The key name to start from.
        :param prefix: The prefix to filter by.
        :return: A list of strings or None on failure.
        """
        request_url = self.namespace_keys_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id,
            limit=limit
        )
        self.cf.apply_filters(request_url, cursor=cursor, prefix=prefix)
        response = self.cf.try_get_request(request_url, headers=self.cf.get_headers())
        results = response.get("result")
        if results is not None:
            if type(results) == list:
                keys = []
                for result in results:
                    keys.append(result.get("name"))
                return keys
            return None
        return None

    def get_key(self, account_id, namespace_id, key_name):
        """
        Get a key-value pair from the Namespace for the account.

        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :param key_name: The name of the Key in the Namespace.
        :return: A Key object.
        """
        request_url = self.get_key_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id,
            key_name=key_name)
        headers = self.cf.get_headers()
        response = self.cf.try_get_request(request_url, headers=headers)
        result = response.get("result")
        if result is not None:
            try:
                return Key(account_id, namespace_id, cf=self.cf, name=key_name, value=json.loads(result))
            except json.decoder.JSONDecodeError:
                return Key(account_id, namespace_id, cf=self.cf, name=key_name, value=result)
            except TypeError:
                if type(result) == dict:
                    success = result.get("success")
                    if success is not None:
                        if not success:
                            return None
                return Key(account_id, namespace_id, cf=self.cf, name=key_name, value=result)
        return None

    def write_key(self, account_id, namespace_id, key_name, data, expiration=None, expiration_ttl=None):
        """
        Creates or updates a Key-Value pair in the Namespace for the account.

        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :param key_name: The name of the Key in the Namespace.
        :param data: The value to write.
        :param expiration: The expiration in time since EPOCH in seconds.
        :param expiration_ttl: The expiration in seconds.
        :return:A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """
        request_url = self.write_key_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id,
            key_name=key_name)
        request_url = self.cf.apply_filters(request_url, expiration=expiration, expiration_ttl=expiration_ttl)
        headers = self.cf.get_headers()
        headers["Content-Type"] = "text/plain"
        return self.cf.try_put_request(request_url, headers=headers, data=data)

    def bulk_write(self, account_id, namespace_id, data):
        """
        Write multiple Key-Value pairs to the Namespace for the account.
        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :param data: A list Key names, values and options to write.
        Example: [{"key": "hello", "value": "world"}, ...]
        :return:
        """
        request_url = self.bulk_write_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id)
        headers = self.cf.get_headers()
        try:
            return self.cf.try_put_request(request_url, headers=headers, data=json.dumps(data))
        except json.decoder.JSONDecodeError:
            return None

    def delete_key(self, account_id, namespace_id, key_name):
        """
        Delete a Key-Value pair from the Namespace for the account.

        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :param key_name:
        :return:A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """
        request_url = self.get_key_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id,
            key_name=key_name)
        headers = self.cf.get_headers()
        return self.cf.try_delete_request(request_url, headers=headers)

    def bulk_delete(self, account_id, namespace_id, keys):
        """
        Delete multiple Key-Value pairs from the Namespace for the account.

        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :param keys: The keys to delete, example ["Hello", "World", ...]
        :return: A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """
        request_url = self.bulk_delete_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id)
        headers = self.cf.get_headers()
        try:
            return self.cf.try_delete_request(request_url, headers=headers, data=json.dumps(keys))
        except json.decoder.JSONDecodeError:
            return None

    def query_request_analytics(self, account_id, limit=10000, since=None, until=None, metrics=None, dimensions=None,
                                sort=None, filters=None):
        """

        :param account_id:
        :param limit:
        :param since:
        :param until:
        :param metrics:
        :param dimensions:
        :param sort:
        :param filters:
        :return:
        """
        request_url = self.query_request_analytics_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            limit=limit
        )
        request_url = self.cf.apply_filters(request_url, since=since, until=until, metrics=metrics,
                                            dimensions=dimensions, sort=sort, filters=filters)
        return self.cf.try_get_request(request_url, headers=self.cf.get_headers())

    def query_stored_data_analytics(self, account_id, limit=10000, since=None, until=None, metrics=None,
                                    dimensions=None, sort=None, filters=None):
        """

        :param account_id:
        :param limit:
        :param since:
        :param until:
        :param metrics:
        :param dimensions:
        :param sort:
        :param filters:
        :return:
        """
        request_url = "{base}/accounts/{account_id}/storage/analytics/stored?limit={limit}".format(
            base=self.cf.api_base,
            account_id=account_id,
            limit=limit
        )
        request_url = self.cf.apply_filters(request_url, since=since, until=until, metrics=metrics,
                                            dimensions=dimensions, sort=sort, filters=filters)
        return self.cf.try_get_request(request_url, headers=self.cf.get_headers())
