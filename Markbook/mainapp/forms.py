from django import forms


class StudentLoginForm(forms.Form):
    code = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'type': 'text', 'maxlength': '6', 'placeholder': 'Код'}))

    def clean_code(self):
        data = self.cleaned_data.get('code')
        if not data:
            self.add_error('code', 'This field is required.')
        return data