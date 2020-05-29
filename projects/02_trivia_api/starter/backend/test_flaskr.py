import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)

        """this is my data base path"""
        # self.database_path = "postgres://postgres:1234@localhost:5432/trivia"

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # ................................................ GET: /categories endpoint test ................................................
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])

    # ................................................ GET: /questins endpoint test ................................................
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], None)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_404_sent_requesting_unfound_page(self):
        res = self.client().get('/questions?page=5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    # ................................................ DELETE: /questins endpoint test ................................................
    def test_delete_question(self):
        res = self.client().delete('/questions/20')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_question'])

    def test_404_sent_requesting_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    # ................................................ POST: /questins endpoint test ................................................
    def test_post_question(self):
        res = self.client().post('/questions',
                                 json={'question': 'what is your name ?', 'answer': 'Ahmed', 'category': 1, 'difficulty': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_question'])

    def test_400_sent_requesting_post_question(self):
        res = self.client().post('/questions',
                                 json={'question': 'what is your name ?', 'answer': '', 'category': 1, 'difficulty': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request (may be missing data)')

    # ................................................ POST: /questins/search endpoint test ................................................
    def test_search_question(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], None)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_400_sent_requesting_search_question(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request (may be missing data)')

    # ................................................ GET: /categories/<int:id>/questions endpoint test ................................................
    def test_get_question_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_category'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_sent_requesting_questions_by_category(self):
        res = self.client().get('/categories/2000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    # ................................................ POST: /quizzes endpoint test ................................................
    def test_post_quizzes(self):
        res = self.client().post('/quizzes',
                                 json={'previous_questions': [], 'quiz_category': {'type': 'science', 'id': 2}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_40_sent_requesting_quizes(self):
        res = self.client().post(
            '/quizzes', json={'quiz_category': {'type': 'science', 'id': 2}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request (may be missing data)')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
