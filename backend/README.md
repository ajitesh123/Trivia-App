# Full Stack Trivia API Backend

## Introduction
This app is created a REST API to power trivia. The tech stack includes - SQLAlchemy ORM, PostgreSQL, Python, Flask, and Flask-cors.

## Getting Started
You should have Python3 and Pip installed in order to get started. Follow instructions to install the latest version of python for your platform in the python docs (https://docs.python.org/3/using/unix.html)

### Virtual Environment Setup
Initialize and activate a virtualenv:

```
$ cd YOUR_PROJECT_DIRECTORY_PATH/
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

### Installing Dependencies

Use Pip to install all of the required packages we selected within the `requirements.txt` file.
```
$ pip install -r requirements.txt
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

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

## API Documentation

### Getting Started
Base Url - At present, this application runs locally and is not hosted at a base URL. The backend app is hosted at the default htttp://127.0.0.1:5000/, which is set as proxy for the frontend configuration.

You can also read the documentation at Postman - https://web.postman.co/collections/8444799-494f5106-20c0-43c2-a7e1-4c8977430d30

### Authentication
This version of this application doesn't require documentation

### Error Handling

Error are returned as JSON objects in the following formats:

```
{
  'success': False
  'error': 400,
  'message'; 'bad request'
}
```
The API could return following error:

400: Bad Request
- 404: Resource not found
- 422: Unprocessable
- 500: Internal server error

### Rate limit
There isn't a limit to the number of requests an user can send.

### Endpoints

#### GET /categories

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

Example RequestDefault:

```
curl --location --request GET 'http://127.0.0.1:5000/categories' \
--data-raw ''
```

Example Response

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### GET /questions?page=1

Fetches a list a list of 10 questions, number of total questions, current category, categories


Example RequestDefault
```
curl --location --request GET 'http://127.0.0.1:5000/questions?page=1' \
--data-raw ''
```

Example Response:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": [
    1,
    2,
    3,
    4,
    6
  ],
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
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
    }
  ],
  "total_questions": 4
}
```

#### DELETE /questions/1

Allows questions to be deleted by question id.

Example Request
```
curl --location --request DELETE 'http://127.0.0.1:5000/questions/1' \
--data-raw ''
```

Example Response:
```
}
    'success': True,
    'deleted': 1
}
```

#### POST /questions

Allows you to POST a new question, which will require the question and answer text, category, and difficulty score.

Body raw (text):
```
{"question":"Where is Red Fort?","answer":"New Delhi","difficulty":"2","category":"3"}
```

Example Request:
```
curl --location --request POST 'http://127.0.0.1:5000/questions' \
--data-raw '{"question":"Where is Red Fort?","answer":"New Delhi","difficulty":"2","category":"3"}'
```

Example Response:
```
}
    'success': True,
    'question_id': 10
}
```

#### POST /questions/search

Fetches questions based on a search term.

Body raw (text)
```
{"searchTerm":"d"}
```

Example Request:
```
curl --location --request POST 'http://127.0.0.1:5000/questions/search' \
--header 'Content-Type: application/json' \
--data-raw '{
	"searchTerm": "What"

}'
```

Example Response:
```
{
  "current_category": [
    1,
    3,
    4,
    5
  ],
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Rajouri Garden",
      "category": 5,
      "difficulty": 3,
      "id": 24,
      "question": "What the best place for chole bhature in Delhi?"
    },
    {
      "answer": "Old Delhi",
      "category": 5,
      "difficulty": 4,
      "id": 25,
      "question": "What's best place to eat Chaat?"
    },
    {
      "answer": "Sarvana Bhavan",
      "category": 5,
      "difficulty": 3,
      "id": 38,
      "question": "What is the best place for dosa?"
    }
  ],
  "success": true,
  "total_questions": 6
}
```

#### GET /categories/<Category ID>/questions

Fetched you only questions from a particular category

Example Request:
```
curl --location --request GET 'http://127.0.0.1:5000/categories/1/questions' \
--data-raw ''
```

Example Response
```
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "total_questions": 2
}
```

#### POST /questions/quizzes

Takes category and previous question parameters and returns a random questions within the given category, if provided, and that is not one of the previous questions

Body raw (text)
```
{"previous_questions":[],"quiz_category":{"type":"Science","id":"1"}}
```

Example Request:
```
curl --location --request POST 'http://127.0.0.1:5000/questions/quizzes' \
--data-raw '{"previous_questions":[],"quiz_category":{"type":"Science","id":"1"}}'
```

Example Response:
```
{
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
```

## Testing
File - trivia_test.py covers extensive test of different end points. To run the tests, run following

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
