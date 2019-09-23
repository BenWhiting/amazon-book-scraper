import requests
import uuid 
import time
import re
import html
from html.parser import HTMLParser
from urllib.parse import urlparse
from bs4 import BeautifulSoup

_HOST_URL = "www.amazon.com"
_HTML_PARSER = "html.parser"

################## USER-AGENT HEADERS ##################
_DEFAULT = 'Mozilla/5.0 (Linux; Android 7.0; \
SM-A520F Build/NRD90M; wv) AppleWebKit/537.36 \
(KHTML, like Gecko) Version/4.0 \
Chrome/65.0.3325.109 Mobile Safari/537.36'

_CHROME_DESKTOP = 'Mozilla/5.0 (Macintosh; \
Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/67.0.3396.79 Safari/537.36'

_ACCEPT = "text/html,application/xhtml+xml,\
    application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"

_USER_AGENT_LIST = [
    _DEFAULT,
    _CHROME_DESKTOP,
]
################## SCANNING REGEX ##################
_BASE_URL = '(https://www.amazon.com)(.*)(&page=)([1-9]\d*)(&+.*)(sr_pg_)([1-9]\d*)'
_MOBILE_URL = '(https://www.amazon.com)(.*)(&page=)([1-9]\d*)(&+.*)(is_pn_)([1-9]\d*)'

_REGEX_NEXT_LIST = [
    _BASE_URL,
    _MOBILE_URL,
]
################## CSS SELECTORS ##################
_CSS_SELECTORS_DESKTOP = {
    "product": "ul > li.s-result-item > div.s-item-container",
    "title": "a.s-access-detail-page > h2",
    "rating": "i.a-icon-star > span",
    "review_nb": "div.a-column.a-span5.a-span-last > \
                div.a-row.a-spacing-mini > \
                a.a-size-small.a-link-normal.a-text-normal",
    "url": "div.a-row.a-spacing-small > div.a-row.a-spacing-none > a[href]",
    "img": "div.a-column.a-span12.a-text-center > a.a-link-normal.a-text-normal > img[src]",
    "next_page_url": "a#pagnNextLink",
}
_CSS_SELECTORS_DESKTOP_2 = {
    "product": "div.s-result-list.sg-row > div.s-result-item",
    "title": "div div.sg-row  h5 > span",
    "rating": "div div.sg-row .a-spacing-top-mini i span",
    "review_nb": "div div.sg-row .a-spacing-top-mini span.a-size-small",
    "url": "div div a.a-link-normal",
    "img": "img[src]",
    "next_page_url": "li.a-last > a[href]",
}

_CSS_SELECTORS_MOBILE = {
    "product": "#resultItems > li",
    "title": "a > div > div.sx-table-detail > h5 > span",
    "rating": "a > div > div.sx-table-detail > \
               div.a-icon-row.a-size-small > i > span",
    "review_nb": "a > div > div.sx-table-detail > \
                  div.a-icon-row.a-size-small > span",
    "url": "a[href]",
    "img": "img[src]",
    "next_page_url": "ul.a-pagination > li.a-last > a[href]",
}

_CSS_SELECTORS_MOBILE_GRID = {
    "product": "#grid-atf-content > li > div.s-item-container",
    "title": "a > div > h5.sx-title > span",
    "rating": "a > div > div.a-icon-row.a-size-mini > i > span",
    "review_nb": "a > div > div.a-icon-row.a-size-mini > span",
    "url": "a[href]",
    "img": "img[src]",
    "next_page_url": "ul.a-pagination > li.a-last > a[href]",
}

_CSS_SELECTOR_LIST = [
                        _CSS_SELECTORS_DESKTOP,
                        _CSS_SELECTORS_DESKTOP_2,
                        _CSS_SELECTORS_MOBILE,
                        _CSS_SELECTORS_MOBILE_GRID,
                     ]

################## SOUP SCANS ###############
_SPAN_CLASS_TITLE_MEDIUM = 'span[class="a-size-medium a-color-base a-text-normal"]'
_SPAN_CLASS_TITLE_BASE = 'span[class="a-size-base a-color-base a-text-normal"]'
_SPAN_SPONSERED_TITLE = 'div[data-component-type="sp-sponsored-result"]' 

################## NUMBER CONSTS ##################
_MAX_TRIAL_REQUESTS = 25
_WAIT_TIME_BETWEEN_REQUESTS = 1

################## CODE ##################
class Client(object):
    def __init__(self):
        self.session = requests.session()
        self.current_user_agent_index=0
        self.headers = {
            'Host': _HOST_URL,
            'User-Agent': _USER_AGENT_LIST[0],
            'Accept': _ACCEPT,
        }
        self.url_list = []

    def initial_scan(self, root_url=""):
        # create all URLS
        next_url = root_url
        print("Starting at URL: {}".format(root_url))

        # get all products
        while True:
            if next_url == "":
                break
            # update headers
            self._update_headers(next_url)

            # get the page
            self.url_list.append(next_url)
            page = self._get_page_html(next_url)
            if not page:
                print("nothing to see here, trying again")
                continue
                
            #extract next page
            next_search = self._extract_next_page_url(page)
            if next_search == "":
                print("no more pages found")
                break
            unescaped_next_search = html.unescape(next_search)
            url = urlparse("{}{}".format(self.base_url, unescaped_next_search))
            
            # purge url
            next_url = url.geturl()
            print("Next url: {}".format(next_url))   
            next_url = self._update_url(next_url)
            print("Updated Next url: {}".format(next_url))   
        return

    def _update_url(self, url):
        '''
        Sometimes amazon returns a url where the pages 
        do not match up, which can lead to odd behavior.
        This will make sure they line up
        '''
        updated_url = ""
        for regex_url in _REGEX_NEXT_LIST:
            m = re.search(regex_url, url)
            if m is not None:
                if m.lastindex != 7 :
                    continue

                updated_url = "{}{}{}{}{}{}{}".format(
                    m.group(1),
                    m.group(2),
                    m.group(3),
                    int(m.group(4)),
                    m.group(5),
                    m.group(6),
                    int(m.group(7)) + 1)
                break
        return updated_url

    def _change_user_agent(self):
        index = (self.current_user_agent_index + 1) % len(_USER_AGENT_LIST)
        self.headers['User-Agent'] = _USER_AGENT_LIST[index]
        self.current_user_agent_index = index

    def _update_headers(self, search_url):
        self.base_url = "https://" + \
            search_url.split("://")[1].split("/")[0] + "/"
        self.headers['Host'] = self.base_url.split("://")[1].split("/")[0]

    def _check_page(self, html_content):
        sign_in_msg = "Sign in for the best experience"
        request_not_satisfied_msg = "The request could not be satisfied."
        robot_check_msg = "Robot Check"

        if sign_in_msg in html_content:
            print(sign_in_msg)
            valid_page = False
        elif request_not_satisfied_msg in html_content:
            print(request_not_satisfied_msg)
            valid_page = False
        elif robot_check_msg in html_content:
            print(robot_check_msg)
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
                print("Utilizing agent: {}".format(self.headers['User-Agent']))
                break

            self._change_user_agent()
            time.sleep(_WAIT_TIME_BETWEEN_REQUESTS)

        if not valid_page:
            raise ValueError('No valid pages found! Perhaps the page returned \
                is a CAPTCHA? Check products.last_html_page')
        return res.text

################## Extractor details ##################
    def _extract_next_page_url(self, page):
        url = ""
        pageSoup = BeautifulSoup(page, _HTML_PARSER)
        f = open('./failures/page-{}'.format(uuid.uuid1()), 'w')
        f.write(str(pageSoup))
        f.write("########\n")
        selector = 0
        successful = False
        for css_selector_dict in _CSS_SELECTOR_LIST:
            selector += 1
            css_selector = css_selector_dict.get("next_page_url", "")
            next_page = pageSoup.select(css_selector)
            if len(next_page) >= 1:
                hrefSoup = BeautifulSoup(str(next_page[0]), _HTML_PARSER)
                for a in hrefSoup.find_all('a', href=True):
                    if a.text != "":
                        f.write(str(selector))
                        f.write("\n##########\n")
                        f.write(css_selector)
                        successful = True
                        url = a['href']
                        f.write("\n##########\n")
                        f.write(url)
                break
            else:
                print("can't find using selector {}".format(css_selector))
        if not successful:
            print("finding next page not successful")
        f.close()
        return url

################## HTML details ##################
    def _get_title(self, product):
        main_css_selectors = [
            _SPAN_CLASS_TITLE_MEDIUM,
            _SPAN_CLASS_TITLE_BASE
        ]

        for selector in main_css_selectors:
            title = _css_select(product, selector)
            if title: 
                #regex = '(<span class=\"a-size-medium a-color-base a-text-normal\">)(.*)(</span>)'
                #m = re.search(regex, str(title))
                #title = m.group(2)
                print(title)
                break

        if not title:
            backup_css_selectors = [
                _SPAN_SPONSERED_TITLE
            ]
            for selector in backup_css_selectors:
                title = _css_select(product, selector)
                if title: 
                    print("Title found... ignoring results due to sponsored")
                    return ""

            f = open('./failures/title-{}'.format(uuid.uuid1()), 'w')
            f.write(str(product))
            f.close()
            print('failed to extract title')

        return title  

def _css_select(soup, css_selector):
    return soup.select(css_selector)