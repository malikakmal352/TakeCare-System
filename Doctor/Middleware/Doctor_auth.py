from django.shortcuts import redirect


def Doctor_middleware(get_response):
    def middleware(request):
        print('middleware Run \n')

        if not request.session.get('doctor_email'):
            return redirect('Doctor_Login')


        response = get_response(request)
        return response

    return middleware


def Doctor_login_check(get_response):
    def middleware(request):
        print('middleware Run \n')

        if request.session.get('doctor_email'):
           return redirect('Doctor_admin')

        response = get_response(request)
        return response

    return middleware
