#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from pprint import pprint

import requests

CHECK_META = {
    'F00': {
        'name': 'README.md',
        'msg': "A README.md is the first thing a user sees. If you do not have this, you should die already.",
        'severity': 2
    },
    'F01': {
        'name': 'LICENSE',
        'msg': 'Head over to http://choosealicense.com and choose the right license for you.',
        'severity': 2
    },
    'F02': {
        'name': 'CONTRIBUTING.md',
        'msg': 'Contributor guidelines for developers and newcomers.',
        'severity': 1
    },
    'F03': {
        'name': 'Travis CI integration',
        'msg': 'Travis CI is a Continuous integration platform for open source projects, letting your users check build the status.',
        'severity': 1
    },
    'F04': {
        'name': 'Gitignore file',
        'msg': 'Absence of a .gitignore file may pose a security risk. Head over to https://www.gitignore.io',
        'severity': 2
    },
    'C01': {
        'name': 'README.md length',
        'msg': 'You have a README.md file, but it is too little to be useful.',
        'severity': 1
    },
    'C02': {
        'name': 'Travis CI build status',
        'msg': 'Your Travis CI builds are failing.',
        'severity': 2
    },
    'C03': {
        'name': 'Project test suite',
        'msg': 'You do not have a test suite on your top-level directory',
        'severity': 1
    },
    'C04': {
        'name': 'GitHub milestones',
        'msg': 'Your GitHub repo does not have milestones. Milestones help you to prioritize and accelerate development.',
        'severity': 1
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

        return {
            'ID': CHECK_ID,
            'status': readme.count('\n') >= 2,
            'name': CHECK_META[CHECK_ID]['name']
        }

    def check_build_status(self):
        CHECK_ID = 'C02'
        return {
            'ID': CHECK_ID,
            'status': requests.get(
                "https://api.travis-ci.org/repositories/%s/%s.json" % (self.owner, self.repo)
            ).json()['last_build_status'] is 0,
            'name': CHECK_META[CHECK_ID]['name']
        }

    def check_test(self):
        CHECK_ID = 'C03'
        return {
            'ID': CHECK_ID,
            'status': 'test' in self.contents or 'tests' in self.contents,
            'name': CHECK_META[CHECK_ID]['name']
        }

    def check_milestones(self):
        CHECK_ID = 'C04'
        uri = "https://api.github.com/repos/%s/%s/milestones" % (self.owner, self.repo)
        return {
            'ID': CHECK_ID,
            'status': requests.get(uri).json() != [],
            'name': CHECK_META[CHECK_ID]['name']
        }

    def get_results(self):
        self.get_contents()
        _results = []
        for check in whitelist:
            _results.append(
                {
                    'ID': check['CHECK_ID'],
                    'name': CHECK_META[check['CHECK_ID']]['name'],
                    'status': self.check_file(check['file'])
                }
            )

        _results.append(
            self.check_build_status()
        )

        _results.append(
            self.check_test()
        )

        _results.append(
            self.check_readme_len()
        )

        _results.append(
            self.check_milestones()
        )

        for result in _results:
            if result['status'] is False:
                meta = CHECK_META[result['ID']]
                result['msg'] = meta['msg']
                result['severity'] = meta['severity']

        return _results
