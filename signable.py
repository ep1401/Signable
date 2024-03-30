#!/usr/bin/env python

import flask
import os
from flask import request
from flask import send_file
import dbconnect

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

@app.route('/courses', methods=['GET'])
def courses():
    html_code = flask.render_template('courses.html')
    response = flask.make_response(html_code)
    return response

@app.route('/learncourses', methods=['GET'])
def learncourses():
    input = request.args.get('type')
    if input is None:
        input = flask.request.cookies.get('type')
    html_code = flask.render_template('learncourses.html', type = input)
    response = flask.make_response(html_code)
    response.set_cookie('type', input)
    return response

@app.route('/learn', methods=['GET'])
def learn():
    html_code = flask.render_template('learn.html')
    response = flask.make_response(html_code)
    return response

@app.route('/searchterm', methods=['GET'])
def searchterm():
    html_code = flask.render_template('searchterm.html')
    response = flask.make_response(html_code)
    return response

@app.route('/searchterm/results', methods=['GET'])
def searchtermresults():
    input = request.args.get('query', default="")   
    query_result = dbconnect.get_terms(input)
    if query_result[0] is True:
        terms = query_result[1]
        terms_sorted = sorted(terms, key=lambda x: x['translation'])
        html_code = flask.render_template('tabledisplay.html', terms = terms_sorted)
    else: 
        html_code =    flask.render_template('index.html') 

        

    response = flask.make_response(html_code)
    return response


@app.route('/lessons', methods=['GET'])
def lessons():
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
    
    course = request.args.get('course', default=None)
    
    html_code = flask.render_template('selectlessons.html', course=course,
        lesson_num = course_lessonsnum[course])
    response = flask.make_response(html_code)
    return response

@app.route('/learnselectlessons', methods=['GET'])
def learnselectlessons():
    
    course = request.args.get('course', default=None)
    type = flask.request.cookies.get('type')
    
    html_code = flask.render_template('learnselectlessons.html', course=course,
        lesson_num = course_lessonsnum[course], type = type)
    response = flask.make_response(html_code)
    response.set_cookie('type', type)
    return response



@app.route('/mirrorsign', methods=['GET'])
def mirrorsign():   
   
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

@app.route('/quiz', methods=['GET'])
def quiz():
    input = request.args.get('value', default=None)
    values = input.split()
    course = values[0]
    courseid = int(course[3:6])
    lessonid = values[1]

    query_result = dbconnect.get_flashcards(courseid, lessonid)
    if True is True:
        flashcards = query_result[1]
        html_code = flask.render_template('quiz.html', 
            flashcards = flashcards)
    else: 
        html_code = flask.render_template('index.html')
    
    response = flask.make_response(html_code)
    return response

@app.route('/gloss', methods=['GET'])
def gloss():
    html_code = flask.render_template('gloss.html')
    response = flask.make_response(html_code)
    return response

@app.route('/review', methods=['GET'])
def review():
    html_code = flask.render_template('reviewstack.html')
    response = flask.make_response(html_code)
    return response

@app.route('/mirrorquiz', methods=['GET'])
def mirrorquiz():
    input = request.args.get('value', default=None)
    type = flask.request.cookies.get('type')
    
    if type == "Mirror Sign":
        values = input.split()
        course = values[0]
        courseid = int(course[3:6])
        lessonid = values[1]

        query_result = dbconnect.get_flashcards(courseid, lessonid)
        if True is True:
            flashcards = query_result[1]
            html_code = flask.render_template('mirrorsign.html', 
                flashcards = flashcards, type = type)
        else: 
            html_code = flask.render_template('index.html')
               
        response = flask.make_response(html_code)
        response.set_cookie('type', type)
    
    else: # type == "Quiz"
        values = input.split()
        course = values[0]
        courseid = int(course[3:6])
        lessonid = values[1]
        
        query_result = dbconnect.get_flashcards(courseid, lessonid)
        if True is True:
            flashcards = query_result[1]
            html_code = flask.render_template('quiz.html', 
                flashcards = flashcards, type = type)
        else: 
            html_code = flask.render_template('index.html')
            
        response = flask.make_response(html_code)
        response.set_cookie('type', type)
    return response

@app.route('/test', methods=['GET'])
def testhome():
    html_code = flask.render_template('sidebar.html')
    response = flask.make_response(html_code)
    return response

if __name__ == '__main__':
    app.run(debug=True)
