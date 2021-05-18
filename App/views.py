from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views import generic
from django.shortcuts import render
from .models import Post
from App import forms
import random

@login_required(login_url="login/")

def home(request):
	posts = Post.objects.filter(status=1).order_by('-created_on')
	return render(request,"home.html",{'post_list': posts})

#delete post, button on hover on each section, should delete that post object from Post.objects. return new list (referring to updated filtered object list); refresh page?

def register(request):
	if not request.user.is_authenticated():
		if request.method == "POST":
			form1 = forms.UserSignUpForm(request.POST)
			if form1.is_valid():
				user = form1.save(commit=False)
				user.password = make_password(form1.cleaned_data['password'])
				user.email = form1.cleaned_data['email']
				user.save()
				return HttpResponseRedirect('/')
		else:
			form1 = forms.UserSignUpForm()
		return render(request,'App/register.html',context={
			'form':form1
			})
	else:
		messages.error(request, 'You Are logged In')
		return redirect('/')


def change_password(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = PasswordChangeForm(request.user, request.POST)
			if form.is_valid():
				user = form.save()
				update_session_auth_hash(request, user)
				messages.success(request, 'Your password was successfully updated!')
				return redirect('/')
			else:
				messages.error(request, 'Please correct the error below.')
		else:
			form = PasswordChangeForm(request.user)
		return render(request, 'App/change_password.html', {
			'form': form
		})
	else:
		messages.error(request, 'You Are not logged In')
		return redirect('/')

def submit(request):
	if request.user.is_authenticated():
		if request.method == "POST":
			form = forms.PostForm(request.POST)
			if form.is_valid():
				post = form.save(commit=False)
				title = form.cleaned_data['title']
				post.title = title
				post.slug = str(random.getrandbits(128))
				post.author = request.user
				post.save()
				return redirect('/')
		else:
			form = forms.PostForm()
		return render(request,'App/submit.html',context={
			'form':form
			})
	else:
		messages.error(request, 'You Are not logged In')
		return redirect('/')

def delete(request, title_id):
	if request.user.is_authenticated():
		post = Post.objects.get(title=title_id)
		post.delete()
		return redirect('/')
	else:
		messages.error(request, 'You Are not logged In')
		return redirect('/')

#delete post; on hover, only show delete button if current user (matching users from curr and post)