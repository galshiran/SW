from site_pkg.page_session_cls import PageSession

HALF_HOUR = 60 * 30


class SiteVisitor(object):
    """
    Representation of unique visitor to specific site
    All SiteVisitor instances are pointed by Site data structure:
        (site_visitors dict in Sessionizing class / site_visitor_cls.py module)
    """
    def __init__(self):
        """
        self.visitor: Visitor instance - value assigned inside Sessionizing._insert method
        self.site: Site instance - value assigned inside Site.get_site_visitor method
        self.last_session: last active PageSession instance
        No parameters passed to constructor since SiteVisitor instance is created dynamically by dafaultdict object.
        """
        self.visitor = None
        self.site = None
        self.last_session = None

    def insert_page_view_to_session(self, page_view):
        """
        If page_session_list is empty or timeframe delta between page_view and last session is greater than 30
            create new session
        else
            insert page_view to last session
        :param page_view:
        :return:
        """
        if not self.last_session or \
                page_view.timeframe - self.last_session.max_timeframe > HALF_HOUR:
            self.last_session = PageSession(page_view)
            self.site.page_session_list.append(self.last_session)
            self.site.num_of_sessions += 1
        else:
            self.last_session.insert_page_view(page_view)
