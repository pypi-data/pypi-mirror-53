# -*- coding: utf-8 -*-
import abc
import logging
from collections import OrderedDict

import six

from ..ml_base_object_store import _MlBaseObjectStore
from ...connection_mixin import ConnectionMixin
from ...dulwich.objects import hex_to_filename, Blob


@six.add_metaclass(abc.ABCMeta)
class CloudObjectStore(ConnectionMixin, _MlBaseObjectStore):
    def __init__(self, connection):
        _MlBaseObjectStore.__init__(self)
        super(CloudObjectStore, self).__init__(connection)
        self.__volume_id = self._connection.data_volume_config.volume_id
        self.__storage_volume_id = self._connection.data_volume_config.storage_volume_id

    @property
    def _storage_volume_id(self):
        return self.__storage_volume_id

    @classmethod
    def _get_shafile_path(cls, sha):
        # Check from object dir
        return hex_to_filename('objects', sha).replace('\\', '/')

    @abc.abstractmethod
    def _get_loose_object_data(self, object_name, target_fileobj=None, progress_callback=None):
        """
        get the content of object_name
        :param object_name:
        :return:
        """

    def get_source_path(self, metadata):
        sha = metadata['@id']

        if self._connection.data_volume_config.embedded:
            return '%s/%s/%s' % (self._connection.data_volume_config.bucket_name, self.__storage_volume_id, self._get_shafile_path(sha))

        return metadata['@url']

    def _get_loose_object(self, metadata, target_fileobj=None, progress_callback=None):
        logging.debug('get object %s', metadata)

        sha = metadata['@id']

        object_name = self.get_source_path(metadata)

        data = self._get_loose_object_data(object_name, target_fileobj=target_fileobj, progress_callback=progress_callback)

        if target_fileobj is not None:
            return

        blob = Blob()
        blob.set_raw_chunks([data], sha)

        return blob

    @classmethod
    def _get_content_headers(cls, content_type=None):
        headers = OrderedDict()
        if content_type:
            headers['Content-Type'] = content_type

        return headers
