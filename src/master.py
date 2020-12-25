"""
Master file reads all urls and saves competitions to a JSON file.
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
    Send message to telegram chat.

    Args:
        telegram_url (string): Telegram api.
        chat_id (int): Chat id.
        message (string): Message.
    """
    url = "{}/sendMessage?chat_id={}&text={}".format(
        telegram_url, chat_id, message)
    get_url(url)


# Read run parameters.
telegram_api = sys.argv[1]
chat_id = sys.argv[2]
day_from_offset = sys.argv[3]

comps = read_slocomps(day_from_offset)

for comp in comps:
    name = comp['node']['title_field']
    event_start = comp['node']['Od']
    event_stop = comp['node']['Do']
    take_off = comp['node']['Lokacija']
    country = comp['node']['Dr\u017eava']
    msg = "New competition published on %s. '%s' will take place from %s to %s on %s (%s). Check %s for more info and registration." % (
        'SloComps', name, event_start, event_stop, take_off, country, 'https://comps.sffa.org')

    # Send message to group.
    response = send_message(telegram_api, chat_id, msg)
