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
    
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    html_code = flask.render_template('index.html', username = username, admin = admin)
    response = flask.make_response(html_code)
    return response

@app.route('/courses', methods=['GET'])
def courses():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"

    html_code = flask.render_template('courses.html', admin = admin)
    response = flask.make_response(html_code)
    return response

@app.route('/learncourses', methods=['GET', 'POST'])
def learncourses():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
    
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    if request.method == 'POST':
        input_data = request.form['course_name']
    else:
        input_data = request.cookies.get('type', 'Default Value')
    html_code = flask.render_template('learncourses.html', type=input_data, admin = admin)
    response = flask.make_response(html_code)
    response.set_cookie('type', input_data)
    return response

@app.route('/learn', methods=['GET'])
def learn():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"

    html_code = flask.render_template('learn.html', admin = admin)
    response = flask.make_response(html_code)
    return response

@app.route('/admin', methods=['GET'])
def admin():
    username = auth.authenticate()
    userinfo = dbconnect.get_admin(username)
 
    if userinfo[1] == False:
        return flask.redirect('/index')
    html_code = flask.render_template('admin.html', admin = admin)
    response = flask.make_response(html_code)
    return response

@app.route('/add_card', methods=['POST'])
def add_card():
    print("enter")
    aslcourse = request.form.get('aslcourse')
    asllesson = request.form.get('asllesson')
    videolink = request.form.get('videolink')
    translation = request.form.get('translation')
    memory = request.form.get('memory')
    speech = request.form.get('speech')
    sentence = request.form.get('sentence')
    print(aslcourse)
    dbconnect.add_card( int(aslcourse), int(asllesson), videolink, translation, memory, speech, sentence)

    return flask.redirect('/admin')


@app.route('/searchterm', methods=['GET'])
def searchterm():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"

    html_code = flask.render_template('searchterm.html', admin = admin)
    response = flask.make_response(html_code)
    return response

@app.route('/searchterm/results', methods=['GET'])
def searchtermresults():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"

    input = request.args.get('query', default="")   
    query_result = dbconnect.get_terms(input)
    if query_result[0] is True:
        terms = query_result[1]
        terms_sorted = sorted(terms, key=lambda x: x['translation'])
        html_code = flask.render_template('tabledisplay.html', terms = terms_sorted)
    else: 
        html_code =    flask.render_template('index.html', admin = admin) 

        

    response = flask.make_response(html_code)
    return response


@app.route('/lessons', methods=['GET'])
def lessons():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"

    input = request.args.get('course', default=None)
        
    values = input.split()
    course = values[0]
    courseid = int(course[3:6])
    lessonid = values[1]

    query_result = dbconnect.get_flashcards(username, courseid, lessonid)
    if query_result[0] is True:
        flashcards = query_result[1]
        html_code = flask.render_template('lessons.html', course=course, 
        lesson_num = lessonid, flashcards = flashcards, admin = admin)
    else: 
        html_code = flask.render_template('index.html', admin = admin)
    
    
    response = flask.make_response(html_code)
    return response

@app.route('/lessons/results', methods=['GET'])
def searchlessonresults():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"

    input_query = request.args.get('query', default="")
    lesson_id = request.args.get('lessonid', default="")
    course_id = request.args.get('courseid', default="")
    
    query_result = dbconnect.get_lessonterms(input_query, lesson_id, course_id)
    if query_result[0] is True:
        terms = query_result[1]
        terms_sorted = sorted(terms, key=lambda x: x['translation'])
        html_code = flask.render_template('tabledisplay.html', terms=terms_sorted, lessonid=lesson_id, courseid=course_id)
    else: 
        html_code = flask.render_template('index.html', admin=admin)

    return html_code


@app.route('/selectlessons', methods=['GET'])
def selectlessons():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"
    course = request.args.get('course', default=None)
    
    html_code = flask.render_template('selectlessons.html', course=course,
        lesson_num = course_lessonsnum[course], admin = admin)
    response = flask.make_response(html_code)
    return response

@app.route('/learnselectlessons', methods=['GET'])
def learnselectlessons():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"

    course = request.args.get('course', default=None)
    if course is None:
        course = flask.request.cookies.get('lesson')
    type = flask.request.cookies.get('type')
    
    html_code = flask.render_template('learnselectlessons.html', course=course,
        lesson_num = course_lessonsnum[course], type = type, admin = admin)
    response = flask.make_response(html_code)
    response.set_cookie('type', type)
    response.set_cookie('lesson', course)
    return response



@app.route('/mirrorsign', methods=['GET'])
def mirrorsign():   
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"

    input = request.args.get('course', default=None)
    values = input.split()
    course = values[0]
    courseid = int(course[3:6])
    lessonid = values[1]

    query_result = dbconnect.get_flashcards(username, courseid, lessonid)
    if True is True:
        flashcards = query_result[1]
        empty = []
        if len(flashcards) != 0:
            empty=[1]
        html_code = flask.render_template('mirrorsign.html', flashcards = flashcards, admin = admin, empty=empty)
    else: 
        html_code = flask.render_template('index.html', admin = admin)
    
    
    response = flask.make_response(html_code)
    return response

@app.route('/quiz', methods=['GET'])
def quiz():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"

    input = request.args.get('value', default=None)
    values = input.split()
    course = values[0]
    courseid = int(course[3:6])
    lessonid = values[1]

    query_result = dbconnect.get_flashcards(username, courseid, lessonid)
    if True is True:
        flashcards = query_result[1]
        html_code = flask.render_template('quiz.html', 
            flashcards = flashcards, admin = admin)
    else: 
        html_code = flask.render_template('index.html', admin = admin)
    
    response = flask.make_response(html_code)
    return response

@app.route('/gloss', methods=['GET'])
def gloss():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"

    html_code = flask.render_template('gloss.html', admin = admin)
    response = flask.make_response(html_code)
    return response

@app.route('/review', methods=['GET'])
def review():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"
        
    query_result = dbconnect.get_starred_cards(username)

    if (query_result[0] == True):
        
        flashcards = query_result[1]
        empty = []
        if len(flashcards) != 0:
            empty=[1]
        html_code = flask.render_template('reviewstack.html', flashcards = flashcards, admin = admin, empty=empty)
        response = flask.make_response(html_code)
    else:
        return flask.redirect('/index')
    
    return response

@app.route('/mirrorquiz', methods=['GET'])
def mirrorquiz():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    
    admin = "false"
    if useradmin[1] == True:
        admin = "true"
       

    input = request.args.get('course', default=None)
    type = flask.request.cookies.get('type')
    
    if type == "Mirror Sign":
        values = input.split()
        course = values[0]
        courseid = int(course[3:6])
        lessonid = values[1]

        query_result = dbconnect.get_flashcards(username, courseid, lessonid)
        if True is True:
            flashcards = query_result[1]
            empty = []
            if len(flashcards) != 0:
                empty=[1]
            html_code = flask.render_template('mirrorsign.html', 
                flashcards = flashcards, type = type, admin = admin, empty = empty)
        else: 
            html_code = flask.render_template('index.html', admin = admin)
               
        response = flask.make_response(html_code)
        response.set_cookie('type', type)
    
    else: # type == "Quiz"
        values = input.split()
        course = values[0]
        courseid = int(course[3:6])
        lessonid = values[1]
        
        query_result = dbconnect.get_flashcards(username, courseid, lessonid)
        if True is True:
            flashcards = query_result[1]
            html_code = flask.render_template('quiz.html', 
                flashcards = flashcards, type = type, admin = admin)
        else:
            html_code = flask.render_template('index.html', admin = admin)
            
        response = flask.make_response(html_code)
        response.set_cookie('type', type)
    return response

    
    

@app.route('/deletestarredflashcard', methods=['PUT'])
def delstarflashcard():
        username = auth.authenticate()
        cardid =  request.get_json()["cardid"]
        result = dbconnect.del_starred_card(username, cardid)
        return result[1]
        
        

@app.route('/addstarredflashcard', methods=['PUT'])
def starflashcard(): 
     username = auth.authenticate()
     cardid =  request.get_json()["cardid"]
     result = dbconnect.add_starred_card(username, cardid)
     return result[1]
        

@app.route('/test', methods=['GET'])
def testhome():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username )
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"

    html_code = flask.render_template('sidebar.html', admin = admin)
    response = flask.make_response(html_code)
    return response



if __name__ == '__main__':
    app.run(debug=True)

