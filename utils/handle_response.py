from rest_framework.response import Response
from rest_framework import status as st
from django.db import connection
import traceback
from .loggers import log_into_file


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


def fetch_records(query):
    result = []
    cur = connection.cursor()
    try:
        cur.execute(query)
        log_into_file({"function": "fetch_records", "query": query})
        customer_lst = cur.fetchall()
        columns = [col[0] for col in cur.description]
        result = [dict(zip(columns, row)) for row in customer_lst]

    except Exception as e:
        log_into_file({"function": "fetch_records", "exception": str(e),
                       "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})

    finally:
        if cur is not None:
            cur.close()
        return result
