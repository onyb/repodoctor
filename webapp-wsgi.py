if __name__ == "__main__":
    from repomixer.webapp import webapp
    from repomixer.webapp import views
    webapp.run(debug=True, port=3000)
else:
    import sys
    #FIXME: Change hardcoded path
    sys.path.append('/home/ani/repos/onyb/repomixer')
    from repomixer.webapp import webapp
    from repomixer.webapp import views
