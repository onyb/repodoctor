import sys

if __name__ == "__main__":
    sys.path.append('/home/ani/repos/onyb/repodoctor')
    from webapp import webapp
    from webapp import views
    webapp.run(debug=True, port=3000)
else:
    import sys
    #FIXME: Change hardcoded path
    sys.path.append('/home/ani/repos/onyb/repodoctor')
    from webapp import webapp
    from webapp import views
