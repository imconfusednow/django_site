from django import forms


class LoginForm(forms.Form):
    room_name = forms.CharField(label="")
    submit_type = forms.CharField(label="")