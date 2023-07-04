# C:\Users\juanp\OneDrive\Documentos\Juan\Python\py-django\premiosplatzi\premiosplatziapp

import datetime

from django.utils import timezone
from django.urls import reverse
from django.test import TestCase

from .models import Question


#Models - Views
class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Quien es el mejor Profesor de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_recently_with_past_quetion(self):
        """was_published_recently returns False for questions whose pub_date is in the past"""
        time = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(question_text="¿Quien es el mejor Profesor de Platzi?", pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)
    

    def test_was_published_recently_with_present_question(self):
        """was_published_recently returns True for questions whose pub_date is in the present"""
        time = timezone.now()
        present_question = Question(question_text="¿Quien es el mejor Profesor de Platzi?", pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)



def create_question(question_text, days):
    """
    Create a question with the given "question_text", and plublished the given
    number of days offset to now (negative for questions published in the past
    positive for questions that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)



class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])


    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed in the index page."""
        response = self.client.get(reverse("polls:index"))
        future_question = create_question(question_text="Future question", days=30)

        self.assertContains(response, "No polls are available.")
        self.assertNotContains(response, "Future question")
        self.assertIsNot(future_question, response.context["latest_question_list"])
        self.assertQuerysetEqual(response.context["latest_question_list"], [])


    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page."""
        question = create_question(question_text="Past question", days=-10)
        response = self.client.get(reverse("polls:index"))

        self.assertQuerysetEqual(response.context["latest_question_list"], [question])


    def test_future_question_and_past_question(self):
        """Even if both past and future question exit, only past questions are displayed"""
        past_question = create_question(question_text="Past question", days=-30)
        future_question = create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))

        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])


    def test_two_past_questions(self):
        """The questions index page may diplay multiple questions."""
        past_question1 = create_question(question_text="Past question1", days=-30)
        past_question2 = create_question(question_text="Past question2", days=-40)
        response = self.client.get(reverse("polls:index"))

        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question1, past_question2])

    
    def test_two_future_questions(self):
        """The question index page doesn't displayed future questions."""
        future_question1 = create_question(question_text="Future question1", days=20)
        future_question2 = create_question(question_text="Future question2", days=40)
        response = self.client.get(reverse("polls:index"))

        self.assertIsNot(future_question1, response.context["latest_question_list"])
        self.assertIsNot(future_question2, response.context["latest_question_list"])



class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """ The detail view of a question with a pub_date in the future returns a 404 error not found """
        future_question = create_question(question_text="Future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)


    def test_past_question(self):
        """ The detail view of a question with a pub_date in the past displays the question's text """
        past_question = create_question(question_text="Past question", days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        
        self.assertContains(response, past_question.question_text)
        
