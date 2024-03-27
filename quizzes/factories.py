from datetime import UTC

import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger

from quizzes.models import Answer, Question, QuestionType, Quiz


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
