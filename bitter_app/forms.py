from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.html import strip_tags, escape
from bitter_app.models import Beet

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation', 'class': 'form-control'}))
    
    def is_valid(self):
        form = super(UserCreateForm, self).is_valid()
        return form
    
    class Meta:
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']
        model = User

class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
 
    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        return form

class BeetForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'class': 'beetText'}))
    
    def is_valid(self):
        form = super(BeetForm, self).is_valid()
        return form
    
    class Meta:
        model = Beet
        exclude = ('user',)