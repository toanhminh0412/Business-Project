from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from forms import LoginForm, SignupForm
from mixins import AlreadyLoginMixin

# View for user login
class LoginView(AlreadyLoginMixin, TemplateView):
    template_name = "login.html"

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_data = login_form.cleaned_data
            email_user = User.objects.filter(email=login_data["email"])
            if len(email_user) > 0:
                login_user_username = email_user[0].username 
                login_user = authenticate(username=login_user_username, password=login_data["password"])
                if login_user:
                    request.session['user_id'] = login_user.id
                    login(request, login_user)
                    return HttpResponseRedirect("/")
        context = {'message': 'Invalid credentials. Please try again.'}
        return render(request, self.template_name, context)


# View for user sign
class SignupView(AlreadyLoginMixin, TemplateView):
    template_name = "signup.html"
    
    def post(self, request):
        form = SignupForm(request.POST)
        # Form is valid
        if form.is_valid():
            # Read data from form
            signup_data = form.cleaned_data
            password = signup_data['password']
            retype_password = signup_data['retype_password']
            email = signup_data['email']
            username = signup_data['username']
            
            # Passwords have to match
            if password == retype_password:
                
                # One email can only register one account
                if len(User.objects.filter(email=email)) > 0:
                    context = {'message': "This email is already in used. Please login."}
                    return render(request, self.template_name, context) 
                
                # Username has to be unique
                if len(User.objects.filter(username=username)) > 0:
                    context = {'message': "This username is already in used. Please pick another one."}
                    return render(request, self.template_name, context) 
                
                # Create a new user and login
                user = User.objects.create(username=signup_data['username'], email=signup_data['email'], password=signup_data['password'])
                login(request, user)
                request.session['user_id'] = user.id
                return HttpResponseRedirect("/")
            else:
                context = {'message': "Passwords don't match. Please try again."}
                return render(request, self.template_name, context)
        else:
            context = {'message': 'Please fill out the form properly. Please try again.'}
            return render(request, self.template_name, context)

# View for user logout
class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        request.session["user_id"] = None
        logout(request)
        return HttpResponseRedirect("/login/")

