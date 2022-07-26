import datetime
import uuid
from datetime import *

from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.timezone import now

from Laboratory.Middleware.Lab_auth import Lab_middleware
from Laboratory.models.Book_lab_test import Book_Test
from Laboratory.models.Lab_tests_list import Test_list
from Laboratory.models.Labcity import Labcity
from Laboratory.models.Samplest import Samplest
from Laboratory.models.add_lab import Lab
from mainpage.Sent_Email import send_forget_password_mail_Lab
from mainpage.models.Patient import Patient
from Doctor.models.appointments import Appointment
from Doctor.models.save_reports import Save_Medical_Reports


# Create your views here.
def Labs(request, id):
    labcity = Labcity.objects.all()
    labcitys = Labcity.objects.all()
    Test_name = Test_list.objects.all()
    all_lab = Lab.objects.all()
    Customer = Patient.objects.all()
    book_Test = Book_Test.objects.all()
    w = datetime.date(now())
    print(w)
    for i in book_Test:
        if w > i.Test_date:
            if i.status == 'Pending':
                i.status = 'Dispatch'
                i.save()
            print(i.Test_date)

    if request.method == 'POST':
        ser = request.POST.get('search')
        labcity = Labcity.objects.filter(Lab_city_name=ser)
        Test_name = Test_list.objects.filter(Test_name=ser)
        labs = Lab.objects.filter(Labname=ser)
        if labcity:
            LabCity = Labcity.objects.filter(id=labcity)
            ci = LabCity

            for d in ci:
                s = d.id

            labs = Lab.objects.filter(city=s)

            data = {'labs': labs, 'ci': ci, 'labcity': labcity,
                    'all_lab': all_lab, 'labcitys': labcitys, 'Test_name': Test_name, 'Customer': Customer}
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

        labs = Lab.objects.filter(city=s)

        data = {'labs': labs, 'ci': ci, 'labcity': labcity,
                'all_lab': all_lab, 'labcitys': labcitys, 'Test_name': Test_name, 'Customer': Customer}
    else:
        labs = Lab.objects.all()
        data = {'labs': labs, 'labcity': labcity,
                'all_lab': all_lab, 'labcitys': labcitys,
                'Test_name': Test_name, 'Customer': Customer}

    return render(request, "index.html", data)


def lab_search(request):
    global d

    labcity = Labcity.objects.all()
    labcitys = Labcity.objects.all()
    Test_name = Test_list.objects.all()
    all_lab = Lab.objects.all()
    labs = Lab.objects.all()
    Customer = Patient.objects.all()

    if request.method == 'POST':
        ser = request.POST.get('search')
        Labcitys = Labcity.objects.filter()
        labcity = Labcity.objects.filter(Lab_city_name__startswith=ser)
        Test_name = Test_list.objects.filter(Test_name__startswith=ser)
        labs = Lab.objects.filter(Labname__startswith=ser)
        # print(ser)
        # print(Labcitys)
        print('Lab City out ', labcity)

        if labcity:
            print('Lab City', labcity)
            for i in labcity:
                d = i.id
                print(d)
                LabCity = Labcity.objects.filter(id=d)
                ci = LabCity
                print(ci)

            for d in ci:
                s = d.id

            labs = Lab.objects.filter(city=s)
            labcity = Labcity.objects.all()
            data = {'labs': labs, 'ci': ci, 'labcity': labcity,
                    'all_lab': all_lab, 'labcitys': labcitys, 'Test_name': Test_name, 'Customer': Customer}
            return render(request, "index.html", data)
        elif labs:
            print(labs)
            for i in labs:
                d = i.id
                s = i.Labname
                print(d)
            labs = Lab.objects.filter(Labname=s)
            labcity = Labcity.objects.all()
            data = {'labs': labs, 'labcity': labcity, 'Customer': Customer}
            return render(request, 'Search_via_lab name.html', data)
        elif Test_name:
            print(Test_name)
            for i in Test_name:
                d = i.id
                s = i.Test_name
                print(d)
            Test_name = Test_list.objects.filter(Test_name=s)
            labcity = Labcity.objects.all()
            data = {'Test_name': Test_name, 'labcity': labcity,
                    'labs': labs,
                    'all_lab': all_lab, 'labcitys': labcitys,
                    'Customer': Customer
                    }
            return render(request, 'Search_via_test_name.html', data)
        else:
            data = {'Test_name': Test_name, 'labcity': labcity,
                    'labs': labs, 'ser': ser,
                    'all_lab': all_lab, 'labcitys': labcitys,
                    'Customer': Customer
                    }
            return render(request, 'Search_via_test_name.html', data)

    data = {'labs': labs,
            'labcity': labcity,
            'all_lab': all_lab,
            'labcitys': labcitys,
            'Test_name': Test_name,
            'Customer': Customer}

    return Labs(request, 400)


def test_list(request, id):
    data = {}
    labcity = Labcity.objects.all()
    Customer = Patient.objects.all()
    testlist = Test_list.objects.filter(laboratory=id)
    if id != 400:
        LabCity = Labcity.objects.filter(id=id)
        ci = LabCity

        labs = Lab.objects.filter(id=id)
        data = {'labs': labs, 'ci': ci, 'labcity': labcity, 'testlist': testlist, 'Customer': Customer}
    # else:
    #     labs = Lab.objects.all()
    #     data = {'labs': labs, 'labcity': labcity}
    return render(request, 'View lab_test_list.html', data)


def Booking_form(request, id):
    data = {}
    labcity = Labcity.objects.all()
    pa = request.session.get('id')
    Customer = Patient.objects.filter(id=pa)
    if request.method == 'POST':
        Data = request.POST
        email = Data.get('email')
        email = Patient.objects.get(id=email)
        name = Data.get('name')
        phone = Data.get('phone')
        city = Data.get('city')
        labname = Data.get('labname')
        date = Data.get('Test_Date')
        labname = Lab.objects.get(id=labname)
        test_name = Data.get('test_name')
        test_name = Test_list.objects.get(id=test_name)
        test_price = Data.get('test_price')
        Address = Data.get('address')
        Test_type = Data.get('Test_type')
        print(Test_type)
        Booking_test = Book_Test(Patient_Name=name, city=city, email=email, Phone=phone, Address=Address,
                                 Laboratory=labname, Book_Test=test_name, Test_date=date, Test_Type=Test_type)
        Booking_test.save()
        Latest_order = Book_Test.objects.all().order_by('-id')

        data = {'labcity': labcity, 'Latest_order': Latest_order, 'Customer': Customer}
        return render(request, 'Order_booked_id.html', data)
    else:
        Booktest = Test_list.objects.filter(id=id)
        # test = Test_list.objects.filter(id=id)
        datetime.now()
        data = {'labcity': labcity, 'Booktest': Booktest, 'Customer': Customer}
    return render(request, 'Test booking forn.html', data)


def View_Your_Appointments(request, id):
    labcity = Labcity.objects.all()
    pa = request.session.get('id')
    Customer = Patient.objects.filter(id=pa)
    patient = Patient.objects.get(id=pa)
    book_Test = Book_Test.objects.filter(email=id)
    book_appointments = Appointment.objects.filter(Patients=pa)
    Save_reports = Save_Medical_Reports.objects.filter(Patient=pa)
    error_message = None
    success = None
    re = "Patient_save_Reports/cancel_btn.png"
    w = datetime.date(now())
    # print(w)
    for i in book_Test:
        if w > i.Test_date:
            if i.status == 'Pending':
                i.status = 'Dispatch'
                i.save()

    for i in book_appointments:
        if w > i.Appointment_date:
            if i.Status == 'Pending':
                i.Status = 'Dispatch'
                i.save()

    if request.method == 'POST':
        data = request.POST
        Attach_file = data.get("report_attach")
        app_id = data.get("app_id")
        appointment = Appointment.objects.get(id=app_id)
        Attach_report = Save_Medical_Reports.objects.get(id=Attach_file)

        print("report_attach = ", Attach_report)
        appointment.Medical_report_1 = Attach_report
        appointment.save()
        success = Attach_report, " is Attach with your Appointment"

    data = {'book_Test': book_Test, 'labcity': labcity, 'w': w,
            'Customer': Customer, "book_appointments": book_appointments,
            "Save_reports": Save_reports, "patient": patient, "success": success, "re": re}
    return render(request, 'View Your Appointments and orders.html', data)


# ///////////////////////////////////////Laboratory admin Login ////////////////////////////////////////////////////////
def Lab_Login(request):
    if request.method == 'GET':
        if request.session.get("required_path"):
            path = request.session.get("required_path")
            return render(request, 'Lab_login.html', {'path': path})
        else:
            return render(request, 'Lab_login.html')
    else:
        Data = request.POST
        email = Data.get('email')
        password = Data.get('password')

        # # Validations
        Laboratory = Lab.objects.filter(email=email, password=password)
        Laboratory_active = Lab.objects.filter(email=email, password=password, is_Active=True)

        error_message = None
        #

        if Laboratory:
            if not Laboratory_active:
                error_message = email + " is Deactivated by the TakeCare Team"
                return render(request, 'Lab_login.html', {'error': error_message})
            for i in Laboratory:
                request.session['lab_id'] = i.id
                request.session['lab_email'] = i.email
                path = request.session.get("required_path")
                if path:
                    return redirect(path)
                else:
                    return redirect(lab_admin)
        else:
            error_message = "Email or Password Invalid......"

        # return render(request, 'Login.html', {'error': error_message})
    return render(request, 'Lab_login.html', {'error': error_message})


# ////////////////////////////Functions Related  Laboratory Admin Dashboard+profile page start///////////////////////////
@Lab_middleware
def lab_admin(request):
    error_message = None
    success = None
    request.session['required_path'] = None

    Test_today = 0
    month = datetime.now().month
    year = datetime.now().year
    lb = request.session.get('lab_id')
    # print(lb)
    samplest = Samplest.objects.filter(Laboratory=lb).order_by('-id')
    current_lab = Lab.objects.get(id=lb)
    Test_count = Test_list.objects.filter(laboratory=lb).count()
    Test_pending = Book_Test.objects.filter(status='Pending', Laboratory=lb).count()
    Test_conform = Book_Test.objects.filter(status='Conform', Laboratory=lb).count()
    Test_col = Book_Test.objects.filter(status='Sample Collected', Laboratory=lb, Test_date=datetime.now()).count()
    tol_Samplest = Samplest.objects.filter(Laboratory=lb).count()
    Test_today_count = Book_Test.objects.filter(Test_date=datetime.now(), Laboratory=lb)
    Test_mouth = Book_Test.objects.filter(month=month, Laboratory=lb).count()
    Test_year = Book_Test.objects.filter(year=year, Laboratory=lb).count()

    all_Test = Test_list.objects.filter(laboratory=lb).order_by('-id')
    Test_pending_booking = Book_Test.objects.filter(status='Pending', Laboratory=lb)
    # Test_conform_booking = Book_Test.objects.filter(Laboratory=lb)
    Test_conform_booking_today = Book_Test.objects.filter(Laboratory=lb, Test_date=datetime.now())

    book_Test = Book_Test.objects.all()
    w = datetime.date(now())
    print(w)
    for i in book_Test:
        if w > i.Test_date:
            if i.status == 'Pending':
                i.status = 'Dispatch'
                i.save()
            print(i.Test_date)

    for j in Test_today_count:
        if j.status != 'Pending':
            Test_today = Test_today + 1

    all_lab = Lab.objects.all()
    Total_pat = Lab.objects.all().count()
    all_pat = Patient.objects.all().count()

    if request.method == 'POST':
        data = request.POST
        ID = data.get('id')
        Test = Book_Test.objects.get(id=ID)
        Status = data.get('name')

        Select_samplest = data.get('Select_samplest')
        print(Select_samplest)
        if Status == 'Samplest_Collected':
            Test.status = 'Sample Collected'
            Test.save()
            success = 'Test Status Change Successfully'
        elif Status == 'test_id':
            img = request.FILES.get('image')
            Report = Book_Test.objects.get(id=ID)
            Report.Test_report = img
            Report.status = "Test Report"
            Report.save()
            success = 'Test Report Uploaded Successfully'
        elif Status == "Payment_received":
            Payment = Book_Test.objects.get(id=ID)
            Payment.payment = "Paid"
            Payment.save()
            success = 'Test Payment Received Successfully'
        else:
            Samplest_assign = Samplest.objects.get(name=Select_samplest)
            Test.Samplest = Samplest_assign
            Test.save()
            success = 'Samplest Change Successfully'

    data = {'all_lab': all_lab, 'all_pat': all_pat,
            'Total_pat': Total_pat, 'current_lab': current_lab,
            'Test_count': Test_count, 'Test_pending': Test_pending,
            'Test_conform': Test_conform, 'Test_today': Test_today,
            'Test_mouth': Test_mouth, 'Test_year': Test_year,
            'Test_col': Test_col, 'tol_Samplest': tol_Samplest,
            'all_Test': all_Test, 'samplest': samplest,
            'Test_pending_booking': Test_pending_booking,
            'Test_conform_booking_today': Test_conform_booking_today,
            'success': success,
            }
    return render(request, "Admin_site/index.html", data)


@Lab_middleware
def Lab_profile(request):
    lb = request.session.get('lab_id')
    error_message = None
    success = None

    flag = False
    Lab_profile = Lab.objects.filter(id=lb)
    labcity = Labcity.objects.all()
    current_lab = Lab.objects.get(id=lb)

    if request.method == 'POST':
        data = request.POST
        Current_password = data.get('C_pass')
        New_password = data.get('New_password')
        Confirm_password = data.get('NConform_pass')
        for i in Lab_profile:
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
            Cus = Lab.objects.get(id=lb)
            Cus.password = New_password
            Cus.save()
            success = "Your Password Updated Successfully"

        else:
            error_message = "Please Check Your Current Password You Enter"

    Data = {'Lab_profile': Lab_profile, 'labcity': labcity,
            'error': error_message, 'current_lab': current_lab,
            'success': success}
    return render(request, "Admin_site/Lab_admin_profile.html", Data)


@Lab_middleware
def Lab_profile_img(request):
    lb = request.session.get('lab_id')
    Laboratory_img = Lab.objects.get(id=lb)
    if request.method == 'POST':
        Laboratory_profile_img = request.FILES.get('image')
        Laboratory_img.img = Laboratory_profile_img
        Laboratory_img.save()
    return redirect(Lab_profile)


@Lab_middleware
def updates_lab_profile(request):
    lb = request.session.get('lab_id')
    error_message = None
    success = None

    Lab_profile = Lab.objects.filter(id=lb)
    labcity = Labcity.objects.all()
    current_lab = Lab.objects.get(id=lb)

    if request.method == 'POST':
        data = request.POST
        name = data.get("username")
        phone = data.get("phone")
        Address = data.get("Address")
        if name:
            name = name.capitalize()
            Profile = Lab.objects.get(id=lb)
            Profile.Username = name
            Profile.save()
            success = "Your Username Change Successfully"
        elif phone:
            if len(phone) < 10:
                error_message = " Password must be At-least 10 digit long without first '0' "
            else:
                Profile = Lab.objects.get(id=lb)
                Profile.Callnumber = phone
                Profile.save()
                success = "Your Phone number Change Successfully"
        elif Address:
            Address = Address.capitalize()
            Profile = Lab.objects.get(id=lb)
            Profile.Address = Address
            Profile.save()
            success = "Your Address Change Successfully"

    Data = {'Lab_profile': Lab_profile, 'labcity': labcity,
            'error': error_message, 'current_lab': current_lab,
            'success': success}
    return render(request, "Admin_site/Lab_admin_profile.html", Data)


# ////////////////////////////Functions Related  Laboratory Admin Dashboard+profile page End///////////////////////////


# //////////////////////////Functions Related Test_list Add_New/Edit/Delete Start///////////////////////////////////////////

@Lab_middleware
def add_new_test(request):
    error_message = None
    success = None
    lb = request.session.get('lab_id')
    current_lab = Lab.objects.get(id=lb)

    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        Price = Data.get('Price')
        Test_type = Data.get('Test_type')
        Is_Exit = Test_list.objects.filter(Test_name=name)
        if Is_Exit:
            error_message = "New with this name is already exit"
            print(error_message)
            Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success}
            return render(request, "Admin_site/Add_new_test.html", Data)

        if Test_type == 'Home Sampling Available':
            Add_New_Test = Test_list(Test_name=name, test_price=Price, laboratory=current_lab, Home_Sample=True)
            Add_New_Test.save()
            success = "New Test is Added Sucessfully"
        else:
            Add_New_Test = Test_list(Test_name=name, test_price=Price, laboratory=current_lab, Home_Sample=False)
            Add_New_Test.save()
            success = "New Test is Added Sucessfully"
        print(error_message, success)
    Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success}
    return render(request, "Admin_site/Add_new_test.html", Data)


@Lab_middleware
def view_test_list(request):
    lb = request.session.get('lab_id')
    current_lab = Lab.objects.get(id=lb)
    all_Test = Test_list.objects.filter(laboratory=lb).order_by('-id')
    Data = {"current_lab": current_lab, 'all_Test': all_Test}
    return render(request, "Admin_site/view_test_list.html", Data)


@Lab_middleware
def test_delete(request):
    error_message = None
    success = None
    lb = request.session.get('lab_id')
    current_lab = Lab.objects.get(id=lb)
    all_Test = Test_list.objects.filter(laboratory=lb).order_by('-id')
    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        id = Data.get('id')
        d_test = Test_list.objects.filter(id=id)
        if d_test:
            d_test = Test_list.objects.get(id=id)
            d_test.delete()
            success = " Deleted Successfully"
        else:
            error_message = " Not Exist or already deleted from System"
        Data = {"current_lab": current_lab, 'all_Test': all_Test, 'error_message': error_message, "success": success,
                'name': name}
        return render(request, "Admin_site/view_test_list.html", Data)
    Data = {"current_lab": current_lab, 'all_Test': all_Test, 'error_message': error_message}
    return render(request, "Admin_site/view_test_list.html", Data)


@Lab_middleware
def update_test(request):
    error_message = None
    success = None
    lb = request.session.get('lab_id')
    current_lab = Lab.objects.get(id=lb)

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            Update_test = Test_list.objects.filter(id=id)
            data = {'current_lab': current_lab, 'Update_test': Update_test}
            return render(request, "Admin_site/Test_update.html", data)
        else:
            return redirect(lab_admin)
    if request.method == 'POST':
        id = request.POST.get('id')
        Update_test = Test_list.objects.get(id=id)
        Data = request.POST
        name = Data.get('name')
        price = Data.get('price')
        Test_type = Data.get('Test_type')
        if Test_type == 'Home Sampling Available':
            Update_test.Home_Sample = True
        else:
            Update_test.Home_Sample = False
        Update_test.Test_name = name
        Update_test.test_price = price
        Update_test.save()
        success = "  updated Sucessfully"
        all_Test = Test_list.objects.filter(laboratory=lb).order_by('-id')
        Data = {"current_lab": current_lab, 'all_Test': all_Test, 'success': success, 'name': name}
        return render(request, "Admin_site/view_test_list.html", Data)


# //////////////////////////Functions Related Test_list Add_New/Edit/Delete End///////////////////////////////////////////


# /////////////////////////Functions Related Samplest Add_New/Edit/Delete/active/deactivate Start/////////////////////////
@Lab_middleware
def add_new_Samplest(request):
    error_message = None
    success = None
    lb = request.session.get('lab_id')
    current_lab = Lab.objects.get(id=lb)

    if request.method == 'POST':
        Data = request.POST
        lb = request.session.get('lab_id')
        current_lab = Lab.objects.get(id=lb)
        name = Data.get('name')
        CNIC = Data.get('CNIC')
        Callnumber = Data.get('phone')
        password = Data.get('password')
        img = request.FILES.get('image')

        Is_Exit = Samplest.objects.filter(CNIC=CNIC, Laboratory=lb)
        if Is_Exit:
            error_message = " This CNIC is already exit"
            Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success, 'name': CNIC}
            return render(request, "Admin_site/add_new_Samplest.html", Data)
        elif len(CNIC) < 13:
            error_message = " This CNIC must be 13 digits"
            Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success, 'name': CNIC}
            return render(request, "Admin_site/add_new_Samplest.html", Data)

        Add_new_Samplest = Samplest(name=name, Callnumber=Callnumber, CNIC=CNIC, password=password,
                                    Laboratory=current_lab, img=img, is_Active=True)
        Add_new_Samplest.save()
        success = "Samplest is Added Sucessfully"
    Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success}
    return render(request, "Admin_site/add_new_Samplest.html", Data)


@Lab_middleware
def View_all_samplest(request):
    error_message = None
    success = None
    lb = request.session.get('lab_id')
    current_lab = Lab.objects.get(id=lb)
    samplest = Samplest.objects.filter(Laboratory=lb).order_by('-id')

    Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success, 'samplest': samplest}
    return render(request, "Admin_site/View_all_samplest.html", Data)


@Lab_middleware
def Status_samplest(request):
    error_message = None
    success = None
    lb = request.session.get('lab_id')
    current_lab = Lab.objects.get(id=lb)
    samplest = Samplest.objects.filter(Laboratory=lb).order_by('-id')

    if request.method == 'POST':
        Data = request.POST
        lb = request.session.get('lab_id')
        current_lab = Lab.objects.get(id=lb)
        name = Data.get('name')
        id = Data.get('id')
        Update_Samplest = Samplest.objects.filter(id=id)
        print(Update_Samplest)
        Update_Samplest = Samplest.objects.get(id=id)

        if Update_Samplest.is_Active:
            Update_Samplest.is_Active = False
            success = name + "is Deactivate Successfully"
        else:
            Update_Samplest.is_Active = True
            success = name + "is Active Successfully"
        Update_Samplest.save()

    Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success, 'samplest': samplest}
    return render(request, "Admin_site/View_all_samplest.html", Data)

    # return redirect(lab_admin)


@Lab_middleware
def Samplest_del(request):
    error_message = None
    success = None
    lb = request.session.get('lab_id')
    current_lab = Lab.objects.get(id=lb)
    samplest = Samplest.objects.filter(Laboratory=lb).order_by('-id')

    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        id = Data.get('id')
        d_Samplest = Samplest.objects.filter(id=id)

        if d_Samplest:
            d_Samplest = Samplest.objects.get(id=id)
            d_Samplest.delete()
            success = name + "Deleted Successfully"
        else:
            error_message = name + " Not Exist or already deleted from System"

    Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success, 'samplest': samplest}
    return render(request, "Admin_site/View_all_samplest.html", Data)


def update_samplest(request, id):
    error_message = None
    success = None
    lb = request.session.get('lab_id')
    samplest = Samplest.objects.filter(Laboratory=lb).order_by('-id')
    current_lab = Lab.objects.get(id=lb)

    Update_Samplest = Samplest.objects.filter(id=id)
    # print(Update_Samplest)
    if request.method == 'POST':
        Update_Samplest = Samplest.objects.get(id=id)
        Data = request.POST
        name = Data.get('name')
        CNIC = Data.get('CNIC')
        Callnumber = Data.get('phone')
        img = request.FILES.get('image')
        if img:
            Update_Samplest.img = img

        print(name, Callnumber)
        Update_Samplest.name = name
        Update_Samplest.Callnumber = Callnumber
        Update_Samplest.CNIC = CNIC
        Update_Samplest.save()
        success = name + "Record is Updated Successfully"
        Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success, 'samplest': samplest}
        return render(request, "Admin_site/View_all_samplest.html", Data)

    data = {'current_lab': current_lab, 'Update_Samplest': Update_Samplest}
    return render(request, "Admin_site/Samplest_update.html", data)


# /////////////////////////Functions Related Samplest Add_New/Edit/Delete/active/deactivate End///////////////////////////


def Test_Booking_conformation(request, id):
    error_message = None
    success = None
    lb = request.session.get('lab_id')
    current_lab = Lab.objects.get(id=lb)
    Test = Book_Test.objects.get(id=id)
    if request.method == 'POST':
        Data = request.POST
        Status = Data.get('name')
        if Status == 'cancel':
            Test.status = "Cancelled"
            Test.save()
            success = "Successfully Cancel This Appointment"
            return redirect(view_all_comfirm_booking)

        Select_samplest = Data.get('Select_samplest')
        print(Select_samplest)
        if Select_samplest != "no_select":
            Samplest_assign = Samplest.objects.get(name=Select_samplest)
            Test.status = "Conform"
            Test.Samplest = Samplest_assign
            Samplest_assign.assign_task = Samplest_assign.assign_task + 1
            Test.save()
            Samplest_assign.save()
            return redirect(view_all_comfirm_booking)

        if Status == 'conform':
            Test.status = "Conform"
            Test.save()
        else:
            Test.status = "Cancelled"
            Test.save()

    return redirect(view_all_comfirm_booking)


@Lab_middleware
def upload_test_report(request):
    lb = request.session.get('lab_id')
    current_lab = Lab.objects.get(id=lb)

    if request.method == 'POST':
        Test_id = request.POST.get("test_id")
        img = request.FILES.get('image')
        Report = Book_Test.objects.get(id=Test_id)
        Report.Test_report = img
        Report.status = "Test Report"
        Report.save()

        all_Test = Test_list.objects.filter(laboratory=lb).order_by('-id')
        Test_pending_booking = Book_Test.objects.filter(status='Pending', Laboratory=lb)
        Test_conform_booking = Book_Test.objects.filter(Laboratory=lb)
        Test_conform_booking_today = Book_Test.objects.filter(Laboratory=lb, Test_date=datetime.now())

        book_Test = Book_Test.objects.all()
        w = datetime.date(now())
        print(w)
        for i in book_Test:
            if w > i.Test_date:
                if i.status == 'Pending':
                    i.status = 'Dispatch'
                    i.save()
                print(i.Test_date)

        data = {'current_lab': current_lab, 'Test_pending_booking': Test_pending_booking,
                'book_Test': book_Test, "Test_conform_booking": Test_conform_booking,
                "Test_conform_booking_today": Test_conform_booking_today, 'all_Test': all_Test}
        return render(request, "Admin_site/view_all_confirm_booking.html", data)

    return redirect(view_all_comfirm_booking)


@Lab_middleware
def view_all_comfirm_booking(request):
    lb = request.session.get('lab_id')
    current_lab = Lab.objects.get(id=lb)

    all_Test = Test_list.objects.filter(laboratory=lb).order_by('-id')
    Test_pending_booking = Book_Test.objects.filter(status='Pending', Laboratory=lb)
    Test_conform_booking = Book_Test.objects.filter(Laboratory=lb)
    Test_conform_booking_today = Book_Test.objects.filter(Laboratory=lb, Test_date=datetime.now())

    book_Test = Book_Test.objects.all()
    w = datetime.date(now())
    print(w)
    for i in book_Test:
        if w > i.Test_date:
            if i.status == 'Pending':
                i.status = 'Dispatch'
                i.save()
            print(i.Test_date)

    data = {'current_lab': current_lab, 'Test_pending_booking': Test_pending_booking,
            'book_Test': book_Test, "Test_conform_booking": Test_conform_booking,
            "Test_conform_booking_today": Test_conform_booking_today, 'all_Test': all_Test}
    return render(request, "Admin_site/view_all_confirm_booking.html", data)


@Lab_middleware
def View_all_new_booking(request):
    lb = request.session.get('lab_id')
    current_lab = Lab.objects.get(id=lb)
    all_Test = Test_list.objects.filter(laboratory=lb).order_by('-id')
    Test_pending_booking = Book_Test.objects.filter(status='Pending', Laboratory=lb)
    samplest = Samplest.objects.filter(Laboratory=lb).order_by('-id')

    Data = {"current_lab": current_lab, 'Test_pending_booking': Test_pending_booking,
            'all_Test': all_Test, 'samplest': samplest}
    return render(request, "Admin_site/View_all_new_booking.html", Data)


# ///////////////////////////////////////Forget Password Email Sent ////////////////////////////////////////////////////

def ChangePassword_Lab(request, token):
    context = {}

    try:
        profile_obj = Lab.objects.get(forget_password_token=token)
        la = profile_obj.id
        context = {'user_id': la}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = la
            print(user_id, 'print 2')
            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password_Lab/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password_Lab/{token}/')

            user_obj = Lab.objects.get(id=user_id)
            user_obj.password = new_password
            user_obj.save()
            user_obj = Lab.objects.get(id=la)
            token = str(uuid.uuid4())
            profile_obj = Lab.objects.get(email=user_obj.email)
            profile_obj.forget_password_token = token
            profile_obj.save()
            success_message = 'Your Password has been changed Now '
            return render(request, 'Lab_login.html', {'success': success_message})
        else:
            return render(request, 'change-password.html')


    except Exception as e:
        print(e)
    return render(request, 'Link_experiy.html', context)


def ForgetPassword_Lab(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            print(username)

            if not Lab.objects.filter(email=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password_Lab/')

            user_obj = Lab.objects.get(email=username)
            token = str(uuid.uuid4())
            print(token)
            profile_obj = Lab.objects.get(email=username)
            print(profile_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail_Lab(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password_Lab/')



    except Exception as e:
        print(e)
    return render(request, 'forget-password.html')

# ///////////////////////////////////// Forget Password Email Sent End  ////////////////////////////////////////////////
