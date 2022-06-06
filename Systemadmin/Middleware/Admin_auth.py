from django.shortcuts import redirect


def Admin_middleware(get_response):
    def middleware(request):
        print('middleware Run \n')

        if not request.session.get('admin_email'):
            return redirect('SuperAdmin_Login')

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
