from django.shortcuts import redirect

'''Authentication mixins'''
# Redirect users to the main page if users try to 
# access login or signup page when they are already logged in
class AlreadyLoginMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('user_id', None):
            return redirect("/")
        else:
            return super().dispatch(request, *args, **kwargs)

# Redirect users to the login page if they access pages that require authentication
class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('user_id', None):
            return redirect("/login/")
        else:
            return super().dispatch(request, *args, **kwargs)
