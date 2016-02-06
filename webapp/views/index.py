#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import redirect, Response, render_template

from webapp import webapp
from webapp.utils.check import RepoScanner

import json

@webapp.route('/api/<owner>/<repo>')
def api(owner, repo):
    r = RepoScanner(owner, repo)
    result = r.get_results()
    return Response(json.dumps(result, indent=4), mimetype="application/json")

@webapp.route('/<owner>/<repo>')
def index(owner, repo):
    r = RepoScanner(owner, repo)
    results = r.get_results()
    return render_template(
        'index.html',
        results=results
    )

@webapp.route('/badge/<owner>/<repo>')
def badge(owner, repo):
    r = RepoScanner(owner, repo)
    results = r.get_results()

    for each in results:
        if each['status'] is False and each['severity'] is 2:
            return redirect("https://img.shields.io/badge/repodoctor-Error-red.svg")
