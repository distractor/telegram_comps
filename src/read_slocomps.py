from datetime import datetime, timedelta
import os.path
from os import path
import json
from helper import *

def read_slocomps():
    msg = []

    # Load new data.
    new_data = load_data()
    orig_data = new_data
    # Load old data.
    with open('telegram_comps/data/events_slocomps.json', 'r') as f:
        old_data = json.load(f)

    # Find new comps.
    temp_msg, new_data = find_new_comps(new_data, old_data)
    msg.extend(temp_msg)
    # Find registration status update.
    msg.extend(find_registration_status_update(new_data, old_data))

    # Save data.
    if msg:
        save_json_to_file('telegram_comps/data/events_slocomps.json', orig_data)

    return msg

def remove_if_contains(messages, word):
    new_messages = []
    
    for msg in messages:
        if not word in msg:
            new_messages.append(msg)

    return new_messages
