from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .auth_forms import LoginForm
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
                    return HttpResponseRedirect("/command-sets/")
        context = {'message': 'Invalid credentials. Please try again.'}
        return render(request, self.template_name, context)


# View for user sign
class SignupView(AlreadyLoginMixin, CreateView):
    model = User
    fields = ['username', 'email', 'password']
    template_name = "signup.html"
    context_object_name = "user"

# View for user logout
class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        request.session["user_id"] = None
        logout(request)
        return HttpResponseRedirect("/login/")

