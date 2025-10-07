from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from telex_test_app import views


sample_issues = {
    "pending": [
         {"fields": {"priority": {"name": "High"}}},
         {"fields": {"priority": {"name": "Medium"}}}
    ],
    "resolved": [
         {"fields": {"priority": {"name": "Low"}}}
    ]
}

def fake_format_priority_counts(priority_counts):
    return ", ".join([f"{k}: {v}" for k, v in priority_counts.items()])

def fake_calculate_resolution_rate(pending, resolved):
    total = pending + resolved
    return f"{(resolved / total * 100):.2f}%" if total > 0 else "N/A"

def fake_calculate_workload_index(pending, resolved):
    return pending + resolved

class FakeJiraReports:
    def __init__(self, domain, email, api_token):
        self.domain = domain
        self.email = email
        self.api_token = api_token

    def get_weekly_issues(self):
        return sample_issues

    def format_priority_counts(self, counts):
        return fake_format_priority_counts(counts)

    def calculate_resolution_rate(self, pending, resolved):
        return fake_calculate_resolution_rate(pending, resolved)

    def calculate_workload_index(self, pending, resolved):
        return fake_calculate_workload_index(pending, resolved)



@patch('telex_test_app.views.JiraReports', new=FakeJiraReports)
class GenerateJiraReportTests(TestCase):
    def test_generate_jira_report_success(self):
        """
        Test that generate_jira_report returns a success payload
        with the expected structure.
        """
        result = views.generate_jira_report()
        self.assertEqual(result['status'], 'success')
        self.assertIn("Weekly Jira Issues Summary", result['message'])
        self.assertEqual(result['username'], "Django-Jira Integration")
        self.assertEqual(result['event_name'], "Telex-Integration")



@patch('telex_test_app.views.requests.post')
@patch('telex_test_app.views.JiraReports', new=FakeJiraReports)
class ProcessJiraReportTests(TestCase):
    def test_process_jira_report_calls_requests_post(self, mock_post):
        """
        Test that process_jira_report calls requests.post with the correct parameters.
        """
        # Call the function
        views.process_jira_report()
        from django.conf import settings
        expected_data = views.generate_jira_report()
        mock_post.assert_called_once_with(url=settings.TELEX_RETURN_URL, json=expected_data)

# --- Tests for the API Views ---
@patch('telex_test_app.views.process_jira_report')
class JiraReportAPIViewTests(APITestCase):
    def test_post_jira_report_api_view(self, mock_process_jira_report):
        """
        Test the JiraReportAPIView endpoint to ensure it returns 202 and triggers processing.
        """

        url = reverse('jira-report')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data, {"status": "accepted"})
        mock_process_jira_report.assert_called_once()

class TelexAPITestViewTests(APITestCase):
    def test_get_telex_api_test(self):
        """
        Test the TelexAPITest GET endpoint returns the expected JSON structure.
        """

        url = reverse('integration-json')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get("data")
        self.assertIsNotNone(data)
        # Check that expected keys are present
        self.assertIn("descriptions", data)
        self.assertIn("tick_url", data)
        # Check that the base URL is correctly formed in tick_url
        self.assertTrue(data["tick_url"].endswith("/tick"))
