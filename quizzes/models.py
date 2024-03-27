from tinymce.models import HTMLField

from django.db import models
from django.utils.translation import gettext_lazy as _


class QuestionType(models.TextChoices):
    SINGLE_QUESTION = "SQ", _("Single question")
    OPEN_QUESTION = "OQ", _("open question")
    MULTIPLE_CHOICES = "MQ", _("multiple choices")


class Quiz(models.Model):
    title = models.CharField(max_length=128)
    description = HTMLField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField()

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self) -> str:
        return str(self.pk)


class Question(models.Model):
    quiz = models.ForeignKey(
        to="quizzes.Quiz",
        on_delete=models.CASCADE,
        related_name="questions",
    )
    title = models.CharField(max_length=128)
    type = models.CharField(
        choices=QuestionType.choices, default=QuestionType.SINGLE_QUESTION
    )
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self) -> str:
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(
        to="quizzes.Question",
        on_delete=models.CASCADE,
        related_name="answers",
    )
    description = models.CharField(max_length=128)
    points = models.PositiveSmallIntegerField(default=0)

    def __str__(self) -> str:
        return self.description


class AnswerRating(models.Model):
    quiz = models.ForeignKey(to="quizzes.Quiz", on_delete=models.CASCADE)
    min_value = models.PositiveSmallIntegerField(default=0)
    max_value = models.PositiveSmallIntegerField(default=0)
    content = models.CharField(max_length=128)
