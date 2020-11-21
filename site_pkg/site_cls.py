from collections import defaultdict

from visitor_pkg.site_visitor_cls import SiteVisitor
from site_pkg.merge_sort import MergeSort


class Site(object):
    """
    Representation of site object.
    All Site instances are pointed by the main data structure
        (sites dict in Sessionizing class / sessionizing.py module)
    """
    def __init__(self):
        """
        self.num_of_sessions: number of sessions per site
        self.page_session_list: list of PageSession instances
        self.site_visitors: dafaultdict of SiteVisitor instances.
        """
        self.num_of_sessions = 0
        self.page_session_list = []
        self.site_visitors = defaultdict(lambda: SiteVisitor())
        self.sorted_sessions = False  # Boolean indicating whether the data has been already sorted.

    def get_site_sessions_median(self):
        """
        Get site median according to page_session_list.
        If first median query for this site (self.sorted_sessions = False) - sort the list using merge sort algorithm.
        Return the median by list length.
        :return:
        """
        if not self.sorted_sessions:
            MergeSort.merge_sort(self.page_session_list, 0, self.num_of_sessions - 1)
            self.sorted_sessions = True

        median_index = int(self.num_of_sessions / 2)
        if self.num_of_sessions % 2:
            median = float(self.page_session_list[median_index].session_length)
        else:
            median = (self.page_session_list[median_index] + self.page_session_list[median_index - 1]) / 2

        return median

    def get_site_visitor(self, visitor_id):
        """
        Get SiteVisitor object from site_visitors dictionary.
        If a new visitor - set its site reference.
        :param visitor_id:
        :return:
        """
        site_visitor = self.site_visitors[visitor_id]
        if not site_visitor.site:
            site_visitor.site = self

        return site_visitor
