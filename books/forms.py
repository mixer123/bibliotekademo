from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    # login = forms.CharField(max_length=20)
    email = forms.EmailField()
    class Meta:
        model=User
        fields = ('username','email', 'password1', 'password2')
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

