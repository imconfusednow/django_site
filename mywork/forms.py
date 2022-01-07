from django import forms


class ContactForm(forms.Form):
    Email = forms.EmailField(label="")
    Subject = forms.CharField(label="")
    Message = forms.CharField(label="", widget=forms.Textarea, max_length=1000)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['placeholder'] = i


class SearchForm(forms.Form):
    search = forms.CharField(label="")