from django.contrib import messages
from django.shortcuts import render
from user.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect
from user.forms import SignUpForm,UserUpdateForm,ProfileUpdateForm
from home.models import Setting
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.


@login_required(login_url='/login')
def index(request):
    setting = Setting.objects.get(pk=1)
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'profile': profile,'setting':setting}
    return render(request, 'user_profile.html', context)


def login_form(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user =request.user
            #userprofile=UserProfile.objects.get(user_id=current_user.id)
            #request.session['userimage'] = userprofile.image.url
            #request.session['currency'] = userprofile.currency.code

            # Redirect to a success page.
            messages.success(request, "Welcome back")
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,"Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.

    context = {'setting':setting}
    return render(request, 'login_form.html',context)


def signup_form(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created! Please save your location details')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup')

    form = SignUpForm()
    context = {
               'form': form,'setting':setting,
               }
    return render(request, 'register.html', context)


def logout_func(request):
    logout(request)
    messages.success(request, 'You are successfully logged out')
    return HttpResponseRedirect('/')


@login_required(login_url='/login') # Check login
def user_update(request):
    setting=Setting.objects.get(pk=1)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) #"userprofile" model -> OneToOneField relatinon with user
        context = {
            'user_form': user_form,
            'setting':setting,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login') # Check login
def user_password(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form,'setting':setting})

