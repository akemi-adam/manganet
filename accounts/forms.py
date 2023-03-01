from django import forms
from django.contrib.auth import get_user_model

# Auth Forms

class RegisterForm(forms.ModelForm):

    class Meta:
        
        model = get_user_model()
        
        fields = [ 'username', 'email', 'password' ]

    username = forms.CharField(max_length = 50, min_length = 3, required = True)

    email = forms.EmailField(max_length = 50, min_length = 3, required = True)

    password = forms.CharField(max_length = 30, min_length = 8, required = True)

class LoginForm(forms.ModelForm):

    class Meta:

        model = get_user_model()

        fields = [ 'username', 'password' ]

    username = forms.CharField(max_length = 50, min_length = 3, required = True)
    
    password = forms.CharField(max_length = 30, min_length = 8, required = True)