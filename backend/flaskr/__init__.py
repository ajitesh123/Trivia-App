import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type = int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions_list = [question.format() for question in selection]
    current_questions = questions_list[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={'/': {"origins": "*"}})
    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        selection = Category.query.all()
        category_dict = {}
        for category in selection:
            category_dict[category.format()['id']] = category.format()['type']

        if len(category_dict)==0:
            abort(404)

        return jsonify({
            'categories': category_dict
        }), 200

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.all()
        category_dict = {}
        for category in categories:
            category_dict[category.format()['id']] = category.format()['type']

        current_categories = list(set([question['category'] for question in current_questions]))

        totalQuestions = len(Question.query.all())

        return jsonify({
            'questions': current_questions,
            'total_questions': totalQuestions,
            'categories': category_dict,
            'current_category': current_categories
        }), 200

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()

            if question is None:
                return abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })

        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_questions():
        '''Endpoint to POST a new question using method "POST" '''
        body = request.get_json()

        question_s = body.get('question', None)
        answer_s = body.get('answer', None)
        difficulty_s = body.get('difficulty', None)
        category_s = body.get('category', None)

        if any(len(elem)==0 for elem in [question_s, answer_s]):
            abort(400)
        if difficulty_s is None or category_s is None:
            abort(400)

        try:
            question = Question(
            question = question_s,
            answer = answer_s,
            difficulty = difficulty_s,
            category = category_s)

            question.insert()

            return jsonify({
                'success': True
            })

        except:
            abort(422)

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions/search', methods = ['POST'])
    def search_questions():
        body = request.get_json()

        search = body.get('searchTerm', None)

        try:
            selection = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search))).all()
            current_questions = paginate_questions(request, selection)

            current_categories = list(set([question['category'] for question in current_questions]))

            return jsonify({
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': current_categories
                })
        except:
            abort(404)

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''


    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    return app
