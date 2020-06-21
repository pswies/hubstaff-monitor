import configparser
import os
from datetime import date, timedelta

from monitor.api_client import APIClient
from monitor.reporting import make_report, render_report


ENV_CHECK_DATE = 'check_date'
CONFIG_OUTPUT_PATH = 'OutputPath'


def read_config(path: str = '/app/config.ini') -> dict:  # technically, a dict-like object
    # Future TODO: let the user set a different config path at runtime.
    config = configparser.ConfigParser()
    config.read(path)
    return config['DEFAULT']


def determine_check_date(env: dict) -> date:
    if user_input := env.get(ENV_CHECK_DATE):
        return date.fromisoformat(user_input)
    else:
        return date.today() - timedelta(days=1)


if __name__ == '__main__':
    check_date = determine_check_date(os.environ)
    print(f'Performing check for: {check_date}')

    config = read_config()
    client = APIClient(config)
    client.authorize()

    report = make_report(client, check_date)
    render_report(report, config[CONFIG_OUTPUT_PATH])
    print('Done.')
