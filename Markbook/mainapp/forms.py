from django import forms

class StudentLoginForm(forms.Form):
    code = forms.CharField(label="",widget=forms.TextInput(attrs={'type':'text','maxlength':'6','placeholder':'Код'}))
