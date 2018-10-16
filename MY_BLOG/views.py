from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse



"""The signup() functon checks whether the method is post or not if yes it checks for the value is signup if yes it calls
the register function or it calls the login function"""
def signup(request):
    if request.method == 'POST':
        if request.POST.get('signup-click') == 'signup_to':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('hme')
        else:
            return _login(request)
    else:
        form = UserCreationForm()
    return render(request, 'index.html', {'form': form})

"""Declaration of login function which is called in signup function if the value of submit button is not 'signup_to then'"""
def _login(request):
    username = request.POST['username']
    password = request.POST['password']
    user     = authenticate(request, username = username, password = password)
    if user:
        login(request, user)
        user_session = request.session['username'] = request.POST.get('username')
        return HttpResponseRedirect(reverse('welcome_home'))
    else:
        context['error'] = 'Incorrect Credentials!'
        return render(request, 'index.html', context)
        
    

"""welcome_home function does nothing but displays data to the home and works as an UI for the users"""
def welcome_home(request):
    context = {}
    context['user']= request.user
    return render(request, 'home.html', context)


"""Visit_again() function just logs out from the system and redirects to the index page where an  user ca login again"""
def visit_again(request):
    if request.method is 'POST':
        logout(request)
        HttpResponseRedirect(reverse('name_signup'))