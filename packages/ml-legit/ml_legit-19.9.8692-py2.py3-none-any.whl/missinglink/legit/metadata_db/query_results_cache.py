# -*- coding: utf-8 -*-
import os
import json
import hashlib
from ..path_utils import safe_make_dirs


class QueryResultsCache(object):

    QUERY_RESULTS_CACHE_FOLDER = 'query_results'

    """
     Used as utility to store requests
    """

    def __init__(self, cache_folder_full_path, query_cache_key):

        results_cache_folder = os.path.join(cache_folder_full_path, self.QUERY_RESULTS_CACHE_FOLDER)
        safe_make_dirs(results_cache_folder)

        self._results_cache_folder = results_cache_folder
        self._query_cache_key = query_cache_key

    def check_if_exists(self):
        """
        Returns:
            bool
        """
        result_file_path = self.get_result_file_path()
        results_summary_file_path = self._results_summary_data_file_path()
        return os.path.exists(result_file_path) or os.path.exists(results_summary_file_path)

    @staticmethod
    def build_query_cache_key(volume_id, query_text):
        """
        Query cache key is used to index queries in the request cache layer

        Args:
            volume_id (str):
            query_text (str):

        Returns:
            str
        """
        data_string = '{volume_id}|{query_text}'.format(volume_id=volume_id, query_text=query_text)

        sha_1 = hashlib.sha1()

        data_encoded = data_string.encode()
        sha_1.update(data_encoded)

        return sha_1.hexdigest()

    # Result Summary

    def save_query_result_summary(self, results_summary_data):
        results_summary_file_path = self._results_summary_data_file_path()
        with open(results_summary_file_path, 'w') as file_object:

            json.dump(results_summary_data, file_object)

    def get_results_summary_data(self):
        results_summary_file_path = self._results_summary_data_file_path()

        if not os.path.exists(results_summary_file_path):
            return None

        with open(results_summary_file_path, 'r') as file_object:
            return json.load(file_object)

    def _results_summary_data_file_path(self):
        return os.path.join(self._results_cache_folder, '{}_summary.json'.format(self._query_cache_key))

    def get_result_file_path(self):
        return os.path.join(self._results_cache_folder, '{}_results.csv'.format(self._query_cache_key))
