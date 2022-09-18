from django.http import HttpResponseRedirect

'''Authentication mixins'''
# Redirect users to the main page if users try to 
# access login or signup page when they are already logged in
class AlreadyLoginMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('user_id', None):
            return HttpResponseRedirect("/command-sets/")
        else:
            return super().dispatch(request, *args, **kwargs)
