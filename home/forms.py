from pickle import TRUE
from wsgiref.validate import validator
from xml.dom import ValidationErr
from attr import attr, attrs
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from .models import ContactUs


#contact us form
class ContactForm(forms.ModelForm):
	name=forms.CharField(widget=forms.TextInput(attrs={
		"class": "myCustomInput",
		"placeholder": "Name"
	}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={
		"class": "myCustomInput",
		"placeholder": "Email",
	}))
	message= forms.CharField(widget=forms.Textarea(attrs={
		"class": "myCustomTextArea",
		"placeholder": "Type you message here..."
	}))
	class Meta:
		model = ContactUs
		fields = '__all__'


# Create new user or register form
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
	}), validators=[validators.MinLengthValidator(6)], error_messages={"required": "Enter your password"})
	password2 = forms.CharField(widget=forms.PasswordInput({
		"class": "form-control",
		"placeholder": "Confirm Password"
	}), validators=[validators.MinLengthValidator(6)], error_messages={"required": "Enter your password"})

	class Meta():
		model = User
		fields = ["first_name", "username", "password1", "password2"]


	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=True)
		user.email = self.cleaned_data['username']
		if commit:
			user.save()
		return user