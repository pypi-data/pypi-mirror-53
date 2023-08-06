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


class Account(object):
    def __init__(self, identifier, name, cf):
        self.name = name
        self.identifier = identifier
        self.cf = cf
        self.namespaces = {}

    def create_namespace(self, title):
        """
        Creates a new Namespace.

        :param title: The title or name of your new Namespace.
        :return: Returns a Namespace class or None on failure.
        """

        return self.cf.kv.create_namespace(account_id=self.identifier, title=title)

    def get_namespaces(self, page=1, per_page=20):
        """
        Returns a paginated list of Namespaces for the account.

        :param page: The page you want to view.
        :param per_page: The number of results per page.
        :return: Returns a list of Namespace objects or None on failure.
        """

        return self.cf.kv.get_namespaces(account_id=self.identifier, page=page, per_page=per_page)

    def delete_namespace(self, namespace_id):
        """
        Deletes a Namespace from the account.

        :param namespace_id: The Namespace UUID.
        :return: A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """

        result = self.cf.kv.delete_namespace(account_id=self.identifier, namespace_id=namespace_id)
        if result is not None:
            if result.get('success'):
                try:
                    namespace = self.namespaces.pop(namespace_id)
                    del namespace
                except KeyError:
                    pass
        return result

    def rename_namespace(self, namespace_id, title):
        """
        Rename's a Namespace for the account.

        :param namespace_id: The Namespace UUID.
        :param title: The new title.
        :return: Returns the Namespace or None on failure.
        """

        return self.cf.kv.rename_namespace(account_id=self.identifier, namespace_id=namespace_id, title=title)

    def namespace_keys(self, namespace_id, limit=1000, cursor=None, prefix=None):
        """
        Gets a list of Keys in the Namespace for the account.

        :param namespace_id: The Namespace UUID.
        :param limit: The maximum number of results.
        :param cursor: The key name to start from.
        :param prefix: The prefix to filter by.
        :return: A list of strings or None on failure.
        """

        return self.cf.kv.namespace_keys(account_id=self.identifier, namespace_id=namespace_id, limit=limit,
                                         cursor=cursor, prefix=prefix)

    def get_key(self, namespace_id, key_name):
        """
        Get a key-value pair from the Namespace for the account.

        :param namespace_id: The Namespace UUID.
        :param key_name: The name of the Key in the Namespace.
        :return: A Key object.
        """

        return self.cf.kv.get_key(account_id=self.identifier, namespace_id=namespace_id, key_name=key_name)

    def write_key(self, namespace_id, key_name, data, expiration=None, expiration_ttl=None):
        """
        Creates or updates a Key-Value pair in the Namespace for the account.

        :param namespace_id: The Namespace UUID.
        :param key_name: The name of the Key in the Namespace.
        :param data: The value to write.
        :param expiration: The expiration in time since EPOCH in seconds.
        :param expiration_ttl: The expiration in seconds.
        :return:A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """

        return self.cf.kv.write_key(account_id=self.identifier, namespace_id=namespace_id, key_name=key_name,
                                    data=data, expiration=expiration, expiration_ttl=expiration_ttl)

    def bulk_write(self, namespace_id, data):
        """
        Write multiple Key-Value pairs to the Namespace for the account.

        :param namespace_id: The Namespace UUID.
        :param data: A list Key names, values and options to write.
        Example: [{"key": "hello", "value": "world"}, ...]
        :return:
        """

        return self.cf.kv.bulk_write(account_id=self.identifier, namespace_id=namespace_id, data=data)

    def delete_key(self, namespace_id, key_name):
        """
        Delete a Key-Value pair from the Namespace for the account.

        :param namespace_id: The Namespace UUID.
        :param key_name:
        :return:A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """

        return self.cf.kv.delete_key(account_id=self.identifier, namespace_id=namespace_id, key_name=key_name)

    def bulk_delete(self, namespace_id, keys):
        """
        Delete multiple Key-Value pairs from the Namespace for the account.

        :param namespace_id: The Namespace UUID.
        :param keys: The keys to delete, example ["Hello", "World", ...]
        :return: A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """

        return self.cf.kv.bulk_delete(account_id=self.identifier, namespace_id=namespace_id, keys=keys)

    def query_request_analytics(self, limit=10000, since=None, until=None, metrics=None, dimensions=None,
                                sort=None, filters=None):
        """

        :param limit:
        :param since:
        :param until:
        :param metrics:
        :param dimensions:
        :param sort:
        :param filters:
        :return:
        """

        return self.cf.kv.query_request_analytics(account_id=self.identifier, limit=limit, since=since, until=until,
                                                  metrics=metrics, dimensions=dimensions, sort=sort, filters=filters)

    def query_stored_data_analytics(self, limit=10000, since=None, until=None, metrics=None,
                                    dimensions=None, sort=None, filters=None):
        """

        :param limit:
        :param since:
        :param until:
        :param metrics:
        :param dimensions:
        :param sort:
        :param filters:
        :return:
        """

        return self.cf.kv.query_stored_data_analytics(account_id=self.identifier, limit=limit, since=since, until=until,
                                                      metrics=metrics, dimensions=dimensions, sort=sort,
                                                      filters=filters)
