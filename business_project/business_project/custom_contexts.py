def get_user(request):
    return {
        'user_id': request.session.get('user_id', None)
    }
