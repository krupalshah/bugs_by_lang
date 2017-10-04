from config import *
import urllib.parse
import requests

auth_token = None


def __authenticate():
    try:
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "note": "bugs_by_lang"
        }
        req = requests.post(auth_url, data=payload)
        req.raise_for_status()
        res = req.json
        if debug:
            print(res)
        auth_token = res['token']
    except ValueError as err:
        print("Error occured while authenticating!")
        if debug:
            print("trace : \n", err)


def search_issues(url):
    if not url:
        return None
    if not auth_token:
        __authenticate()
    try:
        headers = {"access_token": auth_token}
        req = requests.get(url, headers=headers)
        req.raise_for_status()
        res = req.json
        return res
    except ValueError as err:
        print("Unknown error occured while fetching data!")
        print("trace : \n", err)
        return None
    except HTTPError as err:
        print("Server error occured while fetching data!")
        if debug:
            print("error response : %s" % str(err.response))


def write_response(file_name, response):
    if not response:
        return
