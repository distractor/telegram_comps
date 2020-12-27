"""
Master file downloads new competitions and sends messages to group.
"""
import sys

from read_slocomps import read_slocomps
from telegram_helper import *

# Read run parameters.
telegram_api = sys.argv[1]
chat_id = sys.argv[2]

# Read pages.
messages = read_slocomps()

# Send messages to group.
for msg in messages:
    print(msg)
    # send_message(telegram_api, chat_id, msg)
