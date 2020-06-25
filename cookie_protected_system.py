import json
import os
from json import JSONDecodeError

import requests
from selenium import webdriver

USER_AGENT = "SewooPrint"


def set_cookies_on_session(cookies, s):
    for key, val in cookies.items():
        s.cookies.set(key, val)
    return s


def selenium_to_normal_cookies(selenium_cookies):
    return {cookie['name']: cookie['value'] for cookie in selenium_cookies}


class CookieProtectedScrapeSystem:
    USER_AGENT = USER_AGENT

    def __init__(self, cookie_file_name, page_url):
        self.page_url = page_url
        self.cookie_file_name = cookie_file_name
        self._cookies = None

    def get_session(self) -> requests.Session:
        sess = requests.Session()
        sess.headers.update({"User-Agent": self.USER_AGENT})
        return sess

    def needs_new_cookies(self):
        sess = self.get_session()
        try:
            cookies = self.cookies
        except (FileNotFoundError, JSONDecodeError):
            return True
        set_cookies_on_session(cookies, sess)
        r = sess.get(self.page_url)
        return not r.url.startswith(self.page_url)

    @property
    def cookies(self):
        if self._cookies is None:
            with open(self.cookie_file_name, "r") as f:
                self._cookies = json.load(f)
        return self._cookies

    @cookies.setter
    def cookies(self, new_cookies):
        cookie_dir = os.path.dirname(self.cookie_file_name)
        os.makedirs(cookie_dir, exist_ok=True)
        with open(self.cookie_file_name, "w") as f:
            json.dump(new_cookies, f, indent=2)
        self._cookies = new_cookies

    def get_new_oauth_cookies(self):
        browser = webdriver.Chrome()
        browser.get(self.page_url)
        print("Please login on the browser window which has opened.")
        input("Press enter when login is complete, before closing the window.")
        cookies = browser.get_cookies()
        return cookies

    def download_page(self, session=None):
        if self.needs_new_cookies():
            s_cookies = self.get_new_oauth_cookies()
            cookies = selenium_to_normal_cookies(s_cookies)
            self.cookies = cookies
        sess = session or self.get_session()
        set_cookies_on_session(self.cookies, sess)
        resp = sess.get(self.page_url)
        resp.encoding = "utf-8"
        return resp
