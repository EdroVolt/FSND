import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def pagination(request, formatted_questions):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return formatted_questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app)

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories', methods=['GET'])
    def show_all_categories():

        try:
            categories = Category.query.all()
            categories_formatted = {
                category.id: category.type for category in categories}
            return jsonify({
                'success': True,
                'categories': categories_formatted,
                'total_categories': len(categories)
            })
        except:
            abort(500)

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
    def show_questions():

        try:
            questions = Question.query.order_by(Question.id).all()
            formatted_questions = [question.format() for question in questions]

            paginated_questions = pagination(request, formatted_questions)

            categories = Category.query.order_by(Category.id).all()
            categories_formatted = {
                category.id: category.type for category in categories}
        except:
            abort(500)

        if paginated_questions == []:
            abort(404)

        else:
            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(questions),
                'categories': categories_formatted,
                'current_category': None
            })

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id).first()
        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted_question': question.format()
            })
        except:
            abort(404)

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def creat_new_question():
        data = request.json

        print(data)
        question = data.get('question')
        answer = data.get('answer')

        if question == '' or answer == '':
            abort(400)
        else:
            category = data.get('category')
            difficulty = data.get('difficulty')
            try:
                new_question = Question(question, answer, category, difficulty)
                new_question.insert()
                return jsonify({
                    'success': True,
                    'new_question': new_question.format(),
                })
            except:
                abort(500)

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_for_questions():
        try:
            search_term = request.json.get('searchTerm')
        except:
            abort(400)
        try:
            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            formatted_questions = [question.format() for question in questions]

            categories = Category.query.order_by(Category.id).all()
            categories_formatted = {
                category.id: category.type for category in categories}

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(questions),
                'categories': categories_formatted,
                'current_category': None
            })
        except:
            abort(500)

    '''
  @TODO:
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_by_category(id):
        try:
            questions = Question.query.filter_by(category=str(id)).all()
            formatted_questions = [question.format() for question in questions]

            current_category = Category.query.filter_by(id=id).first()

            data = {
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(questions),
                'current_category': current_category.type
            }

            return jsonify(data)
        except:
            abort(404)

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
    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        data = request.json

        if 'previous_questions' not in data or 'quiz_category' not in data:
            abort(400)
        try:
            previous_questions = data.get('previous_questions')
            quiz_category = data.get('quiz_category')

            if quiz_category.get('id') == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(
                    Question.category == str(quiz_category.get('id')), Question.id.notin_(previous_questions)).all()

            if len(questions) == 0:
                random_question = False
            else:
                formatted_questions = [question.format()
                                       for question in questions]
                random_question = random.choice(formatted_questions)
                formatted_questions.remove(random_question)

            return jsonify({
                'success': True,
                "question": random_question,
            })
        except:
            abort(500)

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(400)
    def Bad_Request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request (may be missing data)"
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "this request is unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Error occured in the server side"
        }), 500

    return app
