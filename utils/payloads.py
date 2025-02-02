from .loggers import log_into_file
from constants import MOBILE, EMAIL
import traceback
from backend_app.models import MarkSheet
from datetime import datetime


@staticmethod
def validate_payloads(payloads):
    message = ''
    try:
        log_into_file({"function": "validate_payloads", "started": True})
        if not list(payloads.values()).__contains__(None):
            for payload in payloads:
                if payload is not None:
                    if payload == 'mobile_number':
                        if len(payloads.get(payload)) != MOBILE:
                            message = 'Invalid mobile no.'
                            break

                    if payload == 'email':
                        if not payloads.get(payload).__contains__(EMAIL):
                            message = 'Invalid email'
                            break
                else:
                    message = '{} field is required'.format(payload)
                    break
        else:
            message = 'mandatory fields are required'

        log_into_file({"function": "validate_payloads", "completed": True})

    except Exception as e:
        log_into_file({"function": "validate_payloads", "exception": str(e)})

    return message

def check_sections(section):
    send_sections = None
    try:
        log_into_file({"function": "check_sections", "started": True})
        if section is None:
            sections = MarkSheet.objects.values('section', flat=True)
            get_section = ",".join(str(s) for s in sections)
            send_sections = "section in ({})".format(get_section)
        else:
            send_sections = "section = '{}'".format(section)

        log_into_file({"function": "check_sections", "completed": True})

    except Exception as e:
        log_into_file({"function": "check_sections", "exception": str(e),
                       "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})

    return send_sections

def get_date(f_date, t_date):
    from_date, to_date = None, None
    try:
        log_into_file({"function": "get_date", "started": True})
        from_date = datetime.strptime(f_date, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
        to_date = datetime.strptime(t_date, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M")

        log_into_file({"function": "get_date", "completed": True})

    except Exception as e:
        log_into_file({"function": "get_date", "exception": str(e),
                       "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})

    return from_date, to_date