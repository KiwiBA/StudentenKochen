from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from .forms import RegistrationForm, LoginForm
from .models import Student
from django.contrib.auth import authenticate, login, logout

def StudentRegistration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username = form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
            user.save()
            student = Student(user=user, name=form.cleaned_data['name'])
            student.save()

            return HttpResponseRedirect('/login/')
        else:
            return render_to_response('user_auth/register.html', {'form': form}, context_instance=RequestContext(request))
    else: 
        """user is not submitting the form, show them a blank registration form"""
        form = RegistrationForm()
        context = {'form': form}
        return render_to_response('user_auth/register.html', context, context_instance=RequestContext(request))
    
def LoginRequest(request):
    """
    Shows
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            student = authenticate(username=username, password=password)
            if student is not None:
                login(request, student)

                return HttpResponseRedirect('/profile/')
            else:
                return render_to_response('user_auth/login.html', {'form': form}, context_instance=RequestContext(request))

        else:
            return render_to_response('user_auth/login.html', {'form': form}, context_instance=RequestContext(request))
    else:
        '''user is not submitting the form, show the login form'''
        form = LoginForm()
        context = {'form': form}
        return render_to_response('user_auth/login.html', context, context_instance=RequestContext(request))
    
def LogoutRequest(request):
    logout(request) 
    print("logged out")
    return HttpResponseRedirect('/')

def profile(request):
    return render(request, 'user_auth/profile.html')