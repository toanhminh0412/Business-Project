from django.http import HttpResponseRedirect

# This paths are unaffected by the middleware
LOGIN_PATH = "/login/"
ADMIN_PATH = "/admin/"
SIGNUP_PATH = "/signup/"

class AuthenticateMiddleware():
    """
    This middleware checks if user is authenticated before every view.
    An unauthenticated user will be redirected to the login page
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):     
        # redirect user to login page if user is not authenticated
        if request.path != LOGIN_PATH and request.path != SIGNUP_PATH and ADMIN_PATH not in request.path and not request.session.get('user_id', None):
            return HttpResponseRedirect('/login')
        response = self.get_response(request)
        return response
