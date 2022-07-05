from django.shortcuts import render, redirect
from Rider_dashboard.models.Rider import Rider
from Pharmacy_Store.models.Medicine_Order import order
from django.contrib import messages

from Rider_dashboard.Middleware.Rider_auth import Rider_middleware, Rider_login_check


# Create your views here.

@Rider_login_check
def Rider_Login(request):
    if request.method == 'GET':
        return render(request, "Rider_Login.html")
    else:
        Data = request.POST
        email = Data.get('email')
        password = Data.get('password')

        # # Validations
        rider = Rider.objects.filter(CNIC=email, password=password)
        Rider_active = Rider.objects.filter(CNIC=email, password=password, is_Active=True)
        error_message = None

    if rider:
        if not Rider_active:
            error_message = email + " is Deactivated by the TakeCare Team"
            return render(request, 'Rider_Login.html', {'error': error_message})
        for i in rider:
            request.session['Rid_id'] = i.id
            return redirect(Rider_Dashboard)
    else:
        error_message = "Rider ID or Password Invalid......"
        Data = {'error': error_message}
        # return render(request, 'Login.html', {'error': error_message})
    return render(request, 'Rider_Login.html', Data)


@Rider_middleware
def Rider_Dashboard(request):
    Rd = request.session.get('Rid_id')
    Current_Rider = Rider.objects.get(id=Rd)
    Total_Deliveries_count = order.objects.filter(Rider=Current_Rider).count()

    Pick_order_count = order.objects.filter(Rider=Current_Rider, status="Out for delivery").count()
    Total_medicines_Deliver = order.objects.filter(Rider=Current_Rider, status="Rider Received Payment").count()
    Complete_Deliveries_count = order.objects.filter(Rider=Current_Rider, status="Cancelled").count()
    Data = {"Current_Rider": Current_Rider, "Pick_order_count": Pick_order_count,
            "Total_Deliveries_count": Total_Deliveries_count,
            "Complete_Deliveries_count": Complete_Deliveries_count,
            "Total_medicines_Deliver": Total_medicines_Deliver}
    return render(request, "Dashboard/Rider_dashboard.html", Data)
