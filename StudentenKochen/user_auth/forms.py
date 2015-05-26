from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from user_auth.models import Student

class RegistrationForm(ModelForm):
    username = forms.CharField(label=(u'User Name'))
    email = forms.EmailField(label=(u'Email Adresse'))
    password = forms.CharField(label=(u'Passwort'), widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label=(u'Passwort bestaetigen'), widget=forms.PasswordInput(render_value=False))
    
    class Meta:
        model = Student
        exclude =('user',)
        
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Username wird bereits verwendet")
    
    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError("Passwort stimmt nicht ueberein. Bitte versuche es erneut.")
        return self.cleaned_data
    
class LoginForm(forms.Form):
    username = forms.CharField(label=(u'User Name'))
    password = forms.CharField(label=(u'Passwort'), widget=forms.PasswordInput(render_value=False))
    