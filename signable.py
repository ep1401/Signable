#!/usr/bin/env python

import flask
import os
from flask import request
from flask import send_file
import dbconnect
import auth
import dotenv

app = flask.Flask(__name__, template_folder='.')
_DATABASE_URL = os.environ['DATABASE_URL']
dotenv.load_dotenv()
app.secret_key = os.environ['APP_SECRET_KEY']

course_lessonsnum = {
    'ASL101': 14,
    'ASL102': 11,
    'ASL105': 8,
    'ASL107': 9
}

@app.route('/login', methods=['GET'])
def login():
    return auth.login()

@app.route('/login/callback', methods=['GET'])
def callback():
    return auth.callback()

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()

@app.route('/logoutgoogle', methods=['GET'])
def logoutgoogle():
    return auth.logoutgoogle()

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    html_code = flask.render_template('index.html', username = username)
    response = flask.make_response(html_code)
    return response

@app.route('/courses', methods=['GET'])
def courses():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    html_code = flask.render_template('courses.html')
    response = flask.make_response(html_code)
    return response

@app.route('/learncourses', methods=['GET', 'POST'])
def learncourses():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    if request.method == 'POST':
        input_data = request.form['course_name']
    else:
        input_data = request.cookies.get('type', 'Default Value')
    html_code = flask.render_template('learncourses.html', type=input_data)
    response = flask.make_response(html_code)
    response.set_cookie('type', input_data)
    return response

@app.route('/learn', methods=['GET'])
def learn():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    html_code = flask.render_template('learn.html')
    response = flask.make_response(html_code)
    return response

@app.route('/searchterm', methods=['GET'])
def searchterm():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    html_code = flask.render_template('searchterm.html')
    response = flask.make_response(html_code)
    return response

@app.route('/searchterm/results', methods=['GET'])
def searchtermresults():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
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
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
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
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    course = request.args.get('course', default=None)
    
    html_code = flask.render_template('selectlessons.html', course=course,
        lesson_num = course_lessonsnum[course])
    response = flask.make_response(html_code)
    return response

@app.route('/learnselectlessons', methods=['GET'])
def learnselectlessons():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    course = request.args.get('course', default=None)
    type = flask.request.cookies.get('type')
    
    html_code = flask.render_template('learnselectlessons.html', course=course,
        lesson_num = course_lessonsnum[course], type = type)
    response = flask.make_response(html_code)
    response.set_cookie('type', type)
    return response



@app.route('/mirrorsign', methods=['GET'])
def mirrorsign():   
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    input = request.args.get('course', default=None)
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
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
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
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    html_code = flask.render_template('gloss.html')
    response = flask.make_response(html_code)
    return response

@app.route('/review', methods=['GET'])
def review():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    input = "ASL101 1"
        
    values = input.split()
    course = values[0]
    courseid = int(course[3:6])
    lessonid = values[1]

    query_result = dbconnect.get_flashcards(courseid, lessonid)
    flashcards = query_result[1]
    html_code = flask.render_template('reviewstack.html', flashcards = flashcards)
    response = flask.make_response(html_code)
    return response

@app.route('/mirrorquiz', methods=['GET'])
def mirrorquiz():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    input = request.args.get('course', default=None)
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
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username )
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    html_code = flask.render_template('sidebar.html')
    response = flask.make_response(html_code)
    return response

if __name__ == '__main__':
    app.run(debug=True)
