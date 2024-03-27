from nested_inline.admin import NestedModelAdmin, NestedTabularInline

from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import format_html
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from quizzes.forms import QuizAdminForm, AnswerRatingInlineFormSet, AnswerRatingForm
from quizzes.models import Answer, Question, Quiz, AnswerRating


class AnswerInline(NestedTabularInline):
    model = Answer
    fk_name = "question"
    extra = 1


class QuestionInline(NestedTabularInline):
    model = Question
    fk_name = "quiz"
    extra = 1
    inlines = [AnswerInline]


class AnswerRatingInline(admin.TabularInline):
    model = AnswerRating
    fk_name = "quiz"
    formset = AnswerRatingInlineFormSet
    form = AnswerRatingForm
    extra = 1

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()
        return queryset.order_by("quiz", "min_value", "max_value")


@admin.register(Quiz)
class QuizAdmin(NestedModelAdmin):
    list_display = ("id", "title", "pub_date", "is_published")
    list_filter = ("title",)
    ordering = ["id"]
    date_hierarchy = "pub_date"
    form = QuizAdminForm
    fieldsets = (
        (_("Basic info"), {"fields": ("title", "description")}),
        (_("Publication info"), {"fields": ("active", "pub_date")}),
    )
    inlines = [AnswerRatingInline, QuestionInline]

    @admin.display(description=_("is published"), boolean=True)
    def is_published(self, quiz: Quiz) -> bool:
        today = now()
        return quiz.active and quiz.pub_date <= today


# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ("id", "quiz_link", "title")
#     list_filter = ("title",)
#     ordering = ["quiz", "order", "id"]
#     fields = ["title", "type", "order"]
#
#     @admin.display(description=_("quiz"))
#     def quiz_link(self, question: Question) -> str:
#         url = reverse("admin:quizzes_quiz_change", args=[question.quiz_id])
#         link = format_html('<a href="{}">{}</a>', url, str(question.quiz))
#         return link
#
#
# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ("id", "question", "description")
#     list_filter = ("question",)
#     ordering = ["question", "id"]
#     fields = ["question", "description"]
