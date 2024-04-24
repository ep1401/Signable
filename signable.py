#!/usr/bin/env python

import flask
import os
from flask import request
from flask import render_template
import dbconnect
import auth
import dotenv

app = flask.Flask(__name__, template_folder='.')
_DATABASE_URL = os.environ['DATABASE_URL']
dotenv.load_dotenv()
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route('/', methods=['GET'])
def start_page():
    return render_template('startpage.html')

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

@app.route('/home', methods=['GET'])
def home():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
    
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
    html_code = flask.render_template('home.html', username = username, admin = admin)
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
        return flask.redirect('/home')
    
    asl101len = dbconnect.get_lessonlength(101)
    asl102len = dbconnect.get_lessonlength(102)
    asl105len = dbconnect.get_lessonlength(105)
    asl107len = dbconnect.get_lessonlength(107)
    terms = dbconnect.get_lessonterms('', 2, 101)
    
    if asl101len[0] is True and asl102len[0] is True and asl105len[0] is True and asl107len[0] is True:
        lesson_length101 = len(asl101len[1])
        lesson_length102 = len(asl102len[1])
        lesson_length105 = len(asl105len[1])
        lesson_length107 = len(asl107len[1])
        html_code = flask.render_template('admin.html', admin = admin, asl101len = lesson_length101, 
            asl102len = lesson_length102, asl105len = lesson_length105, asl107len = lesson_length107, terms = terms[1])
    else: 
        html_code = flask.render_template('home.html', admin = admin)
        
    response = flask.make_response(html_code)
    return response

@app.route('/add_card', methods=['POST'])
def add_card():
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
        html_code =    flask.render_template('home.html', admin = admin) 

        

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

    input = request.args.get('course_lesson', default=None)
        
    values = input.split()
    course = values[0]
    lessonid = values[1]

    query_result = dbconnect.get_flashcards(username, course, lessonid)
    if query_result[0] is True:
        flashcards = query_result[1]
        empty = False
        if (len(flashcards) == 0):
            empty = True
        html_code = flask.render_template('lessons.html', course=course, 
        lesson_num = lessonid, flashcards = flashcards, admin = admin, empty = empty)
    else:
        html_code = flask.render_template('home.html', admin = admin)
    
    
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
        html_code = flask.render_template('home.html', admin=admin)

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
    
    query_result = dbconnect.get_lessonlength(course)
    if query_result[0] is True:
        lesson_length = query_result[1]
        html_code = flask.render_template('selectlessons.html', course=course,
        lesson_num = len(lesson_length), admin = admin)
    else: 
        html_code = flask.render_template('home.html', admin = admin)

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
    
    query_result = dbconnect.get_lessonlength(int(course[3:6]))
    if query_result[0] is True:
        lesson_length = query_result[1]
        html_code = flask.render_template('learnselectlessons.html', course=course,
        lesson_num = len(lesson_length), type = type, admin = admin)
    else: 
        html_code = flask.render_template('home.html', admin = admin)

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

    input = request.args.get('course_lesson', default=None)
    values = input.split()
    course = values[0]
    lessonid = values[1]

    query_result = dbconnect.get_flashcards(username, course, lessonid)
    if query_result[0] is True:
        flashcards = query_result[1]
        empty = []
        if len(flashcards) != 0:
            empty=[1]
        html_code = flask.render_template('mirrorsign.html', course = course, lesson_num = lessonid,
            flashcards = flashcards, admin = admin, empty=empty)
    else: 
        html_code = flask.render_template('home.html', admin = admin)
    
    
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

    input = request.args.get('course_lesson', default=None)
    values = input.split()
    course = values[0]
    lessonid = values[1]

    query_result = dbconnect.get_flashcards(username, course, lessonid)
    if query_result[0] is True:
        flashcards = query_result[1]
        html_code = flask.render_template('quiz.html', course = course, lesson_num = lessonid, 
            flashcards = flashcards, admin = admin)
    else: 
        html_code = flask.render_template('home.html', admin = admin)
    
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
        return flask.redirect('/home')
    
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

@app.route('/savechanges', methods=['POST'])
def save_changes():
    data = request.get_json()
    success_messages = []
    error_messages = []

    # Loop through data and update database accordingly
    for item in data:
        card_id = item['cardid']
        translation = item['translation']
        memorytip = item['memorytip']
        speech = item['speech']
        sentence = item['sentence']
        
        # Call the update_flashcard function to update the flashcard
        success, message = dbconnect.update_flashcard(card_id, translation, memorytip, speech, sentence)
        
        if success:
            success_messages.append(message)
        else:
            error_messages.append(message)

    if error_messages:
        return flask.jsonify({'success': False, 'errors': error_messages}), 500
    else:
        return flask.jsonify({'success': True, 'messages': success_messages})

@app.route('/deleteflashcard', methods=['POST'])
def deleteflashcard():
    data = request.get_json()
    card_id = data.get('cardid')

    if card_id is None:
        return flask.jsonify({'success': False, 'error': 'Card ID not provided'}), 400

    # Call the delete_flashcard function to delete the flashcard
    success, message = dbconnect.delete_flashcard(card_id)
    if success:
        return flask.jsonify({'success': True, 'message': message}), 200
    else:
        return flask.jsonify({'success': False, 'error': message}), 500
    
@app.route('/fetch-lesson-terms/<int:course_id>/<int:lesson_number>')
def fetch_lesson_terms(course_id, lesson_number):
    # Call dbconnect.get_lessonterms() to fetch the data
    terms = dbconnect.get_lessonterms('', lesson_number, course_id)
    # Convert the data to a JSON format and return it
    return flask.jsonify(terms[1])

@app.route('/learningcenter', methods=['GET'])
def learningcenter():
    username = auth.authenticate()
    userinfo = dbconnect.get_user(username)
 
    if userinfo[1] == False:
        dbconnect.add_user(username, "", "")
        
    useradmin = dbconnect.get_admin(username)
    admin = "false"
    if useradmin[1] == True:
        admin = "true"

    input = request.args.get('course_lesson', default=None)
        
    values = input.split()
    course = values[0]
    lessonid = values[1]

    html_code = flask.render_template('learningcenter.html', course=course, 
        lesson_num = lessonid,  admin = admin)
    
    
    response = flask.make_response(html_code)
    return response



if __name__ == '__main__':
    app.run(debug=True)

