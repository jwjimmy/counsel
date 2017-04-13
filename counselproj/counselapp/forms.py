from django import forms
from django.core import validators
from django.contrib.auth.models import User
import string

class RegistrationForm(forms.Form):
	
	username = forms.CharField(label='username', max_length=30, required=True)
	email = forms.EmailField(label='email', max_length=30, required=True)
	password1 = forms.CharField(label='password1', widget=forms.PasswordInput(), required=True)
	password2 = forms.CharField(label='password2', widget=forms.PasswordInput(), required=True)

	def clean_username(self):
		try:
			User.objects.get(username=self.cleaned_data['username'])
		except User.DoesNotExist:
			return self.cleaned_data['username']
		raise validators.ValidationError('The username "%s" is already taken.' % self.cleaned_data['username'])

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if not password2:
			raise forms.ValidationError("You must confirm your password")
		if password1 != password2:
			raise forms.ValidationError("Your passwords do not match")
		return password2
	
	def save(self, new_data):
		u = User.objects.create_user(new_data['username'],
									new_data['email'],
									new_data['password1'])
		u.is_active = False
		u.save()
		return u