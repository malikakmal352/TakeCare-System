from django.contrib import messages
from django.shortcuts import redirect


def Admin_middleware(get_response):
    def middleware(request):
        print('middleware Run \n')

        if not request.session.get('admin_email'):
            messages.error(request, "Please Login First For Future Operations")
            request.session['required_path'] = request.path
            return redirect('/SuperAdmin_Login/?next=%s' % request.path)

        response = get_response(request)
        return response

    return middleware


def Admin_login_check(get_response):
    def middleware(request):
        print('middleware Run \n')

        if request.session.get('admin_email'):
            return redirect('Super_admin')

        response = get_response(request)
        return response

    return middleware
