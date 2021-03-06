# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT

```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

GET '/questions'

- Fetch a dictionary of questions paginated by 10 questions per page in which the keys are (question, answer, category, difficulty) and the values is the corresponding values for each question
- Request Arguments: page number . If it's None the page number will be 1.
- Returns: An object with key:value pairs {success: True, questions: 10 question per page, total_questions: number of all question, categories: object of id: category_string key:value pairs, current_category: null}
- sample : curl http://127.0.0.1:5000/questions
  {
  "categories": {
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
  },
  "current_category": null,
  "questions": [
  {
  "answer": "Apollo 13",
  "category": 5,
  "difficulty": 4,
  "id": 2,
  "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  },
  {
  "answer": "Tom Cruise",
  "category": 5,
  "difficulty": 4,
  "id": 4,
  "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  },
  {
  "answer": "Maya Angelou",
  "category": 4,
  "difficulty": 2,
  "id": 5,
  "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  {
  "answer": "Edward Scissorhands",
  "category": 5,
  "difficulty": 3,
  "id": 6,
  "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  {
  "answer": "Muhammad Ali",
  "category": 4,
  "difficulty": 1,
  "id": 9,
  "question": "What boxer's original name is Cassius Clay?"
  },
  {
  "answer": "Uruguay",
  "category": 6,
  "difficulty": 4,
  "id": 11,
  "question": "Which country won the first ever soccer World Cup in 1930?"
  },
  {
  "answer": "George Washington Carver",
  "category": 4,
  "difficulty": 2,
  "id": 12,
  "question": "Who invented Peanut Butter?"
  },
  {
  "answer": "Lake Victoria",
  "category": 3,
  "difficulty": 2,
  "id": 13,
  "question": "What is the largest lake in Africa?"
  },
  {
  "answer": "The Palace of Versailles",
  "category": 3,
  "difficulty": 3,
  "id": 14,
  "question": "In which royal palace would you find the Hall of Mirrors?"
  },
  {
  "answer": "Agra",
  "category": 3,
  "difficulty": 2,
  "id": 15,
  "question": "The Taj Mahal is located in which Indian city?"
  }
  ],
  "success": true,
  "total_questions": 36
  }

DELETE '/questions/<int:question_id>'

- delete single question by id
- Request Arguments: None
- Returns: An object with a two keyes, success: True, deleted_question: that contains the deleted question object.
- Sample : curl -X DELETE http://127.0.0.1:5000/questions/22
  {
  "deleted_question": {
  "answer": "Blood",
  "category": 1,
  "difficulty": 4,
  "id": 22,
  "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true
  }

POST '/questions'

- create new question
- Request Arguments: json object contains (question, answer, category, difficulty)
- Returns: An object with a two keyes, success: True, new_question: that contains the new question object.
- Sample : curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"whats your name","answer":"Ahmed","difficulty":"1","category":"1"}'
  {
  "new_question": {
  "answer": "Ahmed",
  "category": 1,
  "difficulty": 1,
  "id": 58,
  "question": "whats your name"
  },
  "success": true
  }

POST '/questions/search'

- search for available questions with a word or sequence of characters in it.
- Request Arguments: json object contains key:value pair {"searchTerm": string}
- Returns: An object with a two keyes, success: True, questions: that contains list of question objects matches the "searchTerm" value.
- Sample : curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm":"title"}'
  {
  "categories": {
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
  },
  "current_category": null,
  "questions": [
  {
  "answer": "Maya Angelou",
  "category": 4,
  "difficulty": 2,
  "id": 5,
  "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  {
  "answer": "Edward Scissorhands",
  "category": 5,
  "difficulty": 3,
  "id": 6,
  "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  }
  ],
  "success": true,
  "total_questions": 2
  }

GET '/categories/<int:id>/questions'

- search for available questions by specific category.
- Request Arguments: None
- Returns: An object with a three keyes, success: True, questions: that contains list of question objects within the category ,total_questions: number of questions in the category, current_category: category name.
- Sample : curl -X GET http://127.0.0.1:5000/categories/3/questions
  {
  "current_category": "Geography",
  "questions": [
  {
  "answer": "Lake Victoria",
  "category": 3,
  "difficulty": 2,
  "id": 13,
  "question": "What is the largest lake in Africa?"
  },
  {
  "answer": "The Palace of Versailles",
  "category": 3,
  "difficulty": 3,
  "id": 14,
  "question": "In which royal palace would you find the Hall of Mirrors?"
  },
  {
  "answer": "Agra",
  "category": 3,
  "difficulty": 2,
  "id": 15,
  "question": "The Taj Mahal is located in which Indian city?"
  }
  ],
  "success": true,
  "total_questions": 3
  }

POST '/quizzes'

- search for available questions by specific category.
- Request Arguments: json object contains key:value pair {"previous_questions": contains list of IDs of previous questions, "quiz_category": contain two key:value pair {"type": name of category, "id": id of that category}
- Returns: An object with a two keyes, success: True, question: that contains a random question within the selected category and not in the previous_questions list.
- Sample : curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"Geography","id":"3"}}'

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
