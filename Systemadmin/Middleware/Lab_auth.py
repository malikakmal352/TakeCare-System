from django.shortcuts import redirect


def Lab_middleware(get_response):
    def middleware(request):
        print('middleware Run \n')

        if not request.session.get('lab_email'):
            return redirect('Laboratory Login')

        response = get_response(request)
        return response

    return middleware


def Lab_login_check(get_response):
    def middleware(request):
        print('middleware Run \n')

        if request.session.get('lab_email'):
            return redirect('lab_Admin')

        response = get_response(request)
        return response

    return middleware
