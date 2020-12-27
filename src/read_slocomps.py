from bs4 import BeautifulSoup
import requests
import json
import urllib.request
from datetime import datetime, timedelta
import os.path
from os import path


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
    event_url = "https://comps.sffa.org/event/{}".format(
        name.replace(' ', '-').strip().lower())
    msg = "New _SloComps_ notification: Registrations for *{}* are now *{}*. Check {} for more info.".format(
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
    event_url = "https://comps.sffa.org/event/{}".format(
        name.replace(' ', '-').strip().lower())
    msg = "New _SloComps_ notification: New event published. *{}* will take place from *{}* to *{}* on {}({}). Registrations are _{}_. Check {} for more info.".format(
        name, event_start, event_stop, location, country, registration_status, event_url)

    return msg


def read_slocomps():
    """
    Get list of events from SloComps.

    Returns:
        list: List of telegram messages.
    """
    # Download data.
    login_url = 'https://comps.sffa.org/user/login'
    request_utl = 'https://comps.sffa.org/calendar'

    payload = {
        'name': 'telegram-bot',
        'pass': 'vjUD`<bWen*9UdBz',
        'form_build_id': 'form-YtrArwGYXwquwFw-38gr0VbCC_MD2hzfbpugAcFRyrY',
        'form_id': 'user_login',
        'op': 'Log+in'
    }

    base_directory = ''

    with requests.Session() as session:
        post = session.post(login_url, data=payload)
        r = session.get(request_utl)
        comps_json = json.loads(r.text)

        if not path.exists(base_directory + 'data/events.json'):
            save_json_to_file(base_directory + 'data/events.json', comps_json)

    # Read last saved data.
    with open(base_directory + 'data/events.json', 'r') as f:
        comps_json_old = json.load(f)

    # Compare old and just downloaded json.
    telegram_messages = []
    if comps_json != comps_json_old:
        # Look for new or updated events.
        for comp_json in comps_json['nodes']:
            is_updated_or_new = True

            for comp_json_old in comps_json_old['nodes']:
                if comp_json == comp_json_old:
                    is_updated_or_new = False
                    break

            if is_updated_or_new:
                updated_status = False
                for comp_json_old in comps_json_old['nodes']:
                    if comp_json['node']['Dogodek'] == comp_json_old['node']['Dogodek']:
                        if comp_json['node']['Registration Status'] != comp_json_old['node']['Registration Status']:
                            updated_status = True
                            msg = report_updated_registration(
                                comp_json['node'])
                            telegram_messages.append(msg)

                if not updated_status:
                    msg = report_new_event(comp_json['node'])
                    telegram_messages.append(msg)

        # Save updated file.
        save_json_to_file(base_directory + 'data/events.json', comps_json)

    # Return messages.
    return telegram_messages
