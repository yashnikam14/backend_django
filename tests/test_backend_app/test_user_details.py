import pytest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIRequestFactory
from rest_framework import status as st

from backend_app.views import UserDetailsAPI
from backend_app.models import UserDetails, UserMapping, UserTypes


@pytest.mark.django_db
class TestUserDetailsAPI:

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    @pytest.fixture
    def user_info(self):
        mock_user = MagicMock()
        mock_user.id = 1
        return mock_user

    def get_view(self):
        return UserDetailsAPI.as_view({'get': 'list'})

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    def test_list_users_success(self, mock_validate_token, mock_log, factory, user_info):
        mock_validate_token.return_value = ("", user_info)

        user1 = UserDetails.objects.create(
            name="User1", mobile_number="1234567890", email="user1@example.com",
            gender="MALE", is_active=1, is_whatsApp="Yes", created_by=user_info.id
        )
        user_type = UserTypes.objects.create(user_type="Admin")
        UserMapping.objects.create(user_id=user1.id, user_type=user_type.id)

        request = factory.get('/user-list/')
        request.headers = {'Authorization': 'Bearer validtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_200_OK
        print(response.data)
        assert response.data["status"] == "success"
        assert response.data["response_object"] == [{'key': 1, 'user_id': 1, 'name': 'User1', 'email': 'user1@example.com', 'mobile_number': '1234567890', 'user_type': 'Admin'}]

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    def test_list_user_by_id_found(self, mock_validate_token, mock_log, factory, user_info):
        mock_validate_token.return_value = ("", user_info)

        user1 = UserDetails.objects.create(
            name="User1", mobile_number="1234567890", email="user1@example.com",
            gender="MALE", is_active=1, is_whatsApp="Yes", created_by=user_info.id
        )
        user_type = UserTypes.objects.create(user_type="Admin")
        UserMapping.objects.create(user_id=user1.id, user_type=user_type.id)

        request = factory.get('/user-list/', {'user_id': user1.id})
        request.headers = {'Authorization': 'Bearer validtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_200_OK
        assert response.data["status"] == "success"
        print(response.data)
        print(user1.id)
        assert response.data["response_object"][0]["user_id"] == user1.id

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    def test_list_user_by_id_not_found(self, mock_validate_token, mock_log, factory, user_info):
        mock_validate_token.return_value = ("", user_info)

        request = factory.get('/user-list/', {'user_id': 999})
        request.headers = {'Authorization': 'Bearer validtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_200_OK
        assert response.data["status"] == "success"
        assert response.data["message"] == "User not found!"
        assert response.data["response_object"] == []

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    def test_list_user_invalid_token(self, mock_validate_token, mock_log, factory):
        mock_validate_token.return_value = ("Invalid token", None)

        request = factory.get('/user-list/')
        request.headers = {'Authorization': 'Bearer invalidtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_403_FORBIDDEN
        assert response.data["status"] == "fail"
        assert response.data["message"] == "Invalid token"
        assert response.data["response_object"] == []

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    def test_list_user_exception_handling(self, mock_validate_token, mock_log, factory, user_info):
        mock_validate_token.return_value = ("", user_info)

        user1 = UserDetails.objects.create(
            name="User1", mobile_number="1234567890", email="user1@example.com",
            gender="MALE", is_active=1, is_whatsApp="Yes", created_by=user_info.id
        )

        request = factory.get('/user-list/')
        request.headers = {'Authorization': 'Bearer validtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["status"] == "fail"
        assert "something went wrong" in response.data["message"]
        assert response.data['response_object'] == []
