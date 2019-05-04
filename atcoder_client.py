import getpass
import os
from http.cookiejar import LWPCookieJar
import requests
import re
import html

default_cookie_path = os.path.join(
    os.path.expanduser('~/.local/share'), 'atcoder-cookie.txt')

client=None

def get_client():
    global client
    if client is not None:
        return client
    client = AtCoderClient()
    client.login()
    return client

def save_cookie(session: requests.Session):
    cookie_path = default_cookie_path
    os.makedirs(os.path.dirname(cookie_path), exist_ok=True)
    session.cookies.save()
    print("Saved session into {}".format(os.path.abspath(cookie_path)))
    os.chmod(cookie_path, 0o600)


def load_cookie_to(session: requests.Session):
    cookie_path = default_cookie_path
    session.cookies = LWPCookieJar(cookie_path)
    if os.path.exists(cookie_path):
        session.cookies.load()
        return True
    return False


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AtCoderClient(metaclass=Singleton):

    def __init__(self):
        self._session = requests.Session()

    def check_logging_in(self):
        private_url = "https://atcoder.jp/settings"
        resp = self.request(private_url)
        return resp.url == private_url

    def login(self, username=None, password=None, use_local_session_cache=True, save_session_cache=True):
        if use_local_session_cache:
            load_cookie_to(self._session)
            if self.check_logging_in():
                print("Logged in successfully.")

                return

        r = self.request("https://atcoder.jp/login")
        csrf = re.search('name="csrf_token" value=\'(.+?)\'', r.text).group(1)
        csrf = html.unescape(csrf)
        if username is None:
            username = input('username: ')

        if password is None:
            password = getpass.getpass('password: ')

        resp = self.request("https://atcoder.jp/login", data={
            'username': username,
            "password": password,
            'csrf_token': csrf,
        }, method='POST')

        if 'incorrect' in resp.text:
            print(resp.text)
            raise Exception('Failed to Log in')
        if use_local_session_cache and save_session_cache:
            save_cookie(self._session)

    def request(self, url: str, method='GET', **kwargs):
        if method == 'GET':
            response = self._session.get(url, **kwargs)
        elif method == 'POST':
            response = self._session.post(url, **kwargs)
        else:
            raise NotImplementedError
        response.encoding = response.apparent_encoding
        return response
