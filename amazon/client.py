import requests
import time

_HOST_URL = "www.amazon.com"
_DEFAULT_USER_AGENT = ""
_CHROME_DEKSTOP_USER_AGENT = ""
_ACCEPT = "text/html,application/xhtml+xml,\
    application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"

_MAX_TRIAL_REQUESTS = 5
_WAIT_TIME_BETWEEN_REQUESTS = 1

_USER_AGENT_LIST = [
    _DEFAULT_USER_AGENT,
    _CHROME_DEKSTOP_USER_AGENT,
]

class Client(object):
    def __init__(self):
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

    def _update_headers(self, search_url):
        self.base_url = "https://" + \
            search_url.split("://")[1].split("/")[0] + "/"
        self.headers['Host'] = self.base_url.split("://")[1].split("/")[0]

    def _check_page(self, html_content):
        if "Sign in for the best experience" in html_content:
            valid_page = False
        elif "The request could not be satisfied." in html_content:
            valid_page = False
        elif "Robot Check" in html_content:
            valid_page = False
        else:
            valid_page = True
        return valid_page

    def _get(self, url):
        ret = self.session.get(url, headers=self.headers)
        if ret.status_code != 200:
            raise ConnectionError(
                'Status code {status} for url {url}\n{content}'.format(
                    status=ret.status_code, url=url, content=ret.text))
        return ret

    def _get_page_html(self, search_url):
        trials = 0
        res = None

        while trials < _MAX_TRIAL_REQUESTS:

            print('Trying user agent: {}'.format(self.headers['User-Agent']))
            trials += 1
            try:
                res = self._get(search_url)

                valid_page = self._check_page(res.text)

            # To counter the "SSLError bad handshake" exception
            except requests.exceptions.SSLError:
                valid_page = False

            except ConnectionError:
                valid_page = False

            if valid_page:
                break

            self._change_user_agent()
            time.sleep(_WAIT_TIME_BETWEEN_REQUESTS)

        if not valid_page:
            raise ValueError('No valid pages found! Perhaps the page returned \
                is a CAPTCHA? Check products.last_html_page')
        return res.text

    def get_products(self, search_url="", max_product=100):
        if search_url == "":
            raise ValueError ("no url provided")
        self._update_headers(search_url)

        while len(self.product_dict_list) < max_product:

            # get the html of the specified page
            page = self._get_page_html(search_url)
            print(page)

        return self.product_dict_list