from config import issues_url


def generate_url(args):
   # ex: https: // api.github.com / search / issues?q = windows + label: bug + language: python + state: open & sort = created & order = asc
    params = []
    if args.query:
        params.append("q=%s" % args.query)
    else:
        params.append("q=bug")
    if args.language:
        params.append("language:%s" % args.language)
    if args.open:
        params.append("state:open")
    if not args.all:
        params.append("lable:bug")
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
    return issues_url + "?" + "+".join(params)
