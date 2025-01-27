from rest_framework.response import Response
from rest_framework import status as st

def api_response(status, message, response_object, status_code):
    return Response({"status": status,
                     "message": message,
                     "response_object": response_object},
                    status_code)


def api_exception(status, message, response_object):
    return Response({"status": status,
                     "message": message,
                     "response_object": response_object},
                    st.HTTP_500_INTERNAL_SERVER_ERROR)