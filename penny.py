#!/usr/bin/env python

import flask
import os
from flask import request
from flask import send_file
import dbconnect
import auth



app = flask.Flask(__name__, template_folder='.')
_DATABASE_URL = os.environ['DATABASE_URL']

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
    auth.authenticate()
    input = request.args.get('course', default=None)
    values = input.split()
    course = values[0]
    courseid = int(course[3:6])
    lessonid = values[1]

    query_result = dbconnect.get_flashcards(courseid, lessonid)
    if query_result[0] is True:
        flashcards = query_result[1]
        html_code = flask.render_template('lessons.html', course=course, 
        lesson_num = lessonid, flashcards = flashcards)
    else: 
        html_code = flask.render_template('index.html')
    
    
    response = flask.make_response(html_code)
    return response


@app.route('/selectlessons', methods=['GET'])
def selectlessons():
    auth.authenticate()
    course = request.args.get('course', default=None)
    
    # Your existing code for rendering the template
    html_code = flask.render_template('selectlessons.html', course=course,
        lesson_num = course_lessonsnum[course])
    response = flask.make_response(html_code)
    return response



@app.route('/mirrorsign', methods=['GET'])
def mirrorsign():   
    # Your existing code for rendering the template
    auth.authenticate()
    input = request.args.get('mirror', default=None)
    values = input.split()
    course = values[0]
    courseid = int(course[3:6])
    lessonid = values[1]

    query_result = dbconnect.get_flashcards(courseid, lessonid)
    if True is True:
        flashcards = query_result[1]
        html_code = flask.render_template('mirrorsign.html', flashcards = flashcards)
    else: 
        html_code = flask.render_template('index.html')
    
    
    response = flask.make_response(html_code)
    return response
   
    

if __name__ == '__main__':
    app.run(debug=True)
