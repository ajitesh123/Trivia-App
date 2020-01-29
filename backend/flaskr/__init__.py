import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    '''Creates list of 10 questions per page'''
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
    #Allows request from any website
    CORS(app, resources={'/': {"origins": "*"}})


    @app.after_request
    def after_request(response):
        '''Defines access control headers and methods'''
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        '''Serves categories of questions.'''
        selection = Category.query.all()
        category_dict = {}
        for category in selection:
            category_dict[category.format()['id']] = category.format()['type']

        #In case no category exist, display error message
        if len(category_dict)==0:
            abort(404)

        return jsonify({
            'categories': category_dict
        }), 200

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        '''Handles GET request to serves paginated questions'''
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

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        '''Allows questions to be deleted by question_id'''
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()

            #In case no such question exist, then informt resource doesn't exist
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


    @app.route('/questions/search', methods = ['POST'])
    def search_questions():
        body = request.get_json()

        search = body.get('searchTerm', None)

        try:
            selection = Question.query.order_by(Question.id).\
                        filter(Question.question.ilike("%{}%".\
                        format(search))).all()

            current_questions = paginate_questions(request, selection)

            current_categories = list(set([question['category'] for question in current_questions]))

            return jsonify({
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': current_categories
                })
        except:
            abort(404)


    @app.route('/categories/<int:category_id>/questions', methods = ['GET'])
    def get_category_questions(category_id):
        try:
            if category_id==None:
                abort(400)

            selection = Question.query.filter(Question.category==category_id).all()
            current_questions = paginate_questions(request, selection)

            current_category = Category.query.filter(Category.id==category_id).\
                                all()[0].format()["type"]

            if len(selection)==0:
                abort(404)

            return jsonify({
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': current_category,
            })
        except:
            abort(404)


    @app.route('/quizzes', methods = ['POST'])
    def start_quiz():
        body = request.get_json()
        try:
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)

            if previous_questions is None or quiz_category is None:
                abort(400)

            category_id = quiz_category["id"]

            if category_id==0:
                selection = Question.query.all()
            else:
                selection = Question.query.filter(Question.category==category_id).all()

            question_repo = list(filter(lambda q: (q.id not in previous_questions), selection))
            formatted_repo = [question.format() for question in question_repo]

            if len(formatted_repo)==0:
                next_question = None
            else:
                next_question = random.choice(formatted_repo)

            return jsonify({
                'question': next_question
            })

        except:
            abort(422)

#---------------------------------------------------
#  Error Handler
#----------------------------------------------------

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Not found"
            }), 404

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
        'success': False,
        'error': 400,
        'message': "Bad request"
        }), 400

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
        'success': False,
        'error': 422,
        'message': "Unprocessable"
        }), 422

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
        'success': False,
        'error': 405,
        'message': "Method now allowed"
        }), 405

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
        'success': False,
        'error': 405,
        'message': "Method now allowed"
        }), 405

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
        'success': False,
        'error': 500,
        'message': "Internal server error"
        }), 500
#------------------------------------------------
    return app
