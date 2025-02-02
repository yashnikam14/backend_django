from utils.payloads import check_sections, get_date
from utils.loggers import log_into_file
import traceback
from utils.handle_response import fetch_records
from django.core.cache import cache
from datetime import datetime, timedelta


class StudentMarksReportCls:

    def __init__(self, from_date, to_date, section):
        self.from_date = from_date
        self.to_date = to_date
        self.section = section

    def get_student_marks(self, city=None, state=None, age=None):
        reports = []
        try:
            from_date, to_date = get_date(self.from_date, self.to_date)
            log_into_file({"function": "get_student_marks", "started": True})
            sections = check_sections(self.section)
            reports = cache.get("student-marks-with-details{}{}{}".format("?age={}".format(age) if age is not None else "", "?city={}".format(city) if city is not None else "", "?state={}".format(state) if state is not None else ""))
            if reports is None:
                print("caching..")
                query = """SELECT ms.creation_time AS creation_time,ms.section AS section, s.name AS student,
    c.state_id AS state_id, sd.name AS state, c.name AS city, ms.marks AS marks, ms.age as age
    FROM `mark_sheet` AS ms
    JOIN `stud_details` AS sd ON sd.name=ms.name
    JOIN `cities` AS c ON c.id=sd.city
    JOIN states AS s ON s.id=c.state_id
    WHERE ms.creation_time>='%s' AND ms.creation_time<='%s'
    AND ms.%s %s %s %s
    ORDER BY ms.creation_time DESC;""" % (from_date, to_date, sections,
                                          "AND ms.age>{}".format(age) if age is not None else "",
                                          "AND sd.city={}".format(city) if city is not None else "",
                                          "AND c.state_id={}".format(state) if state is not None else "")
                reports = fetch_records(query)
                cache.set("student-marks-with-details{}{}{}".format("?age={}".format(age) if age is not None else "", "?city={}".format(city) if city is not None else "", "?state={}".format(state) if state is not None else ""),
                          reports, timeout=timedelta(hours=24).total_seconds())
            log_into_file({"function": "get_student_marks", "completed": True})

        except Exception as e:
            log_into_file({"function": "get_student_marks", "exception": str(e),
                           "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})
        return reports