#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import redirect, Response

from webapp import webapp
from webapp.utils.check import RepoScanner

import json

@webapp.route('/api/<owner>/<repo>')
def index(owner, repo):
    r = RepoScanner(owner, repo)
    result = r.get_results()
    return Response(json.dumps(result, indent=4), mimetype="application/json")
