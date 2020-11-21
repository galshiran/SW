import csv
from contextlib import ExitStack
from collections import defaultdict
from queue import PriorityQueue

from page_view_pkg.page_view_cls import PageView
from visitor_pkg.visitor_cls import Visitor
from site_pkg.site_cls import Site

__author__ = "Gal Shiran"


class Sessionizing(object):
    def __init__(self):
        # Default dictionary object which return a new instance of Site when key is missing
        # holds Site instances as values.
        self.sites = defaultdict(lambda: Site())
        # Default dictionary object - holds Visitor instances as values.
        self.visitors = dict()
        # Boolean flag indicates whether the program already initialized to support new input without restarting the app
        # If true - will wipe the data structures (sites / visitors).
        self.is_initialized = False
        self.faulty_lines_counter = 0  # Counter for input rows with length not equal to 4.
        self.q = PriorityQueue()  # Used for getting the lowest timeframe view, implemented with heap.

    def initialize(self, *args):
        """
        Initialize program data using input files.
        Reading input files under stack context to easily open multiple file at once with context manager.
        :param args:
        :return:
        """
        # If Sessionizing object already initialized - wipe the data older data.
        if self.is_initialized:
            self.sites.clear()
            self.visitors.clear()

        # Open multiple file descriptors under one context (stack).
        # At the end of this context (when indented block ends) all file descriptors will be close automatically.
        with ExitStack() as stack:
            csv_files = [stack.enter_context(open(fname)) for fname in args]
            readers = [csv.reader(csv_file) for csv_file in csv_files]

            # Read first record from each input file
            for reader in readers:
                self._read_next_record(reader)

            # Get the lowest timeframe record While Q holds not consumed records.
            # Each Q entry includes:
            # 1. Timeframe as key for comparison.
            # 2. PageView object.
            # 3. PageView source reader in order to read the next record from the same input file.
            while not self.q.empty():
                timeframe, (page_view, reader) = self.q.get()
                self._insert(page_view)  # Insert lowest timeframe record to sites and visitors data structures.
                self._read_next_record(reader)

            self.is_initialized = True

        return self.faulty_lines_counter  # Return the number of faulty records.

    def _read_next_record(self, reader):
        """
        Read new record using a given reader.
        :param reader:
        :return:
        """
        try:
            row = next(reader)  # Read next record from given reader
            while len(row) != 4:  # Record will be defined as faulty if its length is not equal to z
                self.faulty_lines_counter += 1
                row = next(reader)
            page_view = PageView(*row)
            # Insert record to Q with timeframe as key and page_view and reader instances.
            self.q.put((page_view.timeframe, (page_view, reader)))
        except StopIteration:
            print("Input file descriptor {} has reached his limit".format(reader))

    def _insert(self, page_view):
        """
        Insert new page_view instance into sites dictionary
        Create or update Visitor info for unique site
        :param page_view:
        :return:
        """
        site_url = page_view.site_url
        visitor_id = page_view.visitor_id

        # Get site data object from sites_data dictionary
        # If page view is a first view of a particular site - return a new defaultdict object
        # Else return the Site instance from sites_data dictionary
        site_data = self.sites[site_url]  # If missing key - defaultdict will return new Site instance

        # Get site visitor data from site_data dictionary
        # For the first site visit of a particular user - return a new SiteVisitor instance
        # Else return the existing SiteVisitor instance from Site instance
        site_visitor = site_data.get_site_visitor(visitor_id)

        # If a new SiteVisitor - initialize visitor attribute of SiteVisitor instance:
        #   If a new system visitor:
        #       Create new Visitor in visitors dictionary
        #   Else:
        #       Get Visitor instance from visitors dictionary and increase unique_sites by 1
        if not site_visitor.visitor:
            if visitor_id in self.visitors:
                site_visitor.visitor = self.visitors[visitor_id]
                site_visitor.visitor.unique_sites += 1
            else:
                site_visitor.visitor = self.visitors[visitor_id] = Visitor(visitor_id)

        # Insert the new PageView instance into SiteVisitor session.
        site_visitor.insert_page_view_to_session(page_view)

