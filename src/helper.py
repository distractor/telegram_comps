from bs4 import BeautifulSoup
import requests
import json
import urllib.request

def save_json_to_file(filepath, json_obj):
    """
    Saves json object to file.

    Args:
        filepath (string): File destination.
        json_obj (obj): Json object.
    """
    with open(filepath, 'w') as outfile:
        json.dump(json_obj, outfile, indent=2)


def report_updated_registration(json_obj):
    """
    Generate message for updated registration.

    Args:
        json_obj (obj): JSON obj.

    Returns:
        string: Message.
    """
    name = json_obj['Dogodek']
    registration_status = json_obj['Registration Status']
    event_url = json_obj['Link']
    msg = "New _SloComps_ notification: Registrations status for competition *{}* changed to *{}*. Check [event page]({}) for more info.".format(
        name, registration_status, event_url)

    return msg


def report_new_event(json_obj):
    """
    Generates new event message.

    Args:
        json_obj (obj): JSON obj.

    Returns:
        string: Message.
    """
    name = json_obj['Dogodek']
    event_start = json_obj['Od']
    event_stop = json_obj['Do']
    location = json_obj['Lokacija']
    country = json_obj['Dr\u017eava']
    registration_status = json_obj['Registration Status']
    event_url = json_obj['Link']
    msg = "New _SloComps_ notification: New event published. *{}* will take place from *{}* to *{}* on {}({}). Registrations are _{}_. Check [event page]({}) for more info.".format(
        name, event_start, event_stop, location, country, registration_status, event_url)

    return msg


def load_data():
    """
    Get list of events from SloComps.

    Returns:
        list: List of telegram messages.
    """
    # Download data.
    login_url = 'https://comps.sffa.org/user/login'
    request_url = 'https://comps.sffa.org/calendar'

    payload = {
        'name': 'telegram-bot',
        'pass': 'T?Y;sN7u8ePx7xzr',
        'form_build_id': 'form-YtrArwGYXwquwFw-38gr0VbCC_MD2hzfbpugAcFRyrY',
        'form_id': 'user_login',
        'op': 'Log+in'
    }

    base_directory = 'telegram_comps/'

    with requests.Session() as session:
        post = session.post(login_url, data=payload, verify=False)
        r = session.get(request_url, verify=False)
        comps_json = json.loads(r.text)

    return comps_json

def find_new_comps(new_data, old_data):
    msg = []
    new_urls = [d['node']['Link'] for d in new_data['nodes']]
    old_urls = [d['node']['Link'] for d in old_data['nodes']]

    old_comps = []
    for new_url in new_urls:
        comp = [d for d in new_data['nodes'] if d['node']['Link'] == new_url][0]
        if not new_url in old_urls:
            msg.append(report_new_event(comp['node']))
        else:
            old_comps.append(comp)

    data = {}
    data['nodes'] = old_comps

    return [msg, data]

def find_registration_status_update(new_data, old_data):
    msg = []

    old_urls = [d['node']['Link'] for d in old_data['nodes']]

    for old_url in old_urls:
        new_comp = [d['node'] for d in new_data['nodes'] if d['node']['Link'] == old_url][0]
        old_comp = [d['node'] for d in old_data['nodes'] if d['node']['Link'] == old_url][0]

        if (old_comp['Registration Status'] != new_comp['Registration Status']):
            msg.append(report_updated_registration(new_comp))
            
    return msg
