"""
Master file downloads new competitions and sends messages to group.
"""
import sys
import requests

from read_slocomps import read_slocomps


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")

    return content


def send_message(telegram_url, chat_id, message):
    """
    Send message to Telegram chat.

    Args:
        telegram_url (string): Telegram api.
        chat_id (int): Chat id.
        message (string): Message.
    """
    url = "{}/sendMessage?chat_id={}&text={}".format(telegram_url, chat_id, message)
    get_url(url)


# Read run parameters.
telegram_api = sys.argv[1]
chat_id = sys.argv[2]
day_from_offset = sys.argv[3]

comps = read_slocomps(day_from_offset)

for comp in comps:
    name = comp['node']['Dogodek']
    event_start = comp['node']['Od']
    event_stop = comp['node']['Do']
    country = comp['node']['Dr\u017eava']
    event_url = "https://comps.sffa.org/event/{}".format(name.replace(' ', '-').strip().lower())
    msg = "New competition published on SloComps. Competition '%s' will take place from %s to %s in %s. Check %s for more info and registration." % (
    name, event_start, event_stop, country, event_url)

    # Send message to group.
    response = send_message(telegram_api, chat_id, msg)
