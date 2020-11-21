class PageSession(object):
    """
    Representation of page session.
    """
    def __init__(self, page_view):
        self.page_views = [page_view]  # List of session PageView
        self.min_timeframe = page_view.timeframe  # First PageView.timeframe of current session instance
        self.max_timeframe = page_view.timeframe  # Last PageView.timeframe of current session instance
        self.session_length = 0  # Session length - updated dynamically when new PageView is inserted

    def _update_session_length(self):
        """
        Calculate current session length.
        :return:
        """
        self.session_length = self.max_timeframe - self.min_timeframe

    def insert_page_view(self, page_view):
        """
        Insert new PageView to current session.
        1. Add new page to page_views list.
        2. Set max_timeframe to new PageView.timeframe
        3. Update session length.
        :param page_view:
        :return:
        """
        self.page_views.append(page_view)
        self.max_timeframe = page_view.timeframe
        self._update_session_length()

    def __add__(self, other):
        if not isinstance(other, PageSession):
            return NotImplemented
        return self.session_length + other.session_length
