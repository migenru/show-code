from django import forms


class QuestionForm(forms.Form):
    title = forms.CharField(max_length=200)
    content = forms.CharField(required=False, widget=forms.Textarea)


class AnswerForm(forms.Form):
    title = forms.CharField(max_length=200)
    content = forms.CharField(required=False, widget=forms.Textarea)
