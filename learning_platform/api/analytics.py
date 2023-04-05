class AnalyticReport(object):
    def __init__(self,
                 course: str,
                 views: int = 0,
                 count_students: int = 0,
                 percent_passed: float = 0.0,
                 date: str = None,
                 url: str = None):
        self.course = course
        self.views = views
        self.count_students = count_students
        self.percent_passed = percent_passed
        self.date = date
        self.url = url
