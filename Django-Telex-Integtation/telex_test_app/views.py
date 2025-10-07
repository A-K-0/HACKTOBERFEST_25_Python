from rest_framework import generics
from .utils import JiraReports
import requests
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


class TelexAPITest(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        base_url = request.build_absolute_uri('/').rstrip("/")
        integration_json = {

            "data": {
                "date": {
                  "created_at": "2025-02-21",
                  "updated_at": "2025-02-21"
                },
                "descriptions": {
                  "app_name": "Django-Jira Integration",
                  "app_description": "A Telex Interval integration that sends pending and resolved jira tasks for the week",
                  "app_logo": "https://cdn.logojoy.com/wp-content/uploads/20220329171603/dating-app-logo-example.jpg",
                  "app_url": base_url,
                  "background_color": "#fff"
                },
                "is_active": True,
                "integration_type": "interval",
                "integration_category": "Monitoring & Logging",
                "key_features": [
                  "Automatically fetches Jira issues(pending and resolved) for the week",
                  "Enhances team productivity"
                ],
                "author": "Chukwukodinaka Benjamin",
                "settings": [
                  {
                    "label": "interval",
                    "type": "dropdown",
                    "required": True,
                    "default": "* * * * *",
                    "description": "Select different intervals to send message to telex channel",
                    "options": ["* * * * *", "59 11 * * 6", "1 * * * *"]
                  },
                ],
                "target_url": "  ",
                "tick_url": f"{base_url}/tick"
            }

        }

        return Response(integration_json, status=200)



def generate_jira_report():
    """
    Generate the weekly Jira report by calling the JiraReports methods.
    """
    try:
        jira_reporter = JiraReports(
            domain=settings.JIRA_DOMAIN,
            email=settings.JIRA_EMAIL,
            api_token=settings.JIRA_API_TOKEN
        )


        issues = jira_reporter.get_weekly_issues()


        pending_count = len(issues.get("pending", []))
        resolved_count = len(issues.get("resolved", []))


        priority_counts = {"pending": {}, "resolved": {}}
        for status in ["pending", "resolved"]:
            for issue in issues.get(status, []):
                priority = issue["fields"]["priority"]["name"]
                priority_counts[status][priority] = priority_counts[status].get(priority, 0) + 1


        message = f"""
Weekly Jira Issues Summary ({(datetime.now() - timedelta(days=7)).strftime('%B %d')} - {datetime.now().strftime('%B %d, %Y')})

📊 Overview:
• New unresolved issues: {pending_count}
• Issues resolved this week: {resolved_count}
• Total issues handled: {pending_count + resolved_count}

🔍 Priority Breakdown:
New Unresolved Issues:
{jira_reporter.format_priority_counts(priority_counts['pending'])}

Resolved Issues:
{jira_reporter.format_priority_counts(priority_counts['resolved'])}

💡 Key Takeaways:
• Issue Resolution Rate: {jira_reporter.calculate_resolution_rate(pending_count, resolved_count)}
• Weekly Workload Index: {jira_reporter.calculate_workload_index(pending_count, resolved_count)}
"""

        return {
            'message': message,
            'username': 'Django-Jira Integration',
            'event_name': 'Telex-Integration',
            'status': 'success'
        }
    except Exception as e:

        return {
            'message': f"Error generating report: {str(e)}",
            'username': 'Django-Jira Integration',
            'event_name': 'Telex-Integration',
            'status': 'error'
        }

def process_jira_report():
    """
    Processes the Jira report and sends it to the Telex webhook.
    """
    data = generate_jira_report()
    try:
        requests.post(
            url= settings.TELEX_RETURN_URL,
            json=data
        )
    except Exception as e:

        print(f"Error sending report to webhook: {e}")

class JiraReportAPIView(APIView):
    """
    Sync POST endpoint that triggers the Jira report to be processed.
    """
    def post(self, request, *args, **kwargs):
        process_jira_report()
        return Response({"status": "accepted"}, status=202)