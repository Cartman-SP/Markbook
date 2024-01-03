from django import forms
from django.forms.widgets import MultiWidget, TextInput

class SixDigitCodeWidget(MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            TextInput(attrs={'maxlength': '1', "type":"number", "min":"0","max":"9",'oninput': 'moveToNext(this, 1)', 'onpaste': 'handlePaste(event)', 'id': 'digit1'}),
            TextInput(attrs={'maxlength': '1', "type":"number", "min":"0","max":"9",'oninput': 'moveToNext(this, 2)', "onkeydown":"handleKeyDown(event, 1)",'id': 'digit2'}),
            TextInput(attrs={'maxlength': '1', "type":"number", "min":"0","max":"9",'oninput': 'moveToNext(this, 3)', "onkeydown":"handleKeyDown(event, 2)",'id': 'digit3'}),
            TextInput(attrs={'maxlength': '1', "type":"number", "min":"0","max":"9",'oninput': 'moveToNext(this, 4)', "onkeydown":"handleKeyDown(event, 3)",'id': 'digit4'}),
            TextInput(attrs={'maxlength': '1', "type":"number", "min":"0","max":"9",'oninput': 'moveToNext(this, 5)', "onkeydown":"handleKeyDown(event, 4)",'id': 'digit5'}),
            TextInput(attrs={'maxlength': '1', "type":"number", "min":"0","max":"9",'oninput': 'moveToNext(this, 6)', "onkeydown":"handleKeyDown(event, 5)", 'id': 'digit6'}),
        ]
        super().__init__(widgets, attrs=attrs)

    def decompress(self, value):
        if value:
            return list(value)
        return [None] * 6

class SixDigitCodeField(forms.CharField):
    widget = SixDigitCodeWidget

    def clean(self, value):
        code = super().clean(value)
        code = code.replace(',', '').replace(' ', '').replace("'", '').replace("[", '').replace("]", '')
        print(code)

        if not code or len(code) != 6 or not code.isdigit():
            raise forms.ValidationError("Некорректный ввод")
        return code

class StudentLoginForm(forms.Form):
    code = SixDigitCodeField(label='', required=True)