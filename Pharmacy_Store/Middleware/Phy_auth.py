from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.messages import success


def Phy_middleware(get_response):
    def middleware(request):
        if not request.session.get('Phy_id'):
            messages.error(request, "Please Login First For Future Operations")
            request.session['required_path'] = request.path
            return redirect('/Phy_Login/?next=%s' % request.path)

        response = get_response(request)
        return response

    return middleware


def Phy_login_check(get_response):
    def middleware(request):
        if request.session.get('Phy_id'):
            return redirect('Phy_admin')

        response = get_response(request)
        return response

    return middleware
