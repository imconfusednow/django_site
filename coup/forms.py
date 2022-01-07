from django import forms


class MsgForm(forms.Form):
    msg = forms.CharField(label="")