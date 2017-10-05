import argparse
import sys
import requests
import json
from config import *

# preparing cli options using argparse
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--language",
                    type=str,
                    metavar="",
                    help="programming language you want to search for.")
parser.add_argument("-q", "--query",
                    type=str,
                    metavar="",
                    help="additional query word to search for in issues list.")
parser.add_argument("-o", "--open",
                    type=bool,
                    default=False,
                    metavar="",
                    help="do you want only open issues?")
parser.add_argument("-a", "--all",
                    default=False,
                    type=bool,
                    metavar="",
                    help="do you want statistics of all issues, not just bugs?")
parser.add_argument("-u", "--user",
                    type=str,
                    metavar="",
                    help="issues specific to username.")
parser.add_argument("-r", "--repo",
                    type=str,
                    metavar="",
                    help="issues specific to repository.")
parser.add_argument("-au", "--author",
                    type=str,
                    metavar="",
                    help="issues created by specific username.")
parser.add_argument("-as", "--assignee",
                    type=str,
                    metavar="",
                    help="issues assigned specific username.")
parser.add_argument("-mn", "--mentions",
                    type=str,
                    metavar="",
                    help="issues mentioning specific username.")
parser.add_argument("-f", "--file",
                    type=str,
                    metavar="",
                    help="specify a file name if you want to write json response.")
args = parser.parse_args()


def generate_params(args):
   # ex: https: // api.github.com / search / issues?q = windows + label: bug + language: python + state: open & sort = created & order = asc
    params = []
    if args.query:
        params.append(args.query)
    else:
        params.append("bug")
    if args.language:
        params.append("language:%s" % args.language)
    if args.open:
        params.append("state:open")
    if not args.all:
        params.append("label:bug")
    if args.user:
        params.append("user:%s" % args.user)
    if args.repo:
        params.append("repo:%s" % args.repo)
    if args.author:
        params.append("author:%s" % args.author)
    if args.assignee:
        params.append("assignee:%s" % args.assignee)
    if args.mentions:
        params.append("mentions:%s" % args.assignee)
    params.append("type:issue")
    return "+".join(params)


def search_issues(query):
    if not query:
        return None
    headers = {
        "content-type": "application/json"
    }
    query_params = {
        "q": query
    }
    req = requests.get(issues_url, params=query_params, headers=headers)
    req.raise_for_status()
    if debug:
        print("url : %s" % req.url)
    try:
        return req.json()
    except ValueError as err:
        print("Unknown error occured while fetching data!")
        print("trace : \n", err)
        return None
    except requests.exceptions.HTTPError as err:
        print("Server error occured while fetching data!")
        if debug:
            print("error response : %s" % str(err.response))
        return None


def write_response(file_name, response):
    if not response:
        return
    formatted_json = json.dumps(response, indent=4)
    try:
        file = open(file_name, "w")
        file.write(formatted_json)
        file.close()
    except IOError as err:
        print("Error occured while writing to file.")
        print("trace : \n", err)


def run(options):
    if debug:
        print("options: %s" % options)
    # checking if at least one option is specified
    if len(options) <= 1:
        print("You need to specify at least one option here.")
        print("Type -h for more info.")
        return

    # generating query params based on options
    params = generate_params(args)
    if debug:
        print("params : %s" % params)

    # calling issue search api
    response = search_issues(params)
    if debug:
        print("response : %s" % response)

    # writing response to file if option has been specified
    if args.file:
        write_response(args.file, response)

    print("Count : %s" % response["total_count"])


if __name__ == '__main__':
    run(sys.argv)
