from django.shortcuts import render, redirect

from Laboratory.models.Labcity import Labcity
from Rider_dashboard.models.Rider import Rider
from Pharmacy_Store.models.Medicine_Order import order
# from django.utils.timezone import now
# from datetime import datetime
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
        # error_message = None

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
    Complete_Deliveries_count = order.objects.filter(Rider=Current_Rider, status="Delivered",
                                                     Rider_Request_status='Completed').count()
    Pending_Deliveries_count = order.objects.filter(Rider=Current_Rider, status="Conform",
                                                    Rider_Request_status='Assign a Rider').count()
    Total_Dispatch_Deliver = order.objects.filter(Rider=Current_Rider, Rider_Request_status='Cancelled').count()
    Assign_Orders = order.objects.filter(Rider=Current_Rider)
    Data = {"Current_Rider": Current_Rider, "Pick_order_count": Pick_order_count,
            "Total_Deliveries_count": Total_Deliveries_count,
            "Complete_Deliveries_count": Complete_Deliveries_count,
            "Total_medicines_Deliver": Total_medicines_Deliver,
            "Total_Dispatch_Deliver": Total_Dispatch_Deliver,
            "Pending_Deliveries_count": Pending_Deliveries_count,
            'Assign_Orders': Assign_Orders}
    return render(request, "Dashboard/Rider_dashboard.html", Data)


@Rider_middleware
def Rider_delivery(request):
    if request.method == 'POST':
        Data = request.POST
        name = Data.get('action')
        Reason = Data.get('Reason')
        id = Data.get('id')
        if name == 'Out For Delivery':
            order_Confirm = order.objects.get(id=id)
            order_Confirm.status = 'Out for delivery'
            order_Confirm.save()
            messages.error(request, "Medicine Order is Out For Delivery Now")
        elif name == 'Delivered':
            order_Confirm = order.objects.get(id=id)
            order_Confirm.status = 'Delivered'
            order_Confirm.Rider_Request_status = 'Completed'
            order_Confirm.payment = 'Paid'
            order_Confirm.save()
            messages.error(request, "Medicine Order is Delivery and Receive Cash")
        elif name == 'Dispatch':
            order_Confirm = order.objects.get(id=id)
            order_Confirm.status = 'Dispatch'
            order_Confirm.Rider_Request_status = 'Cancelled'
            order_Confirm.Rider_Request_Reject_Reason = Reason
            order_Confirm.save()
            messages.error(request, "Medicine Order is Dispatch")
        else:
            order_Confirm = order.objects.get(id=id)
            order_Confirm.status = 'Conform'
            order_Confirm.save()
            messages.error(request, "Medicine Order is Confirm Successfully")
    return redirect("/Rider_Dashboard/#table_sub_2")


@Rider_middleware
def View_Complete_Deliveries(request):
    Rd = request.session.get('Rid_id')
    Current_Rider = Rider.objects.get(id=Rd)
    Assign_Orders = order.objects.filter(Rider=Current_Rider, Rider_Request_status='Completed')
    Data = {"Current_Rider": Current_Rider,
            'Assign_Orders': Assign_Orders}
    return render(request, "Dashboard/View_Complete_Rider_Orders.html", Data)


@Rider_middleware
def View_Pending_Deliveries(request):
    Rd = request.session.get('Rid_id')
    Current_Rider = Rider.objects.get(id=Rd)
    Assign_Orders = order.objects.filter(Rider=Current_Rider)
    Data = {"Current_Rider": Current_Rider,
            'Assign_Orders': Assign_Orders}
    return render(request, "Dashboard/View_Pending_Deliveries.html", Data)


@Rider_middleware
def Deliveries_History(request):
    Rd = request.session.get('Rid_id')
    Current_Rider = Rider.objects.get(id=Rd)
    Assign_Orders = order.objects.filter(Rider=Current_Rider)
    Data = {"Current_Rider": Current_Rider,
            'Assign_Orders': Assign_Orders}
    return render(request, "Dashboard/View_Rider_History.html", Data)


# ////////////////////////////Functions Related  Rider Admin Dashboard+profile page start///////////////////////////


@Rider_middleware
def Rider_profile(request):
    Rd = request.session.get('Rid_id')
    error_message = None
    success = None

    flag = False
    phy_profile = Rider.objects.filter(id=Rd)
    labcity = Labcity.objects.all()
    Current_Rider = Rider.objects.get(id=Rd)

    if request.method == 'POST':
        data = request.POST
        Current_password = data.get('C_pass')
        New_password = data.get('New_password')
        Confirm_password = data.get('NConform_pass')
        for i in phy_profile:
            sa = i.password
            if sa == Current_password:
                flag = True

        if New_password != Confirm_password:
            messages.error(request, "Password and Comfort Password must be same")
        elif len(New_password) < 8:
            messages.error(request, "Password must be At-least 8 digit long")
        elif flag:
            Cus = Rider.objects.get(id=Rd)
            Cus.password = New_password
            Cus.save()
            messages.info(request, "Your Password Updated Successfully")
        else:
            messages.error(request, "Please Check Your Current Password You Enter")
        return redirect(Rider_profile)

    Data = {'phy_profile': phy_profile, 'labcity': labcity,
            'error': error_message, 'Current_Rider': Current_Rider,
            'success': success}
    return render(request, "Dashboard/Rider_Profile.html", Data)


@Rider_middleware
def Rider_profile_img(request):
    Rd = request.session.get('Rid_id')
    Rider_img = Rider.objects.get(id=Rd)
    if request.method == 'POST':
        rider_profile_img = request.FILES.get('image')
        Rider_img.img = rider_profile_img
        Rider_img.save()
    return redirect(Rider_profile)


@Rider_middleware
def updates_Rider_profile(request):
    Rd = request.session.get('Rid_id')
    if request.method == 'POST':
        data = request.POST
        name = data.get("username")
        phone = data.get("phone")
        Address = data.get("Address")
        if name:
            name = name.capitalize()
            Profile = Rider.objects.get(id=Rd)
            Profile.name = name
            Profile.save()
            messages.info(request, "Your Username Change Successfully")
        elif phone:
            if len(phone) < 10:
                messages.error(request, "Password must be At-least 10 digit long without first '0' ")
            else:
                Profile = Rider.objects.get(id=Rd)
                Profile.Callnumber = phone
                Profile.save()
                messages.info(request, "Your Phone number Change Successfully")
        elif Address:
            Address = Address.capitalize()
            Profile = Rider.objects.get(id=Rd)
            Profile.Address = Address
            Profile.save()
            messages.info(request, "Your Address Change Successfully")
    return redirect(Rider_profile)
# //////////////////////////Functions Related Medicine_list Add_New/Edit/Delete Start///////////////////////////////////////////
