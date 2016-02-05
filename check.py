import requests

whitelist = [
    {
        'file': 'README.md',
        'msg': 'People really read this stuff'
    },
    {
        'file': 'LICENSE.TXT',
        'msg': 'Get an Open Source License buddy'
    },
    {
        'file': 'CONTRIBUTING.md',
        'msg': 'Dummy'
    },
    {
        'file': '.travis.yml',
        'msg': 'You should have CI stuff'
    }, {
        'file': '.gitignore',
        'msg': 'You should have this as well'
    },
]


class Repo:
    def __init__(self, owner, repo):
        self.repo = repo
        self.owner = owner
        self.files = None

    def get_contents(self):
        uri = "https://api.github.com/repos/%s/%s/contents" % (self.owner, self.repo)
        resp = requests.get(uri)

        if resp.status_code is not 200:
            print(resp.status_code)
            raise Exception
        else:
            self.files = [each['name'] for each in resp.json()]

    def check_file(self, file):
        return file in self.files


r = Repo("onyb", "cling")
r.get_contents()
for stuff in whitelist:
    print(stuff['file'], ':', r.check_file(stuff), ' - ', stuff['msg'])
