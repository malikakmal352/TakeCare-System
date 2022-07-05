from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.messages import success


def Rider_middleware(get_response):
    def middleware(request):
        if not request.session.get('Rid_id'):
            messages.error(request, "Please Login First For Future Operations")
            return redirect('Rider_Login')

        response = get_response(request)
        return response

    return middleware


def Rider_login_check(get_response):
    def middleware(request):
        if request.session.get('Rid_id'):
            return redirect('Rider_Dashboard')

        response = get_response(request)
        return response

    return middleware
