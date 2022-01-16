from django import forms


class LoginForm(forms.Form):
    game_id = forms.CharField(label="")
    submit_type = forms.CharField(label="")