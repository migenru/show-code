from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(max_length=50, help_text='Введите поисковый запрос', required=True)


class FavoriteForm(forms.Form):
    favorite = forms.CharField(widget=forms.HiddenInput(), required=False)
