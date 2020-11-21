class Visitor(object):
    """
    Representation of general visitor regardless of sites.
    """
    def __init__(self, visitor_id):
        self.visitor_id = visitor_id
        self.unique_sites = 1

    def __str__(self):
        return self.visitor_id

