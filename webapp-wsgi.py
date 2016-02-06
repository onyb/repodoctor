import sys,os

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    from webapp import webapp
    from webapp import views
    webapp.run(debug=True, port=3000)
else:
    import sys
    #FIXME: Change hardcoded path
    sys.path.append(os.getcwd())
    from webapp import webapp
    from webapp import views
