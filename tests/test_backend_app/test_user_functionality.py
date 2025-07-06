import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from rest_framework.test import APIRequestFactory
from rest_framework import status as st
from django.contrib.auth import get_user_model

from backend_app.models import UserDetails, UserToken, UserMapping
from backend_app.views import CreateUpdateUserAPI

User = get_user_model()


@pytest.mark.django_db
class TestCreateUpdateUserAPI:

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    @pytest.fixture
    def user_info(self):
        mock_user = MagicMock()
        mock_user.id = 1
        return mock_user

    def get_view(self):
        view = CreateUpdateUserAPI.as_view({'post': 'create'})
        return view

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    @patch('backend_app.views.create_token', return_value='dummy-token')
    def test_create_user_success(
        self, mock_create_token, mock_validate_token, mock_log, factory, user_info
    ):
        mock_validate_token.return_value = ("", user_info)

        data = {
            "name": "John Doe",
            "mobile_number": "1234567890",
            "email": "john@example.com",
            "gender": "MALE",
            "is_active": 1,
            "is_whatsApp": "Yes",
            "user_type": 2
        }

        request = factory.post('/user-functionality/', data, format='json')
        request.headers = {'Authorization': 'Bearer validtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_201_CREATED
        assert response.data["message"] == "User created successfully!"

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    def test_create_user_fail_duplicate(
        self, mock_validate_token, mock_log, factory, user_info
    ):
        mock_validate_token.return_value = ("", user_info)

        UserDetails.objects.create(
            name="Existing User",
            mobile_number="1234567890",
            email="existing@example.com",
            gender="MALE",
            is_active=1,
            is_whatsApp="Yes",
            created_by=user_info.id
        )

        data = {
            "name": "New User",
            "mobile_number": "1234567890",
            "email": "existing@example.com"
        }

        request = factory.post('/user-functionality/', data, format='json')
        request.headers = {'Authorization': 'Bearer validtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_400_BAD_REQUEST
        assert "already exists" in response.data["message"]

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    def test_create_user_no_token(self, mock_validate_token, mock_log, factory):
        mock_validate_token.return_value = ("Invalid token", None)

        data = {
            "name": "User",
            "mobile_number": "1234567890",
            "email": "user@example.com"
        }

        request = factory.post('/user-functionality/', data, format='json')
        request.headers = {}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_403_FORBIDDEN
        assert response.data["message"] == "Invalid token"

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    def test_create_user_invalid_payload(self, mock_validate_token, mock_log, factory, user_info):
        mock_validate_token.return_value = ("", user_info)

        data = {
            "name": "",  # Invalid
            "mobile_number": "",  # Invalid
            "email": "notanemail"  # Invalid
        }

        request = factory.post('/user-functionality/', data, format='json')
        request.headers = {'Authorization': 'Bearer validtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_400_BAD_REQUEST
        assert response.data["status"] == "fail"

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    def test_update_user_success(self, mock_validate_token, mock_log, factory, user_info):
        mock_validate_token.return_value = ("", user_info)

        existing_user = UserDetails.objects.create(
            name="Old Name",
            mobile_number="9999999999",
            email="old@example.com",
            gender="MALE",
            is_active=1,
            is_whatsApp="No",
            created_by=user_info.id
        )

        UserMapping.objects.create(user_id=existing_user.id, user_type=2)

        data = {
            "user_id": existing_user.id,
            "name": "New Name",
            "mobile_number": "9999999999",  # Same number
            "email": "new@example.com",
            "gender": "FEMALE",
            "is_active": 0,
            "is_whatsApp": "Yes",
            "user_type": 3
        }

        request = factory.post('/user-functionality/', data, format='json')
        request.headers = {'Authorization': 'Bearer validtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_200_OK
        assert response.data["message"] == "User updated successfully!"
        updated_user = UserDetails.objects.get(id=existing_user.id)
        assert updated_user.name == "New Name"

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    def test_update_user_fail_conflict(self, mock_validate_token, mock_log, factory, user_info):
        mock_validate_token.return_value = ("", user_info)

        user1 = UserDetails.objects.create(
            name="User1",
            mobile_number="1111111111",
            email="user1@example.com",
            gender="MALE",
            is_active=1,
            is_whatsApp="Yes",
            created_by=user_info.id
        )

        user2 = UserDetails.objects.create(
            name="User2",
            mobile_number="2222222222",
            email="user2@example.com",
            gender="MALE",
            is_active=1,
            is_whatsApp="Yes",
            created_by=user_info.id
        )

        UserMapping.objects.create(user_id=user2.id, user_type=2)

        data = {
            "user_id": user2.id,
            "name": "New Name",
            "mobile_number": "1111111111",
            "email": "user1@example.com",
        }

        request = factory.post('/user-functionality/', data, format='json')
        request.headers = {'Authorization': 'Bearer validtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_400_BAD_REQUEST
        assert "already exists" in response.data["message"]

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    def test_update_user_not_found(self, mock_validate_token, mock_log, factory, user_info):
        mock_validate_token.return_value = ("", user_info)

        data = {
            "user_id": 9999,  # Non-existent ID
            "name": "User",
            "mobile_number": "1234567890",
            "email": "user@example.com",
        }

        request = factory.post('/user-functionality/', data, format='json')
        request.headers = {'Authorization': 'Bearer validtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_400_BAD_REQUEST
        assert "not found" in response.data["message"]

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    def test_create_user_missing_fields(self, mock_validate_token, mock_log, factory, user_info):
        mock_validate_token.return_value = ("", user_info)

        data = {}

        request = factory.post('/user-functionality/', data, format='json')
        request.headers = {'Authorization': 'Bearer validtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_400_BAD_REQUEST
        assert response.data["status"] == "fail"
