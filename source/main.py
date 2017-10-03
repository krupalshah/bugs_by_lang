import argparse
import sys
from config import debug
from parse import generate_url
from fetch import search_issues, write_response

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
                    help="specify a file name if you want to write incoming json response.")
args = parser.parse_args()


def run(options):
    if debug:
        print("options: %s" % options)
    # checking if at least one option is specified
    if len(options) <= 1:
        print("You need to specify at least one option here. Type -h for more info.")
        return

    # generating url based on options
    url = generate_url(args)
    if debug:
        print("url : %s" % url)

    # authenticating if required and calling issue search api
    response = search_issues(url)
    if debug:
        print("response : %s" % str(response))

    # writing response to file if option has been specified
    if args.file:
        write_response(args.file, response)


if __name__ == '__main__':
    run(sys.argv)
