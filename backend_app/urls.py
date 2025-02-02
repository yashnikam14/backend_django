
from django.urls import path, include
from .views import BaseAPI, CreateUpdateUserAPI, UserDetailsPI, UserLoginAPI, StudentMarks

from rest_framework.routers import SimpleRouter

backend_router = SimpleRouter()
backend_router.register('test', BaseAPI, basename="BaseAPI")
backend_router.register('user-functionality', CreateUpdateUserAPI, basename="CreateUpdateUserAPI")
backend_router.register('user-details', UserDetailsPI, basename="UserDetailsPI")
backend_router.register('user-login', UserLoginAPI, basename="UserLoginAPI")
backend_router.register('student-marks', StudentMarks, basename="StudentMarks")

urlpatterns = [
    path('', include(backend_router.urls)),
]

