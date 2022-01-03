from django import forms
from review.models import Review


class ReviewCrispyForm(forms.ModelForm):
    pass
    """
    helper = FormHelper()
    helper.from_id = 'review-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Review
        fields = ('title', 'text', 'rate')
        """
