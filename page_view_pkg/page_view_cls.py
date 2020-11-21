class PageView(object):
    """
    Representation of page view.
    """
    def __init__(self, visitor_id, site_url, page_view_url, timeframe):
        """
        Initialize PageView instance with a single row information from single input file.
        :param visitor_id:
        :param site_url:
        :param page_view_url:
        :param timeframe:
        """
        self.visitor_id = visitor_id
        self.site_url = site_url
        self.page_view_url = page_view_url
        self.timeframe = int(timeframe)

    def __lt__(self, other):
        """
        Implementation of "Lower Than" function - used in PriorityQueue comparison when timeframe (key) are equal.
        :param other:
        :return:
        """
        if not isinstance(other, PageView):
            raise NotImplemented
        return self.timeframe < other.timeframe

