from django import forms
from command_set.models import CommandSet

# Form for user to log in
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=20)
    password = forms.CharField(max_length=20)

# Form for user to sign up
class SignupForm(forms.Form):
    email = forms.EmailField(max_length=100)
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)
    retype_password = forms.CharField(max_length=20)

# Form for adding a new command set
class CommandSetForm(forms.ModelForm):
    class Meta:
        model = CommandSet
        fields = ['title', 'commands', 'tool']