#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import flask

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
@app.route('/<path:filename>')
def serve_static(filename):
    print(f"Requested filename: {filename}")
    if filename == 'css/card.css' or filename == 'js/card.js':
        return flask.send_from_directory('.', filename)
    else:
        flask.abort(404)


#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
