#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen

import requests

from pprint import pprint

CHECK_META = {
    'F00': {
        'msg': "A README.md is the first thing a user sees. If you do not have this, you should die already.",
        'severity': 2
    },
    'F01': {
        'msg': 'Head over to http://choosealicense.com and choose the right license for you.',
        'severity': 2
    },
    'F02': {
        'msg': 'Contributor guidelines for developers and newcomers.',
        'severity': 1,
    },
    'F03': {
        'msg': 'Travis CI is a Continuous integration platform for open source projects, letting your users check build the status.',
        'severity': 1,
    },
    'F04': {
        'msg': 'Absence of a .gitignore file may pose a security risk. Head over to https://www.gitignore.io',
        'severity': 2,
    },
    'C01': {
        'msg': 'You have a README.md file, but it is too little to be useful.',
        'severity': 1,
    },
    'C02': {
        'msg': 'Your Travis CI builds are failing.',
        'severity': 2,
    },
    'C03': {
        'msg': 'You do not have a test suite on your top-level directory',
        'severity': 1,
    },
    'C04': {
        'msg': 'Your GitHub repo does not have milestones. Milestones help you to prioritize and accelerate development.',
        'severity': 1,
    }
}

whitelist = [
    {
        'file': 'README.md',
        'CHECK_ID': 'F00'
    },
    {
        'file': 'LICENSE',
        'CHECK_ID': 'F01'
    },
    {
        'file': 'CONTRIBUTING.md',
        'CHECK_ID': 'F02'
    },
    {
        'file': '.travis.yml',
        'CHECK_ID': 'F03'
    }, {
        'file': '.gitignore',
        'CHECK_ID': 'F04'
    },
]

class APILimitExceeded(Exception):
    pass

class RepoScanner:
    def __init__(self, owner, repo):
        self.repo = repo
        self.owner = owner
        self.contents = None

    def get_contents(self):
        uri = "https://api.github.com/repos/%s/%s/contents" % (self.owner, self.repo)
        resp = requests.get(uri)

        if resp.status_code is 403:
            raise APILimitExceeded
        elif resp.status_code is 200:
            self.contents = [each['name'] for each in resp.json()]


    def check_file(self, file):
        return file in self.contents

    def check_readme_len(self):
        CHECK_ID = 'C01'
        readme = urlopen(
            "https://raw.githubusercontent.com/%s/%s/master/README.md" % (self.owner, self.repo)
        ).read().strip().decode('utf-8')

        if readme.count('\n') <= 2:
            return {CHECK_ID: False}
        else:
            return {CHECK_ID: True}

    def check_build_status(self):
        CHECK_ID = 'C02'
        return {CHECK_ID: requests.get(
            "https://api.travis-ci.org/repositories/%s/%s.json" % (self.owner, self.repo)
        ).json()['last_build_status'] is 0}

    def check_test(self):
        CHECK_ID = 'C03'
        return {CHECK_ID: 'test' in self.contents or 'tests' in self.contents}

    def check_milestones(self):
        CHECK_ID = 'C04'
        uri = "https://api.github.com/repos/%s/%s/milestones" % (self.owner, self.repo)
        return {CHECK_ID: requests.get(uri).json() != []}


r = RepoScanner("onyb", "cling")
r.get_contents()
_results = []
for check in whitelist:
    _results.append(
        {
            check['CHECK_ID']: r.check_file(check['file'])
        }
    )

_results.append(
    r.check_build_status()
)

_results.append(
    r.check_test()
)

_results.append(
    r.check_readme_len()
)

_results.append(
    r.check_milestones()
)

for result in _results:
    if list(result.values())[0] is False:
        meta = CHECK_META[list(result.keys())[0]]
        result['msg'] = meta['msg']
        result['severity'] = meta['severity']

pprint(_results)
