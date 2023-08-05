# -*- coding: utf-8 -*-
import itertools
import os

import requests
import six
import abc
import csv

from missinglink.legit.utils import atomic_write

METADATA_FIELD_SIZE_LIMIT = 1024 * 1024  # 1MB
csv.field_size_limit(METADATA_FIELD_SIZE_LIMIT)

# Will download the entire partial csv file before iterating it (BigQuery split's the result into files smaller then 1GB)
DOWNLOAD_REQUEST_CHUNK_SIZE = 1024 * 1024 * 1024  # 1GB


@six.add_metaclass(abc.ABCMeta)
class _BaseStreamArray(list):
    def __init__(self, parser_func=None):
        super(_BaseStreamArray, self).__init__()
        self._parser_func = parser_func
        self.__stream = None

    @abc.abstractmethod
    def _create_stream(self):
        """
        creates the stream
        """

    def _parse_stream(self, stream):
        if self._parser_func:
            return self._parser_func(stream)
        else:
            return stream

    @property
    def stream(self):
        if self.__stream is None:
            self.__stream = self._create_stream()
        return self.__stream

    def __iter__(self):
        parsed_stream = self._parse_stream(self.stream)

        for line in parsed_stream:
            yield line


class _DownloadStreamArrayFromUrl(_BaseStreamArray):

    def __init__(self, result_url, parser_func=None):
        super(_DownloadStreamArrayFromUrl, self).__init__(parser_func)
        self._result_url = result_url

    def _create_stream(self):
        r = requests.get(self._result_url, stream=True)  # allowed to use requests

        if r.encoding is None:
            r.encoding = 'utf-8'

        return r.iter_lines(decode_unicode=True, chunk_size=DOWNLOAD_REQUEST_CHUNK_SIZE)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._result_url)


class _StreamArrayFromFilePath(_BaseStreamArray):

    def __init__(self, file_path, parser_func=None):
        super(_StreamArrayFromFilePath, self).__init__(parser_func)
        self._file_path = file_path

    def _create_stream(self):
        return open(self._file_path, 'rt')

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._file_path)


class _StreamCSVArrayFromFilePath(_StreamArrayFromFilePath):

    @classmethod
    def _parse_stream(cls, stream):
        return parse_csv_stream_to_dict(stream)


def parse_csv_stream_to_dict(stream):
    reader = csv.DictReader(stream)
    replace_names = {'_sha': 'path', '_hash': 'id', '_commit_sha': 'version'}

    for row in reader:

        row_params = {}
        meta = {}
        for key, val in row.items():
            if val == '':
                continue

            is_meta = key.startswith('_')
            if is_meta:
                key = replace_names.get(key, key[1:])
                row_params[key] = val
                continue

            meta[key] = val

        if meta:
            row_params['meta'] = meta

        yield row_params


class _MultipleStream(list):
    def __init__(self, streams):
        super(_MultipleStream, self).__init__()
        self._streams = streams

    def __iter__(self):
        return itertools.chain(*self._streams)

    # according to the comment below
    def __len__(self):
        return sum([len(s) for s in self._streams])

    def __repr__(self):
        streams = [s.__repr__() for s in self._streams]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(streams))


class QueryResultsFetcher(object):

    def __init__(self, query_results_cache, should_cache_response=True):
        self._first_request = None
        self._is_live_result = True
        self.__query_results_cache = query_results_cache
        self._should_cache_response = should_cache_response

    @property
    def has_cached_results(self):
        return self.__query_results_cache.check_if_exists()

    def load_results_from_cache(self):
        result_summary = self.__query_results_cache.get_results_summary_data() or {}

        total_rows = result_summary.get('total_data_points', 0)

        if total_rows > 0:
            result_file_path = self.__query_results_cache.get_result_file_path()
            results_stream = _StreamCSVArrayFromFilePath(result_file_path)
        else:
            results_stream = []

        return results_stream, result_summary

    def download_and_save_result_to_cache(self, result_urls, result_summary):

        total_rows = result_summary.get('total_data_points', 0)

        if total_rows > 0:
            download_stream = self._build_download_stream(result_urls)
        else:
            download_stream = []

        if self._should_cache_response:
            self._merge_results_to_single_file(download_stream)
            self.__query_results_cache.save_query_result_summary(result_summary)
            return self.load_results_from_cache()

        return download_stream, result_summary

    def _build_download_stream(self, result_urls):
        parser_func = parse_csv_stream_to_dict if not self._should_cache_response else None
        streams = [_DownloadStreamArrayFromUrl(result_url, parser_func) for result_url in result_urls]
        download_stream = _MultipleStream(streams)
        return download_stream

    def _merge_results_to_single_file(self, download_stream):
        result_file_path = self.__query_results_cache.get_result_file_path()

        csv_header = None

        for row in download_stream:
            csv_header = row
            break

        if csv_header is None:
            return

        with atomic_write(result_file_path, mode='wt') as merged_result_file:
            merged_result_file.write(csv_header + os.linesep)

            for line in download_stream:

                is_header = line.startswith(csv_header)
                if is_header:
                    continue

                if not line.endswith(os.linesep):
                    line += os.linesep

                merged_result_file.write(line)
