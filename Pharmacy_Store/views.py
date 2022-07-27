import uuid
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator

from django.shortcuts import render, redirect
from django.utils.timezone import now
from future.backports.datetime import timedelta

from Laboratory.models.Labcity import Labcity
from Pharmacy_Store.models.Add_pharmacy import Pharmacy
from Pharmacy_Store.models.Add_Medicine import Add_New_Medicine
from Pharmacy_Store.models.Medicine_Order import order

from mainpage.Sent_Email import send_forget_password_mail_Pharmacy
from Pharmacy_Store.Middleware.Phy_auth import Phy_middleware, Phy_login_check
from mainpage.Middleware.Patient_auth import Patient_middleware

# Create your views here.
from mainpage.models.Patient import Patient
from django.contrib.auth.decorators import login_required
from cart.cart import Cart


def Pharmacies(request, id):
    labcity = Labcity.objects.all()
    labcitys = Labcity.objects.all()
    Test_name = Add_New_Medicine.objects.all()
    all_Medicines = Add_New_Medicine.objects.filter(status="Active", is_Expired=False).order_by('-id')
    Customer = Patient.objects.all()

    paginator = Paginator(all_Medicines, 4)  # Show 5 contacts per page.
    page_number = request.GET.get('page')
    all_Medicine = paginator.get_page(page_number)

    # book_Test = Book_Test.objects.all()
    # w = datetime.date(now())

    if request.method == 'POST':
        ser = request.POST.get('search')
        labcity = Labcity.objects.filter(Lab_city_name=ser)
        Test_name = Add_New_Medicine.objects.filter(Medicine_name=ser)
        labs = Pharmacy.objects.filter(Labname=ser)
        if labcity:
            LabCity = Labcity.objects.filter(id=labcity)
            ci = LabCity

            for d in ci:
                s = d.id

            labs = Pharmacy.objects.filter(city=s)

            data = {'labs': labs, 'ci': ci, 'labcity': labcity,
                    'all_Medicine': all_Medicine, 'labcitys': labcitys,
                    'Test_name': Test_name, 'Customer': Customer}
            return render(request, "index.html", data)

        elif Test_name:
            print(Test_name)
        elif labs:
            print(labs)
        else:
            print('not works')

    data = {'labcity': labcity}

    if id != 400:
        LabCity = Labcity.objects.filter(id=id)
        ci = LabCity

        for d in ci:
            s = d.id

        labs = Pharmacy.objects.filter(city=s)
        data = {'labs': labs, 'ci': ci, 'labcity': labcity,
                'all_Medicine': all_Medicine, 'labcitys': labcitys,
                'Test_name': Test_name, 'Customer': Customer}
    # else:
    #     labs = Pharmacy.objects.all()
    #     data = {'labs': labs, 'labcity': labcity,
    #             'all_Medicine': all_Medicine, 'labcitys': labcitys,
    #             'Test_name': Test_name, 'Customer': Customer}

    return render(request, "Medicine_Card.html", data)

def All_Medicines(request):
    labcity = Labcity.objects.all()
    labcitys = Labcity.objects.all()
    Test_name = Add_New_Medicine.objects.all()
    all_Medicines = Add_New_Medicine.objects.filter(status="Active", is_Expired=False).order_by('-id')
    Customer = Patient.objects.all()

    paginator = Paginator(all_Medicines, 4)  # Show 5 contacts per page.
    page_number = request.GET.get('page')
    all_Medicine = paginator.get_page(page_number)

    labs = Pharmacy.objects.all()
    data = {'labs': labs, 'labcity': labcity,
            'all_Medicine': all_Medicine, 'labcitys': labcitys,
             'Test_name': Test_name, 'Customer': Customer}

    return render(request, "Medicine_Card.html", data)


def Medicine_details(request, id):
    Customer = Patient.objects.all()
    labcity = Labcity.objects.all()
    Medicine_detail = Add_New_Medicine.objects.filter(status="Active", is_Expired=False, id=id)
    data = {"Medicine_detail": Medicine_detail, "labcity": labcity, 'Customer': Customer}
    return render(request, "Medicine_Detail.html", data)


def Medicine_search(request):
    global d

    labcity = Labcity.objects.all()
    labcitys = Labcity.objects.all()
    Test_name = Add_New_Medicine.objects.all()
    all_Medicine = Add_New_Medicine.objects.filter(status="Active", is_Expired=False).order_by('-id')
    Customer = Patient.objects.all()
    # book_Test = Book_Test.objects.all()
    w = datetime.date(now())

    Customer = Patient.objects.all()

    if request.method == 'POST':
        ser = request.POST.get('search')
        Labcitys = Labcity.objects.filter()
        labcity = Labcity.objects.filter(Lab_city_name__startswith=ser)
        Test_name = Test_list.objects.filter(Test_name__startswith=ser)
        labs = Lab.objects.filter(Labname__startswith=ser)


        data = {'Test_name': Test_name, 'labcity': labcity,
                    'labs': labs, 'ser': ser,
                    'all_lab': all_lab, 'labcitys': labcitys,
                    'Customer': Customer
                    }
        return render(request, 'Search_via_test_name.html', data)

    data = {'labs': labs, 'labcity': labcity,
            'all_Medicine': all_Medicine, 'labcitys': labcitys,
            'Test_name': Test_name, 'Customer': Customer}

    return Pharmacies(request, 400)


# ///////////////////////////////////////Pharmacy admin Login ////////////////////////////////////////////////////////
@Phy_login_check
def phy_login(request):
    if request.method == 'GET':
        if request.session.get("required_path"):
            path = request.session.get("required_path")
            return render(request, 'Pharmacy_Login.html', {'path': path})
        else:
           return render(request, "Pharmacy_Login.html")
    else:
        Data = request.POST
        email = Data.get('email')
        password = Data.get('password')

        # # Validations
        pharmacy = Pharmacy.objects.filter(email=email, password=password)
        Laboratory_active = Pharmacy.objects.filter(email=email, password=password, is_Active=True)
        error_message = None

        data = {}

    if pharmacy:
        if not Laboratory_active:
            error_message = email + " is Deactivated by the TakeCare Team"
            return render(request, 'Pharmacy_Login.html', {'error': error_message})
        for i in pharmacy:
            request.session['Phy_id'] = i.id
            fa = request.session['Phy_email'] = i.email
            path = request.session.get("required_path")
            if path:
                return redirect(path)
            else:
               return redirect(Phy_admin)
    else:
        error_message = "Email or Password Invalid......"

        # return render(request, 'Login.html', {'error': error_message})
    return render(request, 'Pharmacy_Login.html', {'error': error_message})

@Phy_middleware
def Phy_logout(request):
    request.session['Phy_id'] = None
    request.session['Phy_email'] = None
    return redirect(mainindex)


def Create_password_Pharmacy(request, token):
    context = {}
    success = None

    try:
        profile_obj = Pharmacy.objects.get(forget_password_token=token)
        la = profile_obj.id
        context = {'user_id': la}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = la
            print(user_id, 'print 2')
            if user_id is None:
                success = "No user id found."
                return redirect(f'/Create_password_Pharmacy/{token}/', {"success": success})
            print("equal loop before ")
            if new_password != confirm_password:
                # messages.success(request, 'both should  be equal.')
                success = "both should  be equal."
                return render(request, 'change-password.html', {"success": success})
                # return redirect(f'/Create_password_Pharmacy/{token}/')

            user_obj = Pharmacy.objects.get(id=user_id)
            user_obj.password = new_password
            user_obj.save()
            user_obj = Pharmacy.objects.get(id=la)
            token = str(uuid.uuid4())
            profile_obj = Pharmacy.objects.get(email=user_obj.email)
            profile_obj.forget_password_token = token
            profile_obj.save()
            success_message = 'Your Password has been Created Successfully now please Login '
            return render(request, 'Pharmacy_Login.html', {'success': success_message})
        else:
            return render(request, 'change-password.html')
    except Exception as e:
        print(e)
    return render(request, 'Link_experiy.html', context)


# ///////////////////////////////////////Medicine Order Placing+Tracking+Cancel  ////////////////////////////////////////////////////////
@Patient_middleware
def Medicine_order_form(request):
    pa = request.session.get('id')
    labcity = Labcity.objects.all()
    Customer = Patient.objects.filter(id=pa)
    if pa:
        if request.method == 'POST':
            data = request.POST
            id = data.get('id')
            order_medicine = Add_New_Medicine.objects.filter(id=id).order_by('-id')
            Data = {"Customer": Customer, 'labcity': labcity,
                    'order_medicine': order_medicine}
            return render(request, "Medicine_Order_Form.html", Data)
    else:
        messages.error(request, "Place Login First For Order Medicine")
        return render(request, 'Login.html', {"message": messages})


@Patient_middleware
def Order_Confirmed(request):
    pa = request.session.get('id')
    labcity = Labcity.objects.all()
    Customer = Patient.objects.filter(id=pa)
    if pa:
        if request.method == 'POST':
            data = request.POST
            Medicine_id = data.get('Medicine_id')
            Medicine = Add_New_Medicine.objects.get(id=Medicine_id)
            Customer_id = Patient.objects.get(id=pa)
            Pharmacy_id = data.get('Pharmacy_id')
            Pharmacy_id = Pharmacy.objects.get(id=Pharmacy_id)
            Quantity = data.get('quantity')
            Quantity = int(Quantity)
            price = Medicine.Medicine_price
            Total_price = price * Quantity
            Address = data.get('address')
            Phone = data.get('phone')

            ADD_Order = order(Medicine=Medicine, Customer=Customer_id,
                              Pharmacy=Pharmacy_id, quantity=Quantity,
                              price=price, Total_price=Total_price,
                              Address=Address, phone=Phone)
            ADD_Order.save()
            Medicine = Add_New_Medicine.objects.get(id=Medicine_id)
            Medicine.Total_Stock = Medicine.Total_Stock - int(Quantity)
            Medicine.save()
            messages.error(request, "Your Order is Placed")
            return redirect(Tracking_Order)
    else:
        messages.error(request, "Place Login First For Order Medicine")
        return render(request, 'Login.html', {"message": messages})


@Patient_middleware
def Order_Confirmed_by_Carts(request):
    pa = request.session.get('id')
    labcity = Labcity.objects.all()
    Customer = Patient.objects.filter(id=pa)
    if pa:
        if request.method == 'POST':
            data = request.POST
            Customer_id = Patient.objects.get(id=pa)
            Address = data.get('address')
            Phone = data.get('phone')
            for key, value in request.session['cart'].items():
                Medicine_id = value['product_id']
                Medicine = Add_New_Medicine.objects.get(id=Medicine_id)
                Pharmacy_id = value['Pharmacy_id']
                Pharmacy_id = Pharmacy.objects.get(id=Pharmacy_id)
                Quantity = value['quantity']
                Quantity = int(Quantity)
                price = Medicine.Medicine_price
                Total_price = price * Quantity

                # print(Medicine_id, Customer_id, Pharmacy_id, Quantity, price, Total_price, Address, Phone)
                ADD_Order = order(Medicine=Medicine, Customer=Customer_id,
                                  Pharmacy=Pharmacy_id, quantity=Quantity,
                                  price=price, Total_price=Total_price,
                                  Address=Address, phone=Phone).save()
                Medicine = Add_New_Medicine.objects.get(id=Medicine_id)
                Medicine.Total_Stock = Medicine.Total_Stock - int(Quantity)
                Medicine.save()
            # Data = {"Customer": Customer, 'labcity': labcity,
            #         'order_medicine': order_medicine}
            cart = Cart(request)
            cart.clear()
            messages.error(request, "Your Order is Placed")
            messages.error(request, "Medicine Order is Placed Successfully")
            return redirect(Tracking_Order)
    else:
        messages.error(request, "Place Login First For Order Medicine")
        return render(request, 'Login.html', {"message": messages})


@Patient_middleware
def Tracking_Order(request):
    pa = request.session.get('id')
    labcity = Labcity.objects.all()
    Track_order = order.objects.filter(Customer=pa).order_by('-id')
    Customer = Patient.objects.filter(id=pa)
    Data = {"Customer": Customer, 'labcity': labcity,
            'Track_order': Track_order, "message": messages}
    return render(request, "Tracking_Order.html", Data)


@Patient_middleware
def Cancel_order(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('id')

        order_Cancel = order.objects.get(id=id)
        Quantity = order_Cancel.quantity
        order_Cancel.status = 'Cancelled'
        order_Cancel.is_Cancel = True
        order_Cancel.save()
        Medicine = Add_New_Medicine.objects.get(id=order_Cancel.Medicine.id)
        Medicine.Total_Stock = Medicine.Total_Stock + int(Quantity)
        Medicine.save()
    return redirect(Tracking_Order)


# ////////////////////////////Functions Related  Pharmacy Admin Dashboard+profile page start///////////////////////////

@Phy_middleware
def Phy_admin(request):
    error_message = None
    success = None
    Test_today = 0
    month = datetime.now().date()
    year = datetime.now().year
    w = datetime.date(now())
    request.session['required_path'] = None
    Py = request.session.get('Phy_id')
    Total_medicines = Add_New_Medicine.objects.filter(Pharmacy=Py, is_Expired=False, status="Active").count()
    Expired_Medicine_count = Add_New_Medicine.objects.filter(Pharmacy=Py, is_Expired=True, status="Active").count()
    Expiring_Soon_Medicine = Add_New_Medicine.objects.filter(Pharmacy=Py, is_Expired=False, status="Active",
                                                             Expiry_Alert_Date__lt=w).count()
    Total_order_count = order.objects.filter(Pharmacy=Py, is_Cancel=False).count()
    Pending_order_count = order.objects.filter(Pharmacy=Py, status='Pending').count()
    Complete_order_count = order.objects.filter(Pharmacy=Py, status='Delivered').count()

    print(month, year, Expiring_Soon_Medicine)
    Current_pharmacy = Pharmacy.objects.get(id=Py)

    all_Medicine = Add_New_Medicine.objects.filter(Pharmacy=Py, status="Active", is_Expired=False).order_by('-id')
    All_Orders = order.objects.filter(Pharmacy=Py)
    for i in all_Medicine:
        if w > i.Medicine_Expiry_date:
            if not i.is_Expired:
                i.is_Expired = True
                i.save()
    #
    # back_day = timedelta(days=2)
    # print(back_day)
    # yesterday = w - back_day
    # print('back dates = ', yesterday)

    data = {"Current_pharmacy": Current_pharmacy, "Total_medicines": Total_medicines,
            "Expired_Medicine_count": Expired_Medicine_count,
            "Expiring_Soon_Medicine": Expiring_Soon_Medicine,
            "Total_order_count": Total_order_count,
            'Pending_order_count': Pending_order_count,
            'Complete_order_count': Complete_order_count,
            'All_Orders': All_Orders}
    return render(request, "Pharmacy_Admin/Phy_admin.html", data)


@Phy_middleware
def Phy_profile(request):
    lb = request.session.get('Phy_id')
    error_message = None
    success = None

    flag = False
    phy_profile = Pharmacy.objects.filter(id=lb)
    labcity = Labcity.objects.all()
    Current_pharmacy = Pharmacy.objects.get(id=lb)

    if request.method == 'POST':
        data = request.POST
        Current_password = data.get('C_pass')
        New_password = data.get('New_password')
        Confirm_password = data.get('NConform_pass')
        for i in phy_profile:
            sa = i.password
            print(sa)
            if sa == Current_password:
                flag = True
                print(flag)

        if New_password != Confirm_password:
            error_message = 'Password and Comfort Password must be same'
        elif len(New_password) < 8:
            error_message = " Password must be At-least 8 digit long "
        elif flag:
            Cus = Pharmacy.objects.get(id=lb)
            Cus.password = New_password
            Cus.save()
            success = "Your Password Updated Successfully"

        else:
            error_message = "Please Check Your Current Password You Enter"

    Data = {'phy_profile': phy_profile, 'labcity': labcity,
            'error': error_message, 'Current_pharmacy': Current_pharmacy,
            'success': success}
    return render(request, "Pharmacy_Admin/admin_profile.html", Data)


@Phy_middleware
def Phy_profile_img(request):
    lb = request.session.get('Phy_id')
    error_message = None
    success = None
    Pharmacy_img = Pharmacy.objects.get(id=lb)
    if request.method == 'POST':
        Laboratory_profile_img = request.FILES.get('image')
        Pharmacy_img.img = Laboratory_profile_img
        Pharmacy_img.save()
    return redirect(Phy_profile)


@Phy_middleware
def updates_Phy_profile(request):
    lb = request.session.get('Phy_id')
    error_message = None
    success = None

    phy_profile = Pharmacy.objects.filter(id=lb)
    labcity = Labcity.objects.all()
    Current_pharmacy = Pharmacy.objects.get(id=lb)

    if request.method == 'POST':
        data = request.POST
        name = data.get("username")
        phone = data.get("phone")
        Address = data.get("Address")
        if name:
            name = name.capitalize()
            Profile = Pharmacy.objects.get(id=lb)
            Profile.Username = name
            Profile.save()
            success = "Your Username Change Successfully"
        elif phone:
            if len(phone) < 10:
                error_message = " Password must be At-least 10 digit long without first '0' "
            else:
                Profile = Pharmacy.objects.get(id=lb)
                Profile.Callnumber = phone
                Profile.save()
                success = "Your Phone number Change Successfully"
        elif Address:
            Address = Address.capitalize()
            Profile = Pharmacy.objects.get(id=lb)
            Profile.Address = Address
            Profile.save()
            success = "Your Address Change Successfully"

    Data = {'phy_profile': phy_profile, 'labcity': labcity,
            'error': error_message, 'Current_pharmacy': Current_pharmacy,
            'success': success}
    return render(request, "Pharmacy_Admin/admin_profile.html", Data)


# //////////////////////////Functions Related Medicine_list Add_New/Edit/Delete Start///////////////////////////////////////////

@Phy_middleware
def add_new_Medicine(request):
    error_message = None
    success = None
    w = datetime.date(now())
    Py = request.session.get('Phy_id')
    Current_pharmacy = Pharmacy.objects.get(id=Py)

    if request.method == 'POST':
        Data = request.POST
        image = request.FILES.get('img')
        name = Data.get('name')
        Price = Data.get('Price')
        Expiry_Date = Data.get("Expiry_Date")
        Medicine_type = Data.get('Medicine_type')
        Total_Stock = Data.get("Stock")
        Description = Data.get('Description')
        date_time_obj = datetime.strptime(Expiry_Date, '%Y-%m-%d')

        # print(name, Price, Total_Stock, Medicine_type, Expiry_Date)
        back_day = timedelta(days=14)
        Expiry_Alert_Date = date_time_obj - back_day
        add_New_Medicine = Add_New_Medicine(Medicine_name=name, Medicine_price=Price,
                                            Pharmacy=Current_pharmacy, Total_Stock=Total_Stock,
                                            Medicine_Expiry_date=Expiry_Date, img=image,
                                            Medicine_packaging=Medicine_type,
                                            Expiry_Alert_Date=Expiry_Alert_Date,
                                            Description=Description
                                            )
        add_New_Medicine.save()
        messages.error(request, name + " New Medicine is Added Sucessfully")
        return redirect(add_new_Medicine)
        # success = "New Medicine is Added Sucessfully"

        # Is_Exit = Test_list.objects.filter(Test_name=name)
        # if Is_Exit:
        #     error_message = "Medicine with this name is already exit.Please "
        #     print(error_message)
        #     Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success}
        #     return render(request, "Admin_site/Add_new_test.html", Data)

    Data = {"Current_pharmacy": Current_pharmacy, 'error_message': error_message, 'success': success}
    return render(request, "Pharmacy_Admin/Add_New_Medicine.html", Data)


@Phy_middleware
def view_Medicine_list(request):
    Py = request.session.get('Phy_id')
    Current_pharmacy = Pharmacy.objects.get(id=Py)
    w = datetime.date(now())

    all_Medicine = Add_New_Medicine.objects.filter(Pharmacy=Py, is_Expired=False).order_by('-id')
    for i in all_Medicine:
        if w > i.Medicine_Expiry_date:
            if not i.is_Expired:
                i.is_Expired = True
                i.save()
    all_Medicine = Add_New_Medicine.objects.filter(Pharmacy=Py, status="Active", is_Expired=False).order_by('-id')

    Data = {"Current_pharmacy": Current_pharmacy, 'all_Medicine': all_Medicine}
    return render(request, "Pharmacy_Admin/View_Medicine_List.html", Data)


@Phy_middleware
def Medicine_delete(request):
    error_message = None
    success = None
    Py = request.session.get('Phy_id')
    Current_pharmacy = Pharmacy.objects.get(id=Py)
    all_Medicine = Add_New_Medicine.objects.filter(Pharmacy=Py, status="Active", is_Expired=False).order_by('-id')
    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        id = Data.get('id')
        d_Medicine = Add_New_Medicine.objects.get(id=id)
        d_Medicine.status = "Delete",
        d_Medicine.save()
        messages.error(request, name + "  Medicine is Deleted Successfully")
        # return redirect(request, add_new_Medicine)
        return redirect(Medicine_delete)

    # Data = {"Current_pharmacy": Current_pharmacy, 'all_Medicine': all_Medicine,
    #         'error_message': error_message, "success": success}
    # return render(request, "Admin_site/view_test_list.html", Data)

    Data = {"Current_pharmacy": Current_pharmacy, 'all_Medicine': all_Medicine,
            'error_message': error_message}
    return render(request, "Pharmacy_Admin/View_Medicine_List.html", Data)


@Phy_middleware
def update_Medicine(request):
    error_message = None
    success = None
    Py = request.session.get('Phy_id')
    Current_pharmacy = Pharmacy.objects.get(id=Py)
    all_Medicine = Add_New_Medicine.objects.filter(Pharmacy=Py, status="Active", is_Expired=False).order_by('-id')
    if request.method == 'POST':
        id = request.POST.get('id')
        Update_Medicine = Add_New_Medicine.objects.get(id=id)
        Data = request.POST
        name = Data.get('name')
        Price = Data.get('Price')
        Expiry_Date = Data.get("Expiry_Date")
        if Update_Medicine.Medicine_packaging == "Blister packs":
            Medicine_type = Data.get('Medicine_type2')
        else:
            Medicine_type = Data.get("Medicine_type")
        # Medicine_type2 = Data.get('Medicine_type2')
        Total_Stock = Data.get("Stock")

        if Expiry_Date:
            date_time_obj = datetime.strptime(Expiry_Date, '%Y-%m-%d')
            back_day = timedelta(days=14)
            Expiry_Alert_Date = date_time_obj - back_day
            Update_Medicine.Expiry_Alert_Date = Expiry_Alert_Date
            Update_Medicine.Medicine_Expiry_date = Expiry_Date

        if Medicine_type == 'Blister packs':
            Update_Medicine.Medicine_packaging = "Blister packs"
        else:
            Update_Medicine.Medicine_packaging = "Bottles\Sachets"
        Update_Medicine.Medicine_name = name
        Update_Medicine.Medicine_price = Price
        Update_Medicine.Total_Stock = Total_Stock
        Update_Medicine.save()
        messages.error(request, name + "  Medicine is updated Successfully")
        # return redirect(request, add_new_Medicine)
        return redirect(update_Medicine)

    id = request.GET.get('id')
    if id:
        Update_Medicine = Add_New_Medicine.objects.get(id=id)
        dat = Update_Medicine.Medicine_Expiry_date
        day = Update_Medicine.Medicine_Expiry_date.day
        Month = Update_Medicine.Medicine_Expiry_date.month

        year = Update_Medicine.Medicine_Expiry_date.year
        date = Update_Medicine.Medicine_Expiry_date
        date = str(date)
        print(year, Month, day, date)
        data = {'Current_pharmacy': Current_pharmacy, 'Update_Medicine': Update_Medicine,
                'year': year, "Month": Month, 'day': day, "date": date}
        return render(request, "Pharmacy_Admin/Update_Medicine_Detail.html", data)

    all_Medicine = Add_New_Medicine.objects.filter(Pharmacy=Py, status="Active", is_Expired=False).order_by('-id')
    Data = {"Current_pharmacy": Current_pharmacy, 'all_Medicine': all_Medicine, 'success': success}
    return render(request, "Pharmacy_Admin/View_Medicine_List.html", Data)

@Phy_middleware
def View_all_new_Orders(request):
    Py = request.session.get('Phy_id')
    Current_pharmacy = Pharmacy.objects.get(id=Py)
    All_Orders = order.objects.filter(Pharmacy=Py, status='Pending')
    data = {"Current_pharmacy": Current_pharmacy,
            'All_Orders': All_Orders}
    return render(request, "Pharmacy_Admin/Orders/View_all_new_Orders.html", data)

@Phy_middleware
def view_all_comfirm_Orders(request):
    Py = request.session.get('Phy_id')
    Current_pharmacy = Pharmacy.objects.get(id=Py)
    All_Orders = order.objects.filter(Pharmacy=Py, status='Conform')
    data = {"Current_pharmacy": Current_pharmacy,
            'All_Orders': All_Orders}
    return render(request, "Pharmacy_Admin/Orders/view_all_comfirm_Orders.html", data)

@Phy_middleware
def view_all_complete_Orders(request):
    Py = request.session.get('Phy_id')
    Current_pharmacy = Pharmacy.objects.get(id=Py)
    All_Orders = order.objects.filter(Pharmacy=Py, status='Delivered')
    data = {"Current_pharmacy": Current_pharmacy,
            'All_Orders': All_Orders}
    return render(request, "Pharmacy_Admin/Orders/view_complete_orders.html", data)


@Phy_middleware
def order_cancel_confirm(request):
    if request.method == 'POST':
        Data = request.POST
        name = Data.get('action')
        id = Data.get('id')
        if name == 'cancel':
            order_Cancel = order.objects.get(id=id)
            order_Cancel.status = 'Cancelled'
            Quantity = order_Cancel.quantity
            order_Cancel.is_Cancel = True
            order_Cancel.save()
            Medicine = Add_New_Medicine.objects.get(id=order_Cancel.Medicine.id)
            Medicine.Total_Stock = Medicine.Total_Stock + int(Quantity)
            Medicine.save()
            messages.error(request, "Medicine Order is Cancel Successfully")
        elif name == 'confirm_Rider':
            order_Confirm = order.objects.get(id=id)
            order_Confirm.status = 'Conform'
            order_Confirm.Delivery_by = 'By_Rider'
            order_Confirm.save()
            messages.error(request, "Medicine Order is Confirm Successfully and Sent Rider Request\n"
                                    " Rider will pick Medicine from shop within 30 minutes ")
        elif name == 'By_Self':
            order_Confirm = order.objects.get(id=id)
            order_Confirm.status = 'Conform'
            order_Confirm.Delivery_by = 'Self'
            order_Confirm.save()
            messages.error(request, "Medicine Order is Confirm Successfully")
        elif name == 'Out For Delivery':
            order_Confirm = order.objects.get(id=id)
            order_Confirm.status = 'Out for delivery'
            order_Confirm.save()
            messages.error(request, "Medicine Order is Out For Delivery Now")
        elif name == 'Delivered':
            order_Confirm = order.objects.get(id=id)
            order_Confirm.status = 'Delivered'
            order_Confirm.payment = 'Paid'
            order_Confirm.save()
            messages.error(request, "Medicine Order is Delivery and Receive Cash")
        else:
            order_Confirm = order.objects.get(id=id)
            order_Confirm.status = 'Conform'
            order_Confirm.save()
            messages.error(request, "Medicine Order is Confirm Successfully")

    return redirect("/Phy_admin/#examples")


def cart_add(request, id):
    # pa = request.session.get('id')
    # Customer = Patient.objects.filter(id=pa)
    # if Customer:
    cart = Cart(request)
    product = Add_New_Medicine.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


# return redirect('/Login?next=/Carts/cart_add/')


# @login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Add_New_Medicine.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


# @login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Add_New_Medicine.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


# @login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Add_New_Medicine.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


# @login_required(login_url="/Login/")
def cart_detail(request):
    pa = request.session.get('id')
    Customer = Patient.objects.filter(id=pa)
    labcity = Labcity.objects.all()
    if Customer:
        Customer = Patient.objects.filter(id=pa)
        Data = {"Customer": Customer, 'labcity': labcity,
                "message": messages}
        return render(request, "Carts.html", Data)
    else:
        Data = {'labcity': labcity, "message": messages}
        return render(request, "Carts.html", Data)


@Patient_middleware
def Checkout(request):
    pa = request.session.get('id')
    Customer = Patient.objects.filter(id=pa)
    labcity = Labcity.objects.all()
    if Customer:
        Customer = Patient.objects.filter(id=pa)
        Data = {"Customer": Customer, 'labcity': labcity,
                "message": messages}
        return render(request, 'Checkout.html', Data)


# //////////////////////////Functions Related Medicine_list Add_New/Edit/Delete End///////////////////////////////////////////

# //////////////////////////Functions Related View Expiry or expiry Soon Medicine_list Start///////////////////////////////////////////
@Phy_middleware
def view_Expired_Medicine_list(request):
    Py = request.session.get('Phy_id')
    Current_pharmacy = Pharmacy.objects.get(id=Py)
    w = datetime.date(now())

    all_Medicine = Add_New_Medicine.objects.filter(Pharmacy=Py, is_Expired=False).order_by('-id')
    for i in all_Medicine:
        if w > i.Medicine_Expiry_date:
            if not i.is_Expired:
                i.is_Expired = True
                i.save()
    all_Medicine = Add_New_Medicine.objects.filter(Pharmacy=Py, status="Active", is_Expired=True).order_by('-id')

    Data = {"Current_pharmacy": Current_pharmacy, 'all_Medicine': all_Medicine}
    return render(request, "Pharmacy_Admin/View_Expiry_Medicine.html", Data)


@Phy_middleware
def view_Expiry_Soon_Medicine_list(request):
    Py = request.session.get('Phy_id')
    Current_pharmacy = Pharmacy.objects.get(id=Py)
    w = datetime.date(now())
    all_Medicine = Add_New_Medicine.objects.filter(Pharmacy=Py, is_Expired=False, status="Active",
                                                   Expiry_Alert_Date__lt=w).order_by('-id')

    Data = {"Current_pharmacy": Current_pharmacy, 'all_Medicine': all_Medicine}
    return render(request, "Pharmacy_Admin/Medicine_Expiry_Soon.html", Data)


# //////////////////////////Functions Related View Expiry or expiry Soon Medicine_list End///////////////////////////////////////////


# ///////////////////////////////////////Forget Password Email Sent ////////////////////////////////////////////////////

def ChangePassword_Pharmacy(request, token):
    context = {}

    try:
        profile_obj = Pharmacy.objects.get(forget_password_token=token)
        la = profile_obj.id
        context = {'user_id': la}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = la
            print(user_id, 'print 2')
            if user_id is None:
                messages.success(request, 'No user id found.')
                print(user_id, 'print 3')

                return redirect(f'/change-password_Pharmacy/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password_Pharmacy/{token}/')

            user_obj = Pharmacy.objects.get(id=user_id)
            user_obj.password = new_password
            user_obj.save()
            user_obj = Pharmacy.objects.get(id=la)
            token = str(uuid.uuid4())
            profile_obj = Pharmacy.objects.get(email=user_obj.email)
            profile_obj.forget_password_token = token
            profile_obj.save()
            success_message = 'Your Password has been changed Now '
            return render(request, 'Pharmacy_login.html', {'success': success_message})
        else:
            return render(request, 'change-password.html')


    except Exception as e:
        print(e)
    return render(request, 'Link_experiy.html', context)


def ForgetPassword_Pharmacy(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            print(username)

            if not Pharmacy.objects.filter(email=username).first():
                messages.error(request, 'Not user found with this username.')
                return redirect('/forget-password Pharmacy/')

            user_obj = Pharmacy.objects.get(email=username)
            token = str(uuid.uuid4())
            print(token)
            profile_obj = Pharmacy.objects.get(email=username)
            print(profile_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail_Pharmacy(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password Pharmacy/')



    except Exception as e:
        print(e)
    return render(request, 'forget-password.html')

# ///////////////////////////////////// Forget Password Email Sent End  ////////////////////////////////////////////////
