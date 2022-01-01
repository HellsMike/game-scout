from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from review.models import Review


class ReviewCrispyForm(forms.ModelForm):
    helper = FormHelper()
    helper.from_id = 'review-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Review
        fields = ('title', 'text', 'rate')
