#!/usr/bin/env python

import flask
from flask import request

app = flask.Flask(__name__, template_folder='.')

course_lessonsnum = {
    'ASL101': 14,
    'ASL102': 11,
    'ASL105': 8,
    'ASL107': 9
}


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

@app.route('/lessons', methods=['GET'])
def lessons():
    input = request.args.get('course', default=None)
    values = input.split()
    
    # Your existing code for rendering the template
    html_code = flask.render_template('lessons.html', course=values[0], 
        lesson_num = values[1])
    response = flask.make_response(html_code)
    return response


@app.route('/selectlessons', methods=['GET'])
def selectlessons():
    course = request.args.get('course', default=None)
    
    # Your existing code for rendering the template
    html_code = flask.render_template('selectlessons.html', course=course,
        lesson_num = course_lessonsnum[course])
    response = flask.make_response(html_code)
    return response

if __name__ == '__main__':
    app.run(debug=True)
