from datetime import UTC

import factory
import faker
from factory.fuzzy import FuzzyChoice, FuzzyInteger

from quizzes.models import Answer, Question, QuestionType, Quiz, AnswerRating


class QuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quiz

    title = factory.Faker("text", max_nb_chars=100)
    description = factory.Faker("paragraph")
    active = FuzzyChoice([True, False])
    pub_date = factory.Faker(
        "date_time_between",
        start_date="-1d",
        end_date="+1m",
        tzinfo=UTC,
    )


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    quiz = factory.SubFactory(QuizFactory)
    title = factory.Faker("text", max_nb_chars=100)
    type = FuzzyChoice(QuestionType.values)
    order = FuzzyInteger(0, 10)


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    question = factory.SubFactory(QuestionFactory)
    description = factory.Faker("text", max_nb_chars=100)
    points = FuzzyInteger(0, 10)


class AnswerRatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AnswerRating

    quiz = factory.SubFactory(QuizFactory)
    min_value = FuzzyInteger(0, 10)
    max_value = FuzzyInteger(1, 20)
    content = faker.Faker("text", max_nb_chars=50)
