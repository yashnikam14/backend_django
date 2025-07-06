import pytest
import json
from unittest.mock import patch, MagicMock
from rest_framework.test import APIRequestFactory
from rest_framework import status as st
from backend_app.views import StudentMarks


@pytest.mark.django_db
class TestStudentMarksAPI:

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def get_view(self):
        return StudentMarks.as_view({'post': 'create'})

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    @patch('backend_app.views.StudentMarksReportCls')
    def test_student_marks_success(self, mock_report_cls, mock_validate_token, mock_log, factory):
        mock_validate_token.return_value = ("", MagicMock(id=1))

        mock_instance = MagicMock()
        mock_instance.get_student_marks.return_value = [
            {
                "student": "John Doe",
                "section": "A",
                "age": 15,
                "city": "New York",
                "state": "NY",
                "creation_time": MagicMock(strftime=lambda fmt: "01 Jan 2024 10:00AM"),
                "marks": json.dumps(json.dumps({
                    "science": 90,
                    "english": 85,
                    "history": 88,
                    "maths": 95
                }))
            }
        ]
        mock_report_cls.return_value = mock_instance

        data = {
            "from_date": "2024-01-01",
            "to_date": "2024-12-31",
            "section": "A",
            "city": "New York",
            "state": "NY",
            "age": 15
        }

        request = factory.post('/student-marks/', data, format='json')
        request.headers = {'Authorization': 'Bearer validtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_200_OK
        assert response.data["status"] == "success"
        assert len(response.data["response_object"]) == 1
        assert response.data["response_object"][0]["student"] == "John Doe"
        assert response.data["response_object"][0]["science"] == 90

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    def test_student_marks_invalid_token(self, mock_validate_token, mock_log, factory):
        mock_validate_token.return_value = ("Invalid token", None)

        request = factory.post('/student-marks/', {}, format='json')
        request.headers = {'Authorization': 'Bearer invalidtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_403_FORBIDDEN
        assert response.data["status"] == "fail"
        assert response.data["message"] == "Invalid token"

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    @patch('backend_app.views.StudentMarksReportCls')
    def test_student_marks_empty_result(self, mock_report_cls, mock_validate_token, mock_log, factory):
        mock_validate_token.return_value = ("", MagicMock(id=1))

        mock_instance = MagicMock()
        mock_instance.get_student_marks.return_value = []
        mock_report_cls.return_value = mock_instance

        request = factory.post('/student-marks/', {}, format='json')
        request.headers = {'Authorization': 'Bearer validtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_200_OK
        assert response.data["status"] == "success"
        assert response.data["response_object"] == []

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    @patch('backend_app.views.StudentMarksReportCls')
    def test_student_marks_invalid_json(self, mock_report_cls, mock_validate_token, mock_log, factory):
        mock_validate_token.return_value = ("", MagicMock(id=1))

        mock_instance = MagicMock()
        mock_instance.get_student_marks.return_value = [
            {
                "student": "Jane",
                "section": "B",
                "age": 14,
                "city": "LA",
                "state": "CA",
                "creation_time": MagicMock(strftime=lambda fmt: "01 Feb 2024 11:00AM"),
                "marks": "invalid-json"
            }
        ]
        mock_report_cls.return_value = mock_instance

        request = factory.post('/student-marks/', {}, format='json')
        request.headers = {'Authorization': 'Bearer validtoken'}

        view = self.get_view()
        response = view(request)

        assert response.status_code == st.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["status"] == "fail"
        assert response.data["message"] == "something went wrong"

    @patch('backend_app.views.log_into_file')
    @patch('backend_app.views.validate_token')
    def test_student_marks_internal_exception(self, mock_validate_token, mock_log, factory):
        mock_validate_token.return_value = ("", MagicMock(id=1))

        with patch('backend_app.views.StudentMarksReportCls') as mock_cls:
            mock_cls.side_effect = Exception("Unexpected error")

            request = factory.post('/student-marks/', {}, format='json')
            request.headers = {'Authorization': 'Bearer validtoken'}

            view = self.get_view()
            response = view(request)

            assert response.status_code == st.HTTP_500_INTERNAL_SERVER_ERROR
            assert response.data["status"] == "fail"
            assert response.data["message"] == "something went wrong"
