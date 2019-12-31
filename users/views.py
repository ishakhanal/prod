from django.contrib.auth import authenticate, login
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from datetime import datetime
from users.forms import (EditProfileForm, ProfileForm, RegistrationForm)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from entries.models import Contract

def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = request.POST['username']
			password = request.POST['password1']
			user = authenticate(request, username=username, password=password)
			login(request, user)
			return redirect('letsbid-home')


	else:
		form = RegistrationForm()

	context = {'form':form}

	return render(request, 'users/register.html', context)



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)  # request.FILES is show the selected image or file

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        args = {}
        # args.update(csrf(request))
        args['form'] = form
        args['profile_form'] = profile_form
        return render(request, 'users/editprofile.html', args)


@login_required
def userprofile(request):
    user = request.user
    user_posts = Contract.objects.filter(contract_creator=request.user).order_by('-contract_date')
    template = 'users/profile.html'
    return render(request, template, {'user_posts':user_posts,'user': user})