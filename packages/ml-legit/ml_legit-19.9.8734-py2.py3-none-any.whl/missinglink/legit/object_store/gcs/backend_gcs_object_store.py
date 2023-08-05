# -*- coding: utf-8 -*-
from collections import OrderedDict

from missinglink.core.api import ApiCaller, default_api_retry

from missinglink.legit.gcs_utils import Downloader, Uploader
from ...backend_mixin import BackendMixin
from .gcs_object_store import GCSObjectStore, CloudObjectStore


class BackendGCSSignedUrlService(BackendMixin):
    def __init__(self, connection, config, session):
        super(BackendGCSSignedUrlService, self).__init__(connection, config, session)

    def get_signed_urls(self, methods, object_names, content_type=None, **kwargs):
        headers = []
        for key in sorted(kwargs.keys()):
            val = kwargs[key]
            headers.append('%s:%s' % (key, val))

        msg = {
            'methods': methods,
            'paths': object_names,
        }

        if headers:
            msg['headers'] = headers

        if content_type:
            msg['content_type'] = content_type

        url = 'data_volumes/{volume_id}/gcs_urls'.format(volume_id=self._volume_id)

        result = ApiCaller.call(self._config, self._session, 'post', url, msg, retry=default_api_retry())
        res = {method: result.get(method.lower(), []) for method in methods}

        return res


class BackendGCSObjectStore(BackendMixin, CloudObjectStore):
    def __init__(self, connection, config, session):
        super(BackendGCSObjectStore, self).__init__(connection, config, session)
        self._signed_url_service = BackendGCSSignedUrlService(connection, config, session)

    def __iter__(self):
        return super(BackendGCSObjectStore, self).__iter__()

    def get_source_path(self, metadata):
        sha = metadata['@id']

        # under backend we don't have bucket name as everything saved with our bucket
        if self._connection.data_volume_config.embedded:
            return '%s/%s' % (self._storage_volume_id, self._get_shafile_path(sha))

        raise Exception("Secure Bucket doesn't support linked mode")

    def close(self):
        super(BackendGCSObjectStore, self).close()

    def add_objects_async(self, objects, callback=None, progress_callback=None):
        grouped_files = self.__group_files_by_meta(objects)
        for content_type in grouped_files:
            grouped_objects = grouped_files[content_type]
            self.__upload_http_batch_async(content_type, grouped_objects, callback, progress_callback=progress_callback)

    def _get_loose_object_data(self, object_name, target_fileobj=None, progress_callback=None):
        signed_urls = self._signed_url_service.get_signed_urls(['GET'], [object_name])
        url = signed_urls['GET'][0]

        return Downloader.download_http(url, target_fileobj=target_fileobj, progress_callback=progress_callback)

    @classmethod
    def __group_files_by_meta(cls, objects):
        content_type_grouped = OrderedDict()
        for obj in objects:
            if obj.content_type not in content_type_grouped:
                content_type_grouped[obj.content_type] = []

            content_type_grouped[obj.content_type].append(obj)

        return content_type_grouped

    def __get_urls_for_paths(self, paths, content_type, headers):
        urls = self._signed_url_service.get_signed_urls(['HEAD', 'PUT'], paths, content_type, **headers)
        head_urls = urls['HEAD']
        put_urls = urls['PUT']
        return head_urls, put_urls

    def __gen_upload_http_args(self, obj, put_url, head_url, progress_callback):
        content_type = obj.content_type
        headers = self._get_content_headers(content_type)

        return head_url, put_url, obj.full_path, headers, progress_callback

    @staticmethod
    def _noop(*args, **kwargs):
        pass

    def __upload_http_async(self, obj, put_url, head_url=None, callback=None, progress_callback=None):
        # noinspection PyUnusedLocal
        def on_finish(result):
            callback(obj)

        args = self.__gen_upload_http_args(obj, put_url, head_url, progress_callback)

        actual_callback = on_finish if callback else None

        if obj.skip_upload:
            self._multi_process_control.execute(self._noop, args=(), callback=actual_callback)
            return

        self._multi_process_control.execute(Uploader.upload_http, args=args, callback=actual_callback)

    def __upload_http_batch_async(self, content_type, files_info, callback, progress_callback=None):
        content_headers = self._get_content_headers()
        upload_paths = list(map(lambda x: GCSObjectStore._get_shafile_path(x.sha), files_info))

        head_urls, put_urls = self.__get_urls_for_paths(upload_paths, content_type, content_headers)

        for cur_file_obj, put_url, head_url in zip(files_info, head_urls, put_urls):
            actual_progress_callback = self._create_progress_callback(progress_callback)

            actual_progress_callback_with_obj = self._create_progress_callback_with_args(actual_progress_callback, cur_file_obj)

            self.__upload_http_async(cur_file_obj, put_url, head_url, callback=callback, progress_callback=actual_progress_callback_with_obj)
