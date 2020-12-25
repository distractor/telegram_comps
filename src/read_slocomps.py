from bs4 import BeautifulSoup
import requests
import json
import urllib.request
from datetime import datetime, timedelta


def read_slocomps(day_from_offset):
    """
    Get data from SloComps.

    Returns:
        list: JSON list of competitions.
    """

    # Read json from url and convert to json object.
    with urllib.request.urlopen('https://comps.sffa.org/upcoming-json') as url:
        competitions_json = json.loads(url.read().decode())

    competitions_json = competitions_json['nodes']

    # Get competitions published between day_from and today.
    date_from = datetime.utcnow() + timedelta(days=int(day_from_offset))
    new_competition_list = []

    for comp_json in competitions_json:
        date_published_str = comp_json['node']['Published']
        date_published = datetime.strptime(
            date_published_str, '%d.%m.%Y -  %H:%M')

        if (date_published > date_from):
            # New comp was added. Append to output list.
            new_competition_list.append(comp_json)

    return new_competition_list
