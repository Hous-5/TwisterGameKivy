from kivy.network.urlrequest import UrlRequest
import json

class ServerCommunication:
    def __init__(self, base_url):
        self.base_url = base_url
        self.access_token = None

    def register(self, username, password, on_success=None, on_failure=None):
        data = json.dumps({"username": username, "password": password})
        headers = {'Content-Type': 'application/json'}
        UrlRequest(
            f"{self.base_url}/register",
            on_success=lambda req, result: self._handle_register_response(result, on_success, on_failure),
            on_failure=lambda req, result: on_failure(result) if on_failure else None,
            req_body=data,
            req_headers=headers,
            method='POST'
        )

    def _handle_register_response(self, result, on_success, on_failure):
        if 'error' in result:
            if on_failure:
                on_failure(result['error'])
        else:
            if on_success:
                on_success(result)

    def login(self, username, password, on_success=None, on_failure=None):
        data = json.dumps({"username": username, "password": password})
        headers = {'Content-Type': 'application/json'}
        UrlRequest(
            f"{self.base_url}/login",
            on_success=lambda req, result: self._handle_login_response(result, on_success, on_failure),
            on_failure=lambda req, result: on_failure(result) if on_failure else None,
            req_body=data,
            req_headers=headers,
            method='POST'
        )

    def _handle_login_response(self, result, on_success, on_failure):
        if 'access_token' in result:
            self.access_token = result['access_token']
            if on_success:
                on_success(result)
        else:
            if on_failure:
                on_failure(result.get('error', 'Login failed'))

    def get_leaderboard(self, on_success=None, on_failure=None):
        UrlRequest(
            f"{self.base_url}/leaderboard",
            on_success=lambda req, result: on_success(result) if on_success else None,
            on_failure=lambda req, result: on_failure(result) if on_failure else None
        )

    def submit_score(self, score, on_success=None, on_failure=None):
        if not self.access_token:
            if on_failure:
                on_failure("Not authenticated")
            return

        data = json.dumps({"score": score})
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        UrlRequest(
            f"{self.base_url}/submit_score",
            on_success=lambda req, result: on_success(result) if on_success else None,
            on_failure=lambda req, result: on_failure(result) if on_failure else None,
            req_body=data,
            req_headers=headers,
            method='POST'
        )