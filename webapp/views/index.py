#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, redirect

from repodoctor.webapp import webapp


@webapp.route('/')
def index():
    return render_template('index.html')
