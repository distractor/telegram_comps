from bs4 import BeautifulSoup
import requests
import json
from helper import *


def read_airtribune():
    # Load next events from page.
    next_events_from_page = load_next_events(['SLO'])
    # Load events from file.
    with open('telegram_comps/data/events_airtribune.json', 'r') as f:
        next_events_from_file = json.load(f)

    # Find new comps by id.
    msg = find_new_comp_ids(next_events_from_page, next_events_from_file)

    return msg

def load_next_events(ioc_codes):
    url="https://airtribune.com/events/next"

    # Make a GET request to fetch the raw HTML content.
    html_content = requests.get(url).text

    # Parse the html content.
    soup = BeautifulSoup(html_content, features="html5lib")

    # Get raw event data.
    all_scripts = soup.find_all("script")
    for script in all_scripts:
        if 'window.ATDATA.eventLists' in script.text: 
            raw_script = script.text
    
    raw_script = raw_script.split('window.ATDATA.eventLists = ')[1]
    raw_script = raw_script.split('window.ATDATA.hanggliding_classes')[0]
    raw_script = raw_script.strip()
    raw_script = raw_script[:-1]

    # Load to json.
    events = json.loads(raw_script)
    next_events = [event for event in events['next-events']['content'] if (event['country']['ioc_code'] in ioc_codes) and (event['sport'] == 0)]

    return next_events

def find_new_comp_ids(new_events, old_events):
    msg = []
    _new_events = new_events
    _old_events = old_events

    new_ids = [event['id'] for event in _new_events]
    old_ids = [event['id'] for event in _old_events]

    unknown_comp_ids = []
    for new_id in new_ids:
        if not(new_id in old_ids):
            unknown_comp_ids.append(new_id)

    if len(unknown_comp_ids) != 0:
        # List of all to-this-point unknown events.
        unknown_events = [event for event in _new_events if event['id'] in unknown_comp_ids]
    
        # Append them to file.
        for unknown_event in unknown_events:
            old_events.append(unknown_event)
        
        # Save to file.
        save_json_to_file('telegram_comps/data/events_airtribune.json', old_events)

        for unknown_event in unknown_events:
            # Build json object.
            temp_json = {}
            temp_json['Dogodek'] = unknown_event['title']
            temp_json['Od'] = unknown_event['start_date']
            temp_json['Do'] = unknown_event['end_date']
            temp_json['Lokacija'] = unknown_event['place']
            temp_json['Dr\u017eava'] = unknown_event['country']['name']
            temp_json['Registration Status'] = 'empty'
            temp_json['Link'] = "https://airtribune.com{}".format(unknown_event['url'])

            # Create message.
            msg.append(report_new_event(temp_json))

    return msg