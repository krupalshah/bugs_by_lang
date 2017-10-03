from config import *
import urllib.parse
import requests

auth_token=""


def __authenticate():
    try:
        url = urllib.parse.urljoin(auth_url, client_id)
        payload = {"client_secret": client_secret}
        req = requests.put(url, payload)
        res = req.json
        return res['token']
    except ValueError as err:
        print("Error occured while authenticating!")
        print("trace : \n", err)
        return None
    except HTTPError as err:
        return None


def search_issues(url):
    if not url:
        return None
    try:
        req = requests.get(issues_url)

    except ValueError as err:
        print("Error occured while authenticating!")
        print("trace : \n", err)
        return None
    except requests.exceptions.HTTPError as err:
        auth_token = __authenticate()
        search_issue(url)


def write_response(file_name, response):
    if not response:
        return
