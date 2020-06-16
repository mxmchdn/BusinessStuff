from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm #as CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def register(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')	
			messages.success(request, f'Your account has been created! You are now able to log in.')
			return redirect('Login')
	else:
		form = CustomUserCreationForm()
	return render(request, 'Users/register.html', {'title': 'Register', 'form': form})

@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('Profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form,
		'title': 'Profile'
	}

	return render(request, 'Users/profile.html', context)