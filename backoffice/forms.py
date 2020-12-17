from django import forms
from extuser.models import ExtUser


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    new_password1 = forms.CharField(
        label=("Новый пароль"),
        widget=forms.PasswordInput,
        strip=False,
        required=False,
    )

    new_password2 = forms.CharField(
        label=("Повторите новый пароль"),
        strip=False,
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = ExtUser
        fields = (
            'first_name',
            'second_name',
            'last_name',
            'email',
            'phone',
            'birthday',
            'avatar',
        )


class ConstructorForm(forms.Form):
    isHouse = forms.BooleanField()
    s_living_room = forms.IntegerField(required=False)
    s_kitchen_room = forms.IntegerField(required=False)
    s_bed_room = forms.IntegerField(required=False)
    s_children_room = forms.IntegerField(required=False)
    s_bathroom_room = forms.IntegerField(required=False)
    s_other_room = forms.IntegerField(required=False)
