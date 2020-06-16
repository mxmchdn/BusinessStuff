from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

from .models import Profile
 
 
class CustomUserCreationForm(forms.Form):
	email = forms.EmailField(label='Enter email')
	username = forms.CharField(label='Enter Username', min_length=4, max_length=150, help_text=("~ At least 4 characters (characters, digits and @/-/_/./+ only"))

	password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput, strip=False, help_text=password_validation.password_validators_help_text_html(),)
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput, strip=False, help_text=("~ Enter the same password as before, for verification"))

	def clean_username(self):
		username = self.cleaned_data['username'].lower()
		r = User.objects.filter(username=username)
		if r.count():
			raise ValidationError("Username already exists!")
		return username

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		r = User.objects.filter(email=email)
		if r.count():
			raise ValidationError("Email already exists!")
		with open('./WhiteList.txt', "r") as WhiteList:
			mail = WhiteList.readlines()
			for i in range(len(mail)):
				mail[i] = mail[i].replace('\n', '').lower()
			if not email.lower() in mail:
				raise ValidationError("Your are not allowed to access this site!")
		return email

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise ValidationError("The two password fields didn't match.")
		return password2

	def _post_clean(self):
		super()._post_clean()
		password = self.cleaned_data.get('password2')
		if password:
			try:
				password_validation.validate_password(password)
			except forms.ValidationError as error:
				self.add_error('password1', error)

	def save(self, commit=True):
		user = User.objects.create_user(
			self.cleaned_data['username'],
			self.cleaned_data['email'],
			self.cleaned_data['password1']
		)
		return user

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image', 'powerbi', 'company']