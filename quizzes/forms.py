from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from datetime import datetime

from quizzes.models import Quiz, Question, AnswerRating


class QuizAdminForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'active', 'pub_date']

    def clean_pub_date(self) -> datetime:
        pub_date = self.cleaned_data['pub_date']
        if pub_date < now():
            raise ValidationError("pub date should be in the future.")
        return pub_date

    def clean(self) -> dict:
        cleaned_data = super().clean()
        return cleaned_data


class AnswerRatingForm(ModelForm):
    class Meta:
        model = AnswerRating
        fields = ['quiz', 'min_value', 'max_value', 'content']

    def clean(self) -> dict:
        cleaned_data = super().clean()
        if cleaned_data['min_value'] >= cleaned_data['max_value']:
            raise ValidationError("min value should be less than max value")
        return cleaned_data


class CustomInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        ranges = []
        for form in self.forms:
            if cleaned_data := form.cleaned_data:
                ranges.append((cleaned_data['min_value'], cleaned_data['max_value']))
        ranges.sort(key=lambda r: r)
        checker = None
        for start, end in ranges:
            if not checker:
                checker = start
            if start <= checker < end:
                checker = end
            else:
                raise ValidationError("There are some overlaps. Please correct.")
        return


AnswerRatingInlineFormSet = inlineformset_factory(
    parent_model=Quiz,
    model=AnswerRating,
    fields=['min_value', "max_value"],
    formset=CustomInlineFormSet,
    form=AnswerRatingForm,
)
