from factory import Iterator

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from quizzes.factories import AnswerFactory, QuestionFactory, QuizFactory
from quizzes.models import Answer, Question, QuestionType, Quiz


class Command(BaseCommand):
    help = "Creates simple fake users. Do not use on production!"

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Cannot run this command on production settings!")
        quizzes = self._create_quizzes()
        questions = self._create_questions(quizzes)
        self._create_answers(questions)

    def _create_quizzes(self) -> list[Quiz]:
        quizzes = QuizFactory.create_batch(size=3)
        self.stdout.write(self.style.SUCCESS(f"Created {len(quizzes)} quizzes:"))
        for quiz in quizzes:
            msg = f"PK: {quiz.pk}, title: {quiz.title}"
            self.stdout.write(self.style.SUCCESS(f"    {msg}"))
        return quizzes

    def _create_questions(self, quizzes: list[Quiz]) -> list[Question]:
        questions = []
        for quiz in quizzes:
            questions.extend(
                QuestionFactory.create_batch(
                    size=3,
                    quiz=quiz,
                    order=Iterator(range(3)),
                )
            )
        self.stdout.write(self.style.SUCCESS(f"Created {len(questions)} questions:"))
        for question in questions:
            msg = f"Quiz: {question.quiz.pk}, title: {question.title}, order: {question.order}"
            self.stdout.write(self.style.SUCCESS(f"    {msg}"))
        return questions

    def _create_answers(self, questions: list[Question]) -> list[Answer]:
        answers = []
        questions_with_answers = filter(
            lambda q: q.type != QuestionType.OPEN_QUESTION,
            questions,
        )
        for question in questions_with_answers:
            answers.extend(
                AnswerFactory.create_batch(
                    size=3,
                    question=question,
                )
            )
        self.stdout.write(self.style.SUCCESS(f"Created {len(answers)} answers:"))
        for answer in answers:
            msg = f"Question: {answer.question.pk}, title: {answer.description}"
            self.stdout.write(self.style.SUCCESS(f"    {msg}"))
        return answers
