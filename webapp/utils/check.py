#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen

import requests

whitelist = [
    {
        'file': 'README.md',
        'msg': 'People really read this stuff'
    },
    {
        'file': 'LICENSE',
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
        self.contents = None

    def get_contents(self):
        uri = "https://api.github.com/repos/%s/%s/contents" % (self.owner, self.repo)
        resp = requests.get(uri)

        if resp.status_code is not 200:
            print(resp.status_code)
            raise Exception
        else:
            self.contents = [each['name'] for each in resp.json()]

    def check_file(self, file):
        return file in self.contents

    def check_readme(self):
        readme = urlopen(
            "https://raw.githubusercontent.com/%s/%s/master/README.md" % (self.owner, self.repo)
        ).read().strip().decode('utf-8')

        if readme.count('\n') <= 2:
            raise Exception("Useless README.md")
        else:
            return True

    def check_build(self):
        return requests.get(
            "https://api.travis-ci.org/repositories/%s/%s.json" % (self.owner, self.repo)
        ).json()['last_build_status'] is 0

    def check_test(self):
        return 'test' in self.contents or 'tests' in self.contents

    def check_milestones(self):
        uri = "https://api.github.com/repos/%s/%s/milestones" % (self.owner, self.repo)
        return requests.get(uri).json() != []


r = Repo("onyb", "cling")
r.get_contents()
for stuff in whitelist:
    print(stuff['file'], ':', r.check_file(stuff['file']), '-', stuff['msg'])

assert r.check_build() is True
assert r.check_test()
assert r.check_readme() is True
assert r.check_milestones() is False  # FIXME: Temporary hack
