from django.shortcuts import redirect


def Patient_middleware(get_response):
    def middleware(request):
        print('middleware Run \n')

        if not request.session.get('email'):
            return redirect('login')

        response = get_response(request)
        return response

    return middleware
