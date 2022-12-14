import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
        DB_TEST = os.getenv('DB_TEST', 'trivia_test')
        self.database_name= DB_TEST 
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresq://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_TEST)
        setup_db(self.app, self.database_path)



        self.new_question= {
            'question': 'is the test working?',
            'answer': 'yes',
            'category': 1,
            'difficulty': 'normal'
            }

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

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000", json={"category": 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        

    def test_422_if_question_creation_fails(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        

    def test_delete_question(self):
        question = Question(question="new question",answer="new answer", difficulty=2,category=2)
        question.insert()
        question_id = question.id
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], question_id)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(question, None)

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


    def test_questions_per_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["currentCategory"]))

    def test_404_sent_questions_per_category_invalid_page(self):
        res = self.client().get("/categories/1000/questions", json={"category": 0})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


    def test_quizzes(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [],
            "quiz_category": {
                "type": "Geography",
                "id": "3"
            }
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
       

    def test_422_quizzes_fails(self):
        res = self.client().post("/quizzes")
        self.assertEqual(res.status_code, 400)


    def test_load_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['categories'])


    def test_404_categories(self):
        res = self.client().get("/category")
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    def test_search_question(self):
        res = self.client().post("/questions", json ={"searchTerm":'movie'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
    
    def test_failed_search_question(self):
        res = self.client().post("/questions")
        self.assertEqual(res.status_code,400)
         
        
      








# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()