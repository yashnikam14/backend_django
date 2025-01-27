from base_app.settings import SECRET_KEY
from .loggers import log_into_file
import jwt
from backend_app.models import UserDetails, UserToken


@staticmethod
def create_token(user):
    token = None
    try:
        log_into_file({"function": "create_token", "started": True})
        payloads = {
            "user_id": user.id,
            "mobile_number": user.mobile_number,
            "email": user.email
        }
        token = jwt.encode(payloads, SECRET_KEY, algorithm="HS256")
        log_into_file({"function": "create_token", "completed": True})

    except Exception as e:
        log_into_file({"function": "create_token", "exception": str(e)})

    return token

@staticmethod
def validate_token(token):
    user = None
    message = ''
    try:
        log_into_file({"function": "validate_token", "started": True})
        if token is None:
            message = 'Authentication credentials were not provided.'
        else:
            if token.__contains__('TOKEN'):
                token = token.split(" ")
                get_token = UserToken.objects.filter(token=token[1]).first()
                if get_token is not None:
                    user = UserDetails.objects.filter(id=get_token.user_id).first()
                else:
                    message = 'Invalid token provided.'
            else:
                message = 'Invalid Token provided.'
        log_into_file({"function": "validate_token", "completed": True})

    except Exception as e:
        log_into_file({"function": "validate_token", "exception": str(e)})

    return message, user