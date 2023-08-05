# -*- coding: utf-8 -*-
import json
import logging
import os
import sys

from missinglink.core import ApiCaller
from missinglink.core.api import default_api_retry
from missinglink.core.exceptions import NonRetryException

from .query_results_fetcher import QueryResultsFetcher
from .query_results_cache import QueryResultsCache
from ..path_utils import safe_make_dirs
from ..backend_mixin import BackendMixin
from .base_metadata_db import BaseMetadataDB, MetadataOperationError
from six.moves.urllib.parse import urlencode


class BackendMetadataDB(BackendMixin, BaseMetadataDB):
    max_query_retry = 3
    default_cache_file_name = 'missinglink_query_v' + str(sys.version_info[0])

    ML_CACHE_FOLDER_ENV_VAR = 'ML_CACHE_FOLDER'
    ML_REQUESTS_CACHE_FOLDER_ENV_VAR = 'ML_REQUESTS_CACHE_FOLDER'
    ML_DISABLE_REQUESTS_CACHE_VAR = 'ML_DISABLE_REQUESTS_CACHE'

    def __init__(self, connection, config, session, cache_folder=None):
        super(BackendMetadataDB, self).__init__(connection, config, session)
        self.__query_parser = None

        if cache_folder is None:
            cache_folder = self._get_cache_folder()

        safe_make_dirs(cache_folder)

        self.__cache_folder_full_path = os.path.join(cache_folder, self.default_cache_file_name)

    @property
    def cache_folder_full_path(self):
        return self.__cache_folder_full_path

    @property
    def is_requests_cache_disabled(self):
        return os.environ.get(self.ML_DISABLE_REQUESTS_CACHE_VAR) == '1'

    @classmethod
    def _get_cache_folder(cls):
        from missinglink.core.config import default_missing_link_cache_folder

        requests_cache_path = os.environ.get(cls.ML_REQUESTS_CACHE_FOLDER_ENV_VAR)
        cache_path = os.environ.get(cls.ML_CACHE_FOLDER_ENV_VAR)
        return requests_cache_path or cache_path or default_missing_link_cache_folder()

    @property
    def _query_parser(self):
        from ..scam import QueryParser

        if self.__query_parser is not None:
            return self.__query_parser

        self.__query_parser = QueryParser()

        return self.__query_parser

    def _create_table(self):
        pass

    def _add_missing_columns(self, data_object):
        pass

    def get_data_for_commit(self, sha, commit_sha):
        raise NotImplementedError(self.get_data_for_commit)

    def _add_data(self, data):
        pass

    def add_data_using_url(self, metadata_url, isolation_token):
        if not metadata_url:
            logging.debug('no data provided')
            return

        logging.debug('add data %s', metadata_url)

        with self._connection.get_cursor() as session:
            url = 'data_volumes/%s/metadata/head/add' % self._volume_id

            msg = {
                'metadata_url': metadata_url,
                'isolation_token': isolation_token,
            }

            return ApiCaller.call(self._config, session, 'post', url, msg, retry=default_api_retry(), is_async=True)

    @classmethod
    def _convert_type(cls, schema, field_name, field_val):
        schema = schema or {}

        def convert_bool(v):
            return v not in ['no', 'No', 'False', 'false', '0', 0]

        def safe_json_loads(val):
            try:
                return json.loads(val)
            except ValueError:
                return val

        field_convert = {
            'STRING': lambda val: val,
            'JSON': safe_json_loads,
            'INTEGER': int,
            'FLOAT': float,
            'BOOLEAN': convert_bool,
        }

        json_complex_field_suffix = '_json'

        if field_name.endswith(json_complex_field_suffix):
            field_name = field_name[:-len(json_complex_field_suffix)]
            field_type = 'JSON'
        else:
            field_type = schema.get(field_name, 'STRING')

        return field_name, field_convert[field_type](field_val)

    @classmethod
    def _create_iter_data(cls, results_stream, schema=None):
        def handle_meta_item():
            def iter_list():
                for meta_key_val in val:
                    yield meta_key_val['key'], meta_key_val.get('val')

            items_iter = val.items if isinstance(val, dict) else iter_list

            meta = [cls._convert_type(schema, k, v) for k, v in items_iter()]

            return dict(meta)

        for data_point in results_stream:
            result_data_point = {}

            for key, val in data_point.items():
                if key == 'meta':
                    result_data_point['meta'] = handle_meta_item()
                    continue

                key, val = cls._convert_type(schema, '@' + key, val)
                result_data_point[key] = val

            yield result_data_point

    def __is_stable_query(self, query_text):
        from ..scam import QueryUtils

        return QueryUtils.get_version(query_text, parser_=self._query_parser) not in ['head', 'staging', None]

    @classmethod
    def _schema_as_dict(cls, schema_as_list):
        if schema_as_list is None:
            return None

        if isinstance(schema_as_list, dict):
            return schema_as_list

        if isinstance(schema_as_list, list):
            return {s['name']: s['type'] for s in schema_as_list}

    def _call_query_api(self, version_query, **kwargs):

        is_async = kwargs.pop('is_async', False)
        url = self.__build_query_api_url(version_query, **kwargs)

        try:
            api_result = ApiCaller.call(
                self._config,
                self._session,
                'get',
                url,
                retry=default_api_retry(stop_max_attempt_number=self.max_query_retry),
                is_async=is_async
            )
        except NonRetryException as ex:
            msg = 'Failed to run query "%s"\n%s' % (version_query, ex)
            raise NonRetryException(msg)

        api_result = self.__convert_result_from_old_client(api_result)

        if not api_result['ok']:
            raise MetadataOperationError(api_result['error'])

        return api_result

    def __build_query_api_url(self, version_query, **kwargs):
        params = {
            'query': version_query,
            'results_format': 'csv',
        }

        for key, val in kwargs.items():
            if val is None:
                continue

            params[key] = val

        return 'data_volumes/%s/query/?%s' % (self._volume_id, urlencode(params))

    @staticmethod
    def __convert_result_from_old_client(api_result):
        """
        Tuple results always come without schema data, it is called by old clients
        new clients calls using return_schema=True and the result will be returned using a dict
        """
        if isinstance(api_result, (tuple, list)):
            result_url, total_rows, total_size, explicit_query = api_result

            api_result = {
                'ok': True,
                'result_url': result_url,
                'total_data_points': total_rows,
                'total_size': total_size,
                'explicit_query': explicit_query,
            }

        return api_result

    def query(self, query_text, **kwargs):
        version_query = query_text if query_text else '@version:head'

        is_stable_query = self.__is_stable_query(version_query)
        should_cache_response = is_stable_query and not self.is_requests_cache_disabled

        if not should_cache_response:
            logging.info('not a stable query, caching cannot be used')

        query_cache_key = QueryResultsCache.build_query_cache_key(self._volume_id, query_text)
        query_results_cache = QueryResultsCache(self.__cache_folder_full_path, query_cache_key)
        query_results_fetcher = QueryResultsFetcher(query_results_cache, should_cache_response)

        if should_cache_response and query_results_fetcher.has_cached_results:
            results_stream, result_summary = query_results_fetcher.load_results_from_cache()
        else:
            api_result = self._call_query_api(version_query, **kwargs)

            if 'result_urls' in api_result:
                result_urls = api_result.pop('result_urls')
            else:
                # Backwards compatibility for old clients
                result_urls = [api_result['result_url']] if 'result_url' in api_result else None

            if result_urls and len(result_urls) > 0:
                results_stream, result_summary = query_results_fetcher.download_and_save_result_to_cache(result_urls, result_summary=api_result)
            else:
                # Backwards compatibility for old clients
                results_stream = api_result.pop('data_points') or []
                result_summary = api_result

        schema = self._schema_as_dict(result_summary.get('schema'))

        return self._create_iter_data(results_stream, schema), int(result_summary.get('total_data_points', 0)), int(result_summary.get('total_size', 0))

    def _query(self, sql_vars, select_fields, where, **kwargs):
        raise NotImplementedError(self._query)

    def get_all_data(self, sha):
        raise NotImplementedError(self.get_all_data)

    def end_commit(self):
        raise NotImplementedError(self.end_commit)

    def begin_commit(self, commit_sha, tree_id, ts):
        raise NotImplementedError(self.begin_commit)
