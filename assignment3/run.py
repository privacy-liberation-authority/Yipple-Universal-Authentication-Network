#!/usr/bin/env python3
import os, urllib
from markupsafe import Markup

from komradebank import create_app

app = create_app()

if __name__ == "__main__":

    # run flask server
    app.run(port=9447, host='0.0.0.0', debug=True)


# add url encode filter to app
@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.parse.quote_plus(s)
    return Markup(s)
