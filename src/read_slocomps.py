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
    event_url = "https://comps.sffa.org/event/{}".format(
        name.replace(' ', '-').strip().lower())
    msg = "New _SloComps_ notification: Registrations for *{}* are now *open*. Check {} for more info.".format(
        name, event_url)

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
    msg = "New _SloComps_ notification: New event published. *{}* will take place from *{}* to *{}* on {}({}). Check {} for more info.".format(
        name, event_start, event_stop, location, country, event_url)

    return msg


def read_slocomps():
    """
    Get list of events from slocomps.

    Returns:
        list: List of telegram messages.
    """
    # Download data.
    with urllib.request.urlopen('https://comps.sffa.org/calendar') as url:
        comps_json = json.loads(url.read().decode())

        if not path.exists('data/events.json'):
            save_json_to_file('data/events.json', comps_json)

    # Read last saved data.
    with open('data/events.json', 'r') as f:
        comps_json_old = json.load(f)

    # Compare old and just downloaded json.
    telegram_messages = []
    if comps_json != comps_json_old:
        for comp_json in comps_json['nodes']:
            for comp_json_old in comps_json_old['nodes']:
                if comp_json != comp_json_old:
                    if comp_json['node']['Dogodek'] == comp_json_old['node']['Dogodek']:
                        if comp_json['node']['Registration Status'] != comp_json_old['node']['Registration Status']:
                            msg = report_updated_registration(
                                comp_json['node'])
                            telegram_messages.append(msg)

        # New events.
        last_old_event = comps_json_old['nodes'][0]['node']
        for comp_json in comps_json['nodes']:
            if (comp_json['node']['Dogodek'] != last_old_event['Dogodek']):
                # Probably new event.
                msg = report_new_event(comp_json['node'])
                telegram_messages.append(msg)
            else:
                break

        # Save updated file.
        save_json_to_file('data/events.json', comps_json)

    # Return messages.
    return telegram_messages
