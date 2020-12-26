import requests


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
    url = "{}/sendMessage?chat_id={}&text={}&parse_mode=markdown".format(
        telegram_url, chat_id, message)
    get_url(url)
