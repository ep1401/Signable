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

cards = [
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO1',
            'id': 1,
            'mem': "Think of a salute",
            'speach': "noun",
            'sentence': "When I walked in he told me hello"
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO2',
            'id': 2,
            'mem': "Think of a salute",
            'speach': "noun",
            'sentence': "When I walked in he told me hello"
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO3',
            'id': 3,
            'mem': "Think of a salute",
            'speach': "noun",
            'sentence': "When I walked in he told me hello"
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO4',
            'id': 4,
            'mem': "Think of a salute",
            'speach': "noun",
            'sentence': "When I walked in he told me hello"
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO5',
            'id': 5,
            'mem': "Think of a salute",
            'speach': "noun",
            'sentence': "When I walked in he told me hello"
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO6',
            'id': 6,
            'mem': "Think of a salute",
            'speach': "noun",
            'sentence': "When I walked in he told me hello"
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO7',
            'id': 7,
            'mem': "Think of a salute",
            'speach': "noun",
            'sentence': "When I walked in he told me hello"
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO8',
            'id': 8,
            'mem': "Think of a salute",
            'speach': "noun",
            'sentence': "When I walked in he told me hello"
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO9',
            'id': 9,
            'mem': "Think of a salute",
            'speach': "noun",
            'sentence': "When I walked in he told me hello"
        }
    ]

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
    course = values[0]
    courseid = int(course[3:6])
    lessonid = values[1]

    query_result = dbconnect.get_flashcards(courseid, lessonid)
    if query_result[0] is True:
        flashcards = query_result[1]
        html_code = flask.render_template('lessons.html', course=course, 
        lesson_num = lessonid, flashcardscards = flashcards)
    else: 
        html_code = flask.render_template('index.html')
    
    
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

@app.route('/get_shuffle', methods=['GET'])
def get_shuffle():
    return send_file("shuffle.png")

@app.route('/get_logo', methods=['GET'])
def get_logo():
    return send_file("logo.png")

@app.route('/get_arrowleft', methods=['GET'])
def get_arrowleft():
    return send_file("arrowleft.png")

@app.route('/get_arrowright', methods=['GET'])
def get_arrowright():
    return send_file("arrowright.png")

@app.route('/get_flip', methods=['GET'])
def get_flip():
    return send_file("flip.png")

@app.route('/get_full', methods=['GET'])
def get_full():
    return send_file("full.png")

@app.route('/get_info', methods=['GET'])
def get_info():
    return send_file("info.png")

@app.route('/get_mirror', methods=['GET'])
def get_mirror():
    return send_file("mirror.png")

@app.route('/get_star', methods=['GET'])
def get_star():
    return send_file("star.png")

@app.route('/mirrorsign', methods=['GET'])
def mirrorsign():   
    # Your existing code for rendering the template
    cards = [
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO1',
            'id': 1
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO2',
            'id': 2
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO3',
            'id': 3
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO4',
            'id': 4
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO5',
            'id': 5
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO6',
            'id': 6
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO7',
            'id': 7
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO8',
            'id': 8
        },
        {
            'front': '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/NXRzRZFgSco" frameborder="0" allowfullscreen></iframe>',
            'back': 'HELLO9',
            'id': 9
        }
    ]
    html_code = flask.render_template('mirrorsign.html', cards = cards)
    response = flask.make_response(html_code)
    return response

if __name__ == '__main__':
    app.run(debug=True)
