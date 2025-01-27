from .loggers import log_into_file
from constants import MOBILE, EMAIL

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
