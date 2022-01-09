from django import forms


class LoginForm(forms.Form):
    game_id = forms.CharField(label="", required=False)