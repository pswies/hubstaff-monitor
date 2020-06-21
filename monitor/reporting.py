from collections import defaultdict
from datetime import date, timedelta

import jinja2

from monitor.api_client import APIClient


TEMPLATES_PATH = '/app/monitor/templates'
REPORT_TEMPLATE_FILE = 'report.html'


class TrackedTime:
    """Helper class to represent tracked time and conveniently display it."""
    def __init__(self, value: int = 0):
        self.value = value

    def __add__(self, other):
        return TrackedTime(self.value + other)

    def __str__(self):
        return str(timedelta(seconds=self.value)) if self.value else '-'


def make_report(client: APIClient, check_date: date) -> dict:
    """
    Return a dict with all the data required to display a report.

    The central item is the `activity_table` which has the following format:
    {
        project_id: {
            user_id: tracked_time,
            ...
        },
        ...
    }
    """
    user_names = client.get_user_names()
    project_names = client.get_project_names()
    activities = client.get_activities(check_date)

    table = defaultdict(lambda: defaultdict(TrackedTime))
    user_ids = set()

    for entry in activities:
        project_id = entry['project_id']
        user_id = entry['user_id']
        seconds = entry['tracked']
        table[project_id][user_id] += seconds
        user_ids.add(user_id)

    return {
        'check_date': check_date,
        'user_names': user_names,
        'project_names': project_names,
        'activity_table': table,
        'ordered_user_ids': sorted(user_ids),
    }


def render_report(report: dict, output_path: str) -> None:
    print(f'Writing to: {output_path}')

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES_PATH),
        autoescape=True,
    )
    template = env.get_template(REPORT_TEMPLATE_FILE)
    html = template.render(**report)

    with open(output_path, 'w') as f:
        f.write(html)
