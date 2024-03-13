#!/usr/bin/env python

import flask
from flask import request
from flask import send_file

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
    
    # Your existing code for rendering the template
    html_code = flask.render_template('lessons.html', course=values[0], 
        lesson_num = values[1], cards = cards)
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


if __name__ == '__main__':
    app.run(debug=True)
