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

        self.producer_headers = {
            "Content-Type": "application/json",
            "Authorization":  {'Token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik4wUXdRVEUwTnpFMk0wTTVRVVF4TXpGRE9FTXhOMFkyUTBORk5FVkZPRFkxUlRRelJUa3hOQSJ9.eyJpc3MiOiJodHRwczovL2Rldi0xcGwzLTQ2NS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3ZjUzZTI5ZDhhMTgwYzg0ZGE2NGNmIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTU5MDQwODUwNCwiZXhwIjoxNTkwNDE1NzA0LCJhenAiOiJyN2hjMnRhYnYyaTZpOHJYUEJXMm4zbFFLN29rbEhybiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.pMc0pR63syUDVq8mcKCB2xmwMtVT3Dwr9vXTOKVKENGy1CxA3QlYQR3yPP127v8v3j65caICy0RWPKhN0SzVQfDi-c-JRKwJZn718WQLQzQMVVt1RhoAsVy8wkNv4c18KGA2oHkaEqhqV522biUMxMBQGXoTPh3JI1GHechCheiqWxp5s4QEhbmlS4CGGXMP1sX-ih5VZEGXhFA3mcwASFLTua8DfcSTwmVRhkXSyEy48_IpiSvvW-lwDUzW1TW4dRBtp_NPF3h6HDKHOlgIlKuLw2gFhiEPqJyb5mkruOusFPkqP3LfXL0D7mD2ug4T7_aZQXkIJKlbKlnAEDsQmw'}
        }
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
                                 json={"name": "Mona", "age": 15,
                                       "gender": "female"},
                                 headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_actor'])

    def test_401_sent_requesting_post_actors_without_auth_header(self):
        res = self.client().post('/actors',
                                 json={"name": "Hala", "age": 15, "gender": "female"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # ................................................ POST: /movies endpoint test ................................................
    def test_post_movies(self):
        res = self.client().post('/movies',
                                 json={"title": "awsome1 movie",
                                       "year": 2024, "month": 12, "day": 10},
                                 headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_movie'])

    def test_401_sent_requesting_post_movies_without_auth_header(self):
        res = self.client().post('/movies',
                                 json={"title": "awsome2 movie", "year": 2024, "month": 12, "day": 10})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # ................................................ GET: /actors endpoint test ................................................
    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.producer_headers)
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
        res = self.client().get('/movies', headers=self.producer_headers)
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
        res = self.client().patch('/actors/3',
                                  json={"age": 20}, headers=self.producer_headers)
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
        res = self.client().patch('/movies/3',
                                  json={"age": 20}, headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['modified_movie'])

    def test_401_sent_requesting_patch_movies_without_auth_header(self):
        res = self.client().patch('/movies/3',
                                  json={"age": 22})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # ................................................ DELETE: /actors endpoint test ................................................

    def test_delete_actors(self):
        res = self.client().delete('/actors/3', headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_actor'])

    def test_401_sent_requesting_delete_actors_without_auth_header(self):
        res = self.client().delete('/actors/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # ................................................ DELETE: /movies endpoint test ................................................
    def test_delete_movies(self):
        res = self.client().delete('/movies/3', headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_movie'])

    def test_401_sent_requesting_delete_movies_without_auth_header(self):
        res = self.client().delete('/movies/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
