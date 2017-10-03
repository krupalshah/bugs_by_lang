from config import issues_url
# ex: https: // api.github.com / search / issues?q = windows + label: bug + language: python + state: open & sort = created & order = asc


def generate_url(args):
    params = []
    if args.query:
        params.append("q=" + args.query)
    if args.language:
        params.append("language:" + args.language)
    if args.open:
        params.append("state:open")
    if not args.all:
        params.append("lable:bug")
    if args.user:
        params.append("user:" + args.user)
    if args.repo:
        params.append("repo:" + args.repo)
    if args.author:
        params.append("author:" + args.author)
    if args.assignee:
        params.append("assignee:" + args.assignee)
    if args.mentions:
        params.append("mentions:" + args.assignee)
    params.append("type:issue")
    return issues_url + "?" + "+".join(params)
