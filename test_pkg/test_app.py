import unittest
import glob
import csv
from collections import defaultdict

import pandas as pd

from sessionizing import Sessionizing


class TestSessionizing(unittest.TestCase):
    def __init__(self, *args):
        super().__init__(*args)
        self.sessionizing = None
        self.sites_session_counter = {}
        self.users_unique_sites_dict = {}
        self.sites_sessions_length = defaultdict(list)

    def setUp(self):
        """
        This method run before each test.
        If test objects (data structures) already initialized - skip.
        Else:
            1. Initialize Sessionizing object with input data.
            2. Initialize naive data structure for tests.
        :return:
        """
        input_files = glob.glob("/home/galsh/mine/sw/test/*.csv")  # Read input (csv) files from current (sw/test) directory.
        if not self.sessionizing:
            self.sessionizing = Sessionizing()
            self.sessionizing.initialize(*input_files)
        if not self.sites_session_counter:
            self.merge_and_sort_input_files(*input_files)
            self.process_input_files()

    # def test_visitor_count(self):
    #     visitors = list(self.users_unique_sites_dict.keys())
    #     for i in range(len(visitors)):
    #         naive_data = self.users_unique_sites_dict[visitors[i]]
    #         sessionizing_data = self.sessionizing.visitors[visitors[i]].unique_sites
    #         try:
    #             self.assertEqual(naive_data, sessionizing_data)
    #         except AssertionError:
    #             print("Visitor {} unique sites number {} != {}".format(visitors[i], naive_data, sessionizing_data))
    #
    # def test_session_count_per_site(self):
    #     sites = list(self.sites_session_counter.keys())
    #     for i in range(len(sites)):
    #         naive_data = self.sites_session_counter[sites[i]]
    #         sessionizing_data = self.sessionizing.sites[sites[i]].num_of_sessions
    #         try:
    #             self.assertEqual(naive_data, sessionizing_data)
    #         except AssertionError:
    #             print("Site {} sessions number {} != {}".format(sites[i], naive_data, sessionizing_data))

    def test_session_median_per_site(self):
        sites = list(self.sites_sessions_length.keys())
        for i in range(len(sites)):
            naive_data = self.sites_sessions_length[sites[i]]
            naive_median = self._get_median_session(naive_data, sites[i])
            sessionizing_data = self.sessionizing.sites[sites[i]].get_site_sessions_median()
            try:
                self.assertEqual(naive_median, sessionizing_data)
            except AssertionError:
                print("Site {} median {} != {}".format(sites[i], naive_median, sessionizing_data))

    def _get_median_session(self, session_list, site):
        median_index = int(len(session_list) / 2)
        if len(session_list) % 2:
            median_data = self.sites_sessions_length[site][median_index]
        else:
            median_data = (self.sites_sessions_length[site][median_index] + self.sites_sessions_length[site][median_index - 1]) / 2

        return median_data

    def process_input_files(self):
        with open('/home/galsh/mine/sw/merged.csv') as f:
            reader = csv.reader(f)
            next(reader)  # Skip first row which includes columns name
            try:
                row = next(reader)
                line, visitor, site_url, page_site_url, timeframe = row
                last_visitor = visitor
                last_site_url = site_url
                last_session_timeframe = timeframe
                first_session_timeframe = timeframe
                self.users_unique_sites_dict[visitor] = 1
                self.sites_session_counter[site_url] = 1

                while True:
                    row = next(reader)
                    line, visitor, site_url, page_site_url, timeframe = row
                    if visitor == last_visitor:
                        if site_url == last_site_url:
                            if int(timeframe) - int(last_session_timeframe) > 1800:
                                self.sites_session_counter[site_url] += 1
                                self.sites_sessions_length[site_url].append(int(last_session_timeframe) - int(first_session_timeframe))
                                first_session_timeframe = timeframe
                        else:
                            self.users_unique_sites_dict[visitor] += 1
                            if site_url in self.sites_session_counter:
                                self.sites_session_counter[site_url] += 1
                            else:
                                self.sites_session_counter[site_url] = 1
                            last_site_url = site_url
                            self.sites_sessions_length[site_url].append(
                                int(last_session_timeframe) - int(first_session_timeframe))
                            first_session_timeframe = timeframe
                    else:
                        self.users_unique_sites_dict[visitor] = 1
                        if site_url in self.sites_session_counter:
                            self.sites_session_counter[site_url] += 1
                        else:
                            self.sites_session_counter[site_url] = 1
                        last_visitor = visitor
                        last_site_url = site_url
                        self.sites_sessions_length[site_url].append(
                            int(last_session_timeframe) - int(first_session_timeframe))
                        first_session_timeframe = timeframe
                    last_session_timeframe = timeframe
            except StopIteration:
                for k in self.sites_sessions_length.keys():
                    self.sites_sessions_length[k].sort()

    def merge_and_sort_input_files(self, *args):
        dfs = [pd.read_csv(f, header=None, sep=",") for f in args]
        df = pd.concat(dfs, ignore_index=True)
        df.sort_values([0, 1, 3], ascending=(True, True, True), inplace=True)
        df.to_csv("/home/galsh/mine/sw/merged.csv")


if __name__ == '__main__':
    unittest.main()
