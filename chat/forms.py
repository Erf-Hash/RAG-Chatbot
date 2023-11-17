from django import forms

class ChatForm(forms.Form):
    query = forms.CharField(max_length=100)