from datetime import datetime, timedelta
from typing_extensions import LiteralString

import requests
from typing import Dict

class JiraReports:
    def __init__(self, domain: str, email: str, api_token: str):
        self.base_url = f"https://{domain}/rest/api/3"
        self.auth = (email, api_token)

    def get_weekly_issues(self) -> Dict:
        """Get issues created and resolved in the past week."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        queries = {
            "pending": f'created >= "{start_date.strftime("%Y-%m-%d")}" AND status = "In Progress"',
            "resolved": f'resolved >= "{start_date.strftime("%Y-%m-%d")}" AND status = "Done"'
        }

        results = {}
        for status, jql in queries.items():
            response = requests.get(
                f"{self.base_url}/search",
                auth=self.auth,
                params={
                    "jql": jql,
                    "fields": "summary,status,priority,assignee"
                }
            )
            response.raise_for_status()
            results[status] = response.json()["issues"]


        return results


    def format_priority_counts(self, priority_dict: Dict) -> LiteralString | str:
        """Format priority counts for the API response."""
        formated_items = [f"Priority -> {priority}: {count}" for priority, count in priority_dict.items()]


        return ", ".join(formated_items)

    def calculate_resolution_rate(self, pending: int, resolved: int) -> float:
        """Calculate the resolution rate percentage."""
        total = pending + resolved
        return round((resolved / total * 100), 1) if total > 0 else 0


    def calculate_workload_index(self, pending: int, resolved: int) -> str:
        """Calculate a simple workload assessment."""
        ratio = pending / (resolved + 1)
        if ratio < 0.5:
            return "Light"
        elif ratio < 1.0:
            return "Moderate"
        else:
            return "Heavy"