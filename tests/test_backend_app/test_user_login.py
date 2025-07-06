import pytest
from unittest.mock import patch
from rest_framework.test import APIRequestFactory
from rest_framework import status as st

from backend_app.views import UserLoginAPI
from backend_app.models import UserDetails, UserMapping, UserTypes, UserToken


@pytest.mark.django_db
class TestUserLoginAPI:

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def get_view(self):
        return UserLoginAPI.as_view({'post': 'create'})

    @patch('backend_app.views.log_into_file')
    def test_user_login_success(self, mock_log, factory):
        user = UserDetails.objects.create(
            name="John Doe",
            mobile_number="1234567890",
            email="john@example.com",
            gender="MALE",
            is_active=1,
            is_whatsApp="Yes",
            created_by=1
        )
        user_token = UserToken.objects.create(user_id=user.id, token="testtoken123")
        user_type = UserTypes.objects.create(user_type="Admin")
        UserMapping.objects.create(user_id=user.id, user_type=user_type.id)

        data = {"username": "1234567890"}
        request = factory.post('/user-login/', data, format='json')

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_200_OK
        assert response.data["status"] == "success"
        assert response.data["response_object"] == [{
            "user_id": user.id,
            "name": "John Doe",
            "email": "john@example.com",
            "mobile_number": "1234567890",
            "token": "testtoken123",
            "user_type": "Admin"
        }]

    @patch('backend_app.views.log_into_file')
    def test_user_login_with_email_success(self, mock_log, factory):
        user = UserDetails.objects.create(
            name="Jane Smith",
            mobile_number="9999999999",
            email="jane@example.com",
            gender="FEMALE",
            is_active=1,
            is_whatsApp="Yes",
            created_by=1
        )
        UserToken.objects.create(user_id=user.id, token="token456")
        user_type = UserTypes.objects.create(user_type="User")
        UserMapping.objects.create(user_id=user.id, user_type=user_type.id)

        data = {"username": "jane@example.com"}
        request = factory.post('/user-login/', data, format='json')

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_200_OK
        assert response.data["status"] == "success"
        assert response.data["response_object"][0]["user_type"] == "User"

    @patch('backend_app.views.log_into_file')
    def test_user_login_missing_username(self, mock_log, factory):
        data = {}  # No username provided
        request = factory.post('/user-login/', data, format='json')

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_400_BAD_REQUEST
        assert response.data["status"] == "fail"
        assert response.data["message"] == "username is required"

    @patch('backend_app.views.log_into_file')
    def test_user_login_user_not_found(self, mock_log, factory):
        data = {"username": "nonexistent@example.com"}
        request = factory.post('/user-login/', data, format='json')

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_400_BAD_REQUEST
        assert response.data["status"] == "fail"
        assert response.data["message"] == "User not found!"

    @patch('backend_app.views.log_into_file')
    def test_user_login_missing_token_or_mapping(self, mock_log, factory):
        user = UserDetails.objects.create(
            name="No Token User",
            mobile_number="2222222222",
            email="no_token@example.com",
            gender="MALE",
            is_active=1,
            is_whatsApp="Yes",
            created_by=1
        )
        # Note: No UserToken or UserMapping created

        data = {"username": "2222222222"}
        request = factory.post('/user-login/', data, format='json')

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["status"] == "fail"
        assert response.data["message"] == "something went wrong"

    @patch('backend_app.views.log_into_file')
    def test_user_login_unexpected_exception(self, mock_log, factory):
        # Simulate DB error or bad model access
        with patch('backend_app.views.UserDetails.objects.filter') as mock_filter:
            mock_filter.side_effect = Exception("DB error")

            data = {"username": "anyuser"}
            request = factory.post('/user-login/', data, format='json')

            view = self.get_view()
            response = view(request)

            assert response.status_code == st.HTTP_500_INTERNAL_SERVER_ERROR
            assert response.data["status"] == "fail"
            assert response.data["message"] == "something went wrong"
