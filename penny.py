#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import flask

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.', static_url_path='/static', static_folder='static')


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response



#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/lessons', methods=['GET'])
def index():
    html_code = flask.render_template('lessons.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------



#-----------------------------------------------------------------------

