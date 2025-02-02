import json
from datetime import datetime
from rest_framework import viewsets
from utils.loggers import log_into_file
from utils.security import create_token, validate_token
from utils.payloads import validate_payloads
from utils.handle_response import api_response, api_exception
from rest_framework import status as st

from .management.commands.data_generator import sections
from .models import UserToken, UserDetails, UserTypes, UserMapping
from django.db.models import Q
import traceback
from .reports import StudentMarksReportCls


class BaseAPI(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization', None)
            auth_message, user = validate_token(auth_header)
            print(1/0)
            if len(auth_message):
                return api_response('fail', auth_message, [],st.HTTP_403_FORBIDDEN)
            log_into_file({"function": "BaseAPI", "started": True})
            return api_response("success", "hello yash", [], st.HTTP_200_OK)
        except Exception as e:
            log_into_file({"function": "BaseAPI", "exception": str(e),
                           "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})
            return api_exception("fail", "something went wrong", [])


class CreateUpdateUserAPI(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            log_into_file({"function": "CreateUpdateUserAPI", "started": True})
            auth_header = request.headers.get('Authorization', None)
            auth_message, user_info = validate_token(auth_header)
            if len(auth_message):
                return api_response('fail', auth_message, [], st.HTTP_403_FORBIDDEN)

            name = request.data.get('name', None)
            mobile_number = request.data.get('mobile_number', None)
            email = request.data.get('email', None)
            gender = request.data.get('gender', 'MALE')
            is_active = request.data.get('is_active', 1)
            is_whatsApp = request.data.get('is_whatsApp', 'Yes')
            user_id = request.data.get('user_id')
            user_type = request.data.get('user_type', 2)

            payloads = validate_payloads({"name": name,
                                          "mobile_number": mobile_number,
                                          "email": email})
            if len(payloads):
                return api_response('fail', payloads, [], st.HTTP_400_BAD_REQUEST)

            status = 'fail'
            status_code = st.HTTP_400_BAD_REQUEST
            message = 'User is already exists with provided mob no./email.'
            response_object = []
            if user_id is None:
                get_user = UserDetails.objects.filter(Q(mobile_number=mobile_number) | Q(email=email)).first()
                if get_user is None:
                    log_into_file({"function": "creating user", "started": True})
                    user = UserDetails(name=name, mobile_number=mobile_number, email=email,
                                       gender=gender, is_active=is_active, is_whatsApp=is_whatsApp, created_by=user_info.id)
                    user.save()
                    log_into_file({"function": "creating user", "completed": True})

                    log_into_file({"function": "creating token", "started": True})
                    token = create_token(user)
                    user_token = UserToken(user_id=user.id, token=token)
                    user_token.save()
                    log_into_file({"function": "creating token", "completed": True})

                    log_into_file({"function": "creating user mapping", "started": True})
                    create_user_type = UserMapping(user_id=user.id, user_type=user_type)
                    create_user_type.save()
                    log_into_file({"function": "creating user mapping", "completed": True})

                    status_code = st.HTTP_201_CREATED
                    status = 'success'
                    message = 'User created successfully!'
            else:
                get_user = UserDetails.objects.filter(id=user_id).first()
                check_user = UserDetails.objects.filter(Q(mobile_number=mobile_number) | Q(email=email)).exclude(id=get_user.id).first()
                if check_user is None:
                    if get_user is not None:
                        get_user.name = name
                        get_user.email = email
                        get_user.gender = gender
                        get_user.is_active = is_active
                        get_user.is_whatsApp = is_whatsApp
                        get_user.updated_at = datetime.now()

                        get_user.save(update_fields=['name', 'email', 'gender', 'is_active', 'is_whatsApp', 'updated_at'])

                        get_user_mapping = UserMapping.objects.get(user_id=user_id)
                        get_user_mapping.user_type = user_type
                        get_user_mapping.save(update_fields=['user_type'])

                        status_code = st.HTTP_200_OK
                        status = 'success'
                        message = 'User updated successfully!'
                    else:
                        status_code = st.HTTP_400_BAD_REQUEST
                        message = 'User not found!'

            log_into_file({"function": "CreateUpdateUserAPI", "completed": True})
            return api_response(status, message, response_object, status_code)

        except Exception as e:
            log_into_file({"function": "CreateUpdateUserAPI", "exception": str(e),
                           "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})
            return api_exception("fail", "something went wrong", [])


class UserDetailsPI(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization', None)
            auth_message, user_info = validate_token(auth_header)
            if len(auth_message):
                return api_response('fail', auth_message, [], st.HTTP_403_FORBIDDEN)

            log_into_file({"function": "UserDetailsPI", "started": True})
            status_code = st.HTTP_200_OK
            response_object = []
            status = "success"
            message = ""

            user_id = request.query_params.get('user_id')
            users = UserDetails.objects.all()
            if user_id is not None:
                users = UserDetails.objects.filter(id=user_id).all()
                if not len(users):
                    status = "success"
                    message = "User not found!"

            icount = 1
            for user in users:
                get_user_type = UserMapping.objects.get(user_id=user.id)
                role = UserTypes.objects.get(id=get_user_type.user_type)
                response_object.append({
                    "key": icount,
                    "user_id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "mobile_number": user.mobile_number,
                    "user_type": role.user_type
                })
                icount += 1
            log_into_file({"function": "UserDetailsPI", "completed": True})

            return api_response(status, message, response_object, status_code)

        except Exception as e:
            log_into_file({"function": "UserDetailsPI", "exception": str(e),
                           "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})
            return api_exception("fail", "something went wrong", [])


class UserLoginAPI(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            log_into_file({"function": "UserLoginAPI", "started": True})
            username = request.data.get('username')
            status = 'fail'
            status_code = st.HTTP_400_BAD_REQUEST
            response_object = []
            message = 'username is required'

            if username is not None:
                user = UserDetails.objects.filter(Q(mobile_number=username) | Q(email=username)).first()
                if user is not None:
                    user.last_login_at = datetime.now()
                    user.save(update_fields=(['last_login_at']))
                    get_token = UserToken.objects.get(user_id=user.id)
                    get_user_type = UserMapping.objects.get(user_id=user.id)
                    role = UserTypes.objects.get(id=get_user_type.user_type)
                    response_object.append({
                        "user_id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "mobile_number": user.mobile_number,
                        "token": get_token.token,
                        "user_type": role.user_type
                    })
                    status = 'success'
                    status_code = st.HTTP_200_OK
                    message = ''
                else:
                    status = 'fail'
                    status_code = st.HTTP_400_BAD_REQUEST
                    response_object = []
                    message = 'User not found!'

            log_into_file({"function": "UserLoginAPI", "completed": True})
            return api_response(status, message, response_object, status_code)
        except Exception as e:
            log_into_file({"function": "UserLoginAPI", "exception": str(e),
                           "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})
            return api_exception("fail", "something went wrong", [])


class StudentMarks(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization', None)
            auth_message, user_info = validate_token(auth_header)
            if len(auth_message):
                return api_response('fail', auth_message, [], st.HTTP_403_FORBIDDEN)

            from_date = request.data.get('from_date')
            to_date = request.data.get('to_date')
            section = request.data.get('section')
            city = request.data.get('city')
            state = request.data.get('state')
            age = request.data.get('age')

            log_into_file({"function": "StudentMarks", "started": True})
            student_rep = StudentMarksReportCls(from_date, to_date, section)
            data = student_rep.get_student_marks(city, state, age)
            response = []
            icount = 1
            for d in data:
                json_data = json.loads(json.loads(d.get('marks')))
                response.append({
                    "key": icount,
                    "student": d.get('student'),
                    "section": d.get('section'),
                    "age": d.get('age'),
                    "city": d.get('city'),
                    "state": d.get('state'),
                    "creation_time": d.get('creation_time').strftime("%d %b %Y %I:%M%p"),
                    "science": json_data["science"],
                    "english": json_data["english"],
                    "history": json_data["history"],
                    "maths": json_data["maths"]

                })
                icount += 1
            log_into_file({"function": "StudentMarks", "completed": True})
            return api_response('success', '', response, st.HTTP_200_OK)

        except Exception as e:
            log_into_file({"function": "StudentMarks", "exception": str(e),
                           "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})
            return api_exception("fail", "something went wrong", [])