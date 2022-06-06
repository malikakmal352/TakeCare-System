from django.shortcuts import redirect


def Phy_middleware(get_response):
    def middleware(request):
        if not request.session.get('Phy_email'):
            return redirect('pharmacy Login')

        response = get_response(request)
        return response

    return middleware


def Phy_login_check(get_response):
    def middleware(request):
        if request.session.get('Phy_email'):
            return redirect('Phy_admin')

        response = get_response(request)
        return response

    return middleware
