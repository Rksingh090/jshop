from pickle import TRUE
from attr import attr, attrs
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
	username = forms.EmailField(widget=forms.EmailInput(attrs={
		"class": "form-control",
		"placeholder": "Email"
	}), required=True)
	first_name = forms.CharField(widget=forms.TextInput({
		"class": "form-control",
		"placeholder": "First Name"
	}))
	password1 = forms.CharField(widget=forms.PasswordInput({
		"class": "form-control",
		"placeholder": "Password"
	}))
	password2 = forms.CharField(widget=forms.PasswordInput({
		"class": "form-control",
		"placeholder": "Confirm Password"
	}))

	class Meta():
		model = User
		fields = ["first_name", "username", "password1", "password2"]

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=True)
		user.email = self.cleaned_data['username']
		if commit:
			user.save()
		return user