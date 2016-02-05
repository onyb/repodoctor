#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import redirect, Response

from webapp import webapp

import json

@webapp.route('/api/<owner>/<repo>')
def index(owner, repo):
    result = {
        'success': None,
        'warning': None,
        'error': None
    }
    return Response(json.dumps(result, indent=4), mimetype="application/json")
