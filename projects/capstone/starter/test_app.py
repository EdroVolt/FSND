import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from app import create_app
from models import setup_db, Movie, Actor


load_dotenv()


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        database_filename = "database.db"
        project_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = os.getenv("sqlite:///{}".format(
            os.path.join(project_dir, database_filename)))

        setup_db(self.app)

        # self.assistant_headers =
        # self.director_headers =
        self.producer_headers = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik4wUXdRVEUwTnpFMk0wTTVRVVF4TXpGRE9FTXhOMFkyUTBORk5FVkZPRFkxUlRRelJUa3hOQSJ9.eyJpc3MiOiJodHRwczovL2Rldi0xcGwzLTQ2NS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3ZjUzZTI5ZDhhMTgwYzg0ZGE2NGNmIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTU5MDQyMzU3NiwiZXhwIjoxNTkwNTA5OTc2LCJhenAiOiJyN2hjMnRhYnYyaTZpOHJYUEJXMm4zbFFLN29rbEhybiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.0ITdRZhkiiMNW0A8Hjyxrb3x3-H9rItEd4HO0a2gWuf_qBphNihZRR-nRsV4c8zyory-mnT-jSrpzcXa9wDlaAP-ZFqCk70uLINUSxO-EWVGYSkie41V-oTIaaYMQoXJ85EREG3rAmZW2FbrqGvI3JZouMTcRv6fRVvfwx5d3ym5_h1rKXuBkXnjKW594N-7_GqRNiE2zmxWeIYzUDqJJN41OkIm8H26pdYYRsEBaFsksMr28hxpjLymA-2zvcPUNsz-MO_Bf8EsGl795x7MsuxV-CvMyHVKdv8YyV6ule6qupI2A6wszYlWo-reAYFP2OQq9FA4MnGe_8XHONMX9g'

        # self.assistant_headers = {
        #     "Content-Type": "application/json",
        #     "Authorization": os.getenv('CASTING_ASSISTANT')
        # }
        # self.director_headers = {
        #     "Content-Type": "application/json",
        #     "Authorization":  os.getenv('CASTING_DIRECTOR')
        # }
        # self.producer_headers = {
        #     "Content-Type": "application/json",
        #     "Authorization":  os.getenv('EXECUTIVE_PRODUCER')
        # }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create/drop all tables

    def tearDown(self):
        """Executed after reach test"""
        pass


# ................................................ POST: /actors endpoint test ................................................

    def test_post_actors(self):
        res = self.client().post('/actors',
                                 json={"name": "Hudaasa", "age": 15,
                                       "gender": "female"},
                                 headers={'Authorization':
                                          'Bearer ' + self.producer_headers})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_actor'])

    def test_401_sent_requesting_post_actors_without_auth_header(self):
        res = self.client().post('/actors',
                                 json={"name": "Halaaaa", "age": 15, "gender": "female"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # ................................................ POST: /movies endpoint test ................................................
    def test_post_movies(self):
        res = self.client().post('/movies',
                                 json={"title": "shs movie",
                                       "year": 2024, "month": 12, "day": 10},
                                 headers={'Authorization':
                                          'Bearer ' + self.producer_headers})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_movie'])

    def test_401_sent_requesting_post_movies_without_auth_header(self):
        res = self.client().post('/movies',
                                 json={"title": "ss movie", "year": 2024, "month": 12, "day": 10})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # ................................................ GET: /actors endpoint test ................................................
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization':
                                                    'Bearer ' + self.producer_headers})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_401_sent_requesting_actors_without_auth_header(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # ................................................ GET: /movies endpoint test ................................................
    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization':
                                                    'Bearer ' + self.producer_headers})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_401_sent_requesting_movies_without_auth_header(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # ................................................ PATCH: /actors endpoint test ................................................
    def test_patch_actors(self):
        res = self.client().patch('/actors/8',
                                  json={"name": "HalaHala"}, headers={'Authorization':
                                                                      'Bearer ' + self.producer_headers})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['modified_actor'])

    def test_401_sent_requesting_patch_actors_without_auth_header(self):
        res = self.client().patch('/actors/3',
                                  json={"age": 22})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # ................................................ PATCH: /movies endpoint test ................................................
    def test_patch_movies(self):
        res = self.client().patch('/movies/2',
                                  json={"title": "wow"}, headers={'Authorization':
                                                                  'Bearer ' + self.producer_headers})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['modified_movie'])

    def test_401_sent_requesting_patch_movies_without_auth_header(self):
        res = self.client().patch('/movies/1',
                                  json={"age": 22})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # ................................................ DELETE: /actors endpoint test ................................................

    def test_delete_actors(self):
        res = self.client().delete('/actors/2', headers={'Authorization':
                                                         'Bearer ' + self.producer_headers})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_actor'])

    def test_401_sent_requesting_delete_actors_without_auth_header(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # ................................................ DELETE: /movies endpoint test ................................................
    def test_delete_movies(self):
        res = self.client().delete('/movies/2', headers={'Authorization':
                                                         'Bearer ' + self.producer_headers})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_movie'])

    def test_401_sent_requesting_delete_movies_without_auth_header(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
