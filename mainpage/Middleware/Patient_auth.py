from django.contrib import messages
from django.shortcuts import redirect


def Patient_middleware(get_response):
    def middleware(request):
        print('middleware Run \n')

        if not request.session.get('email'):
            messages.error(request, "Please Login First For Future Operations")
            print(request.path)
            request.session['required_path'] = request.path
            return redirect('/Login/?next=%s' % request.path)

        response = get_response(request)
        return response

    return middleware
