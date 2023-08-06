import requests
from .apis.instagram import Authenticate
from .apis.exceptions import AuthenticateFailException, AuthenticateRevokeException

class Instpector:
    def __init__(self):
        self._auth = None
        self._browser_session = requests.session()

    def __del__(self):
        if self._browser_session:
            self._browser_session.close()

    def session(self):
        return self._browser_session

    def login(self, user, password, two_factor_code=None):
        self._auth = Authenticate(self._browser_session, user, password, two_factor_code)
        try:
            self._auth.login()
            return True
        except AuthenticateFailException as auth_exception:
            print(f"AuthenticateFailException: {auth_exception}")
            return False

    def logout(self):
        if not self._auth:
            print("No active session found.")
            return
        try:
            self._auth.logout()
        except AuthenticateRevokeException as auth_exception:
            print(f"AuthenticateRevokeException: {auth_exception}")
