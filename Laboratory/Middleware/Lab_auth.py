from django.contrib import messages
from django.shortcuts import redirect


def Lab_middleware(get_response):
    def middleware(request):

        if not request.session.get('lab_email'):
            messages.error(request, "Please Login First For Future Operations")
            request.session['required_path'] = request.path
            return redirect('/Lab_Login/?next=%s' % request.path)

        response = get_response(request)
        return response

    return middleware


def Lab_login_check(get_response):
    def middleware(request):

        if request.session.get('lab_email'):
            return redirect('lab_Admin')

        response = get_response(request)
        return response

    return middleware
