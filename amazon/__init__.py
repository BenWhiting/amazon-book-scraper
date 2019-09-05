import requests
from amazon.client import Client

_HOST_URL = "www.amazon.com"
_DEFAULT_USER_AGENT = ""
_CHROME_DEKSTOP_USER_AGENT = ""
_ACCEPT = "text/html,application/xhtml+xml,\
    application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"


_USER_AGENT_LIST = [
    _DEFAULT_USER_AGENT,
    _CHROME_DEKSTOP_USER_AGENT,
]

class Connection(object):
    def __init__(self, URL=""):
        self.url = URL
        self.session = requests.session()
        self.current_user_agent_index=0
        self.headers = {
            'Host': _HOST_URL,
            'User-Agent': _USER_AGENT_LIST[0],
            'Accept': _ACCEPT,
        }
        self.product_dict_list = []
        self.html_pages = []

    def _change_user_agent(self):
        index = (self.current_user_agent_index + 1) % len(_USER_AGENT_LIST)
        self.headers['User-Agent'] = _USER_AGENT_LIST[index]
        self.current_user_agent_index = index

    def search(self, search_url="", max_product=100):
        cli = Client()
        cli.get_products(search_url, max_product)