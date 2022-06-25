from datetime import datetime

from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from django.utils.timezone import now

from mainpage.models.Patient import Patient
from Laboratory.models.Labcity import Labcity
from Laboratory.models.add_lab import Lab

from Laboratory.Middleware.Lab_auth import Lab_middleware, Lab_login_check
from mainpage.Middleware.Patient_auth import Patient_middleware

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from mainpage.Sent_Email import send_forget_password_mail
from Doctor.models.ADD_Docror import Doctors
from Doctor.models.appointments import Appointment
from Doctor.models.save_reports import Save_Medical_Reports
from Pharmacy_Store.models.Add_Medicine import Add_New_Medicine
import uuid


# Create your views here.
def about_us(request):
    Data = {}
    return render(request, 'about.html', Data)


@Lab_login_check
def mainindex(request):
    labcity = Labcity.objects.all()
    # Data = {'labcity': labcity}
    Customer = Patient.objects.all()
    All_Doctor = Doctors.objects.all()
    cs = 'Child Specialist'
    Child_Specialist = Doctors.objects.filter(Speciality=cs).count()

    w = datetime.date(now())
    all_Medicine = Add_New_Medicine.objects.filter(is_Expired=False)
    for i in all_Medicine:
        if w > i.Medicine_Expiry_date:
            if not i.is_Expired:
                i.is_Expired = True
                i.save()

    Data = {'labcity': labcity, 'Customer': Customer,
            'All_Doctor': All_Doctor,
            'Child_Specialist': Child_Specialist}

    return render(request, 'slider.html', Data)


@Lab_login_check
def registeruser(request):
    Data = request.POST
    fullname = Data.get('fullname')
    email = Data.get('email')
    password = Data.get('password')
    C_password = Data.get('C_password')
    phone = Data.get('Mn')
    city = Data.get('city')
    Address = Data.get('address')
    # gender = Data.get('gender')
    print(fullname, email, password, C_password, phone)
    # Validations
    value = {
        'fullname': fullname,
        'email': email,
        'password': password,
        'C_password,': C_password,
        'phone': phone,
        # 'gender': gender
    }
    error_message = None
    Customer = Patient(name=fullname, email=email, password=password, Mn=phone, city=city, Address=Address)

    if not fullname:
        error_message = "Fullname is Required."
    elif len(fullname) < 4:
        error_message = "Fullname must be 4 char long or more"
    elif len(password) < 8:
        error_message = "Password must be minimum 8 char long or more"
    elif password != C_password:
        error_message = 'Password and Comfort Password must be same'
    elif not phone:
        error_message = "Phone number is Required."
    elif len(phone) < 10:
        error_message = " Phone number must be 10 digit long "
    elif city == 'No-cities':
        error_message = 'Please select your city'
    elif Customer.isExits():
        error_message = "Email Already Exits "
    # Saving
    if not error_message:
        Customer.password = make_password(Customer.password)
        Customer.save()
        # Customer = Customer.get_by_email(email)
        # request.session['id'] = Customer.id
        # print(request.session.id)
        # print(Customer.email, Customer.id)
        return redirect(mainindex)
    else:
        data = {
            'error': error_message,
            'Value': value
        }
    return render(request, 'Signup.html', data)


@Lab_login_check
def Signup(request):
    if request.method == 'GET':
        return render(request, 'Signup.html')
    else:
        return registeruser(request)


@Lab_login_check
def Login(request):
    if request.method == 'GET':
        return render(request, 'Login.html')
    else:
        print('view reach ')
        Data = request.POST
        email = Data.get('email')
        password = Data.get('password')

        # Validations
        Customer = Patient.get_by_email(email)
        error_message = None
        Customer_active = Patient.objects.filter(email=email, is_Active=True)

        if not Customer_active:
            error_message = email + " is Deactivated by the TakeCare Team"
        elif Customer:
            print(Customer.password)
            flag = check_password(password, Customer.password)
            print('pass not match', Customer)
            if flag:
                request.session['id'] = Customer.id
                fa = request.session['email'] = Customer.email
                request.session['phone'] = Customer.Mn
                request.session['Address'] = Customer.Address
                request.session['fullname'] = Customer.name
                request.session['city'] = Customer.city
                print('you are ', Customer)
                print('customer Login')
                return redirect(mainindex)
            else:
                error_message = "Email or Password Invalid......"
        else:
            error_message = "Email or Password Invalid......"

        return render(request, 'Login.html', {'error': error_message})


def Logout(request):
    Phy_id = request.session.get('Phy_id')
    Customer_id = request.session.get('id')
    if Phy_id:
        request.session['Phy_id'] = None
        request.session.get['Phy_email'] = None
    elif Customer_id:
        request.session['id'] = None
        request.session['email'] = None
        request.session['phone'] = None
        request.session['Address'] = None
        request.session['fullname'] = None
        request.session['city'] = None
    else:
        request.session.clear()
    return redirect(mainindex)


@Patient_middleware
def Save_Records(request):
    pa = request.session.get('id')
    Customer = Patient.objects.filter(id=pa)
    labcity = Labcity.objects.all()
    prescription_records = Appointment.objects.filter(Patients=pa)
    Save_Reports = Save_Medical_Reports.objects.filter(Patient=pa)
    prescription_records_count = Appointment.objects.filter(Patients=pa, Status="Completed").count()
    Data = {"Customer": Customer, "labcity": labcity,
            "prescription_records": prescription_records,
            "prescription_records_count": prescription_records_count,
            "Save_Reports": Save_Reports}
    return render(request, "medical_Record.html", Data)


@Patient_middleware
def Add_new_Reports(request):
    pa = request.session.get('id')
    Customer = Patient.objects.filter(id=pa)
    Patients = Patient.objects.get(id=pa)
    labcity = Labcity.objects.all()
    error_message = None
    success = None

    if request.method == 'POST':
        data = request.POST
        report = request.FILES.get("report")
        Report_Title = data.get("Report_Title")
        Report_Date = data.get("Test_Date")
        Time = data.get("Time")
        Doctor_name = data.get("Doctor_name")
        Patient_name = data.get("Patient_name")
        Notes = data.get("Notes")
        Add_new_report = Save_Medical_Reports(Reports=report, Report_Title=Report_Title,
                                              Doctor_name=Doctor_name, Patient_name=Patient_name,
                                              Date=Report_Date, Report_time=Time, Note=Notes,
                                              Patient=Patients)
        Add_new_report.save()
        return redirect("Save_medical_Records")

        # car = Save_Medical_Reports.objects.filter(Reports=report, Report_Title=Report_Title).order_by('-id')
        # files = []
        # for i in car:
        #     files.append(i.Reports)
        #     break
        # for f in files:
        #     shutil.copy(f, "static/Reports/")

    # success = "Patient new Report is Save Successfully"
    # prescription_records = Appointment.objects.filter(Patients=pa)
    # Save_Reports = Save_Medical_Reports.objects.filter(Patient=pa)
    # prescription_records_count = Appointment.objects.filter(Patients=pa, Status="Completed").count()
    #
    # Data = {"Customer": Customer, "labcity": labcity,
    #         "prescription_records": prescription_records,
    #         "prescription_records_count": prescription_records_count,
    #         "Save_Reports": Save_Reports, "success": success}
    # return render(request, "medical_Record.html", Data)

    Data = {'Customer': Customer,
            'labcity': labcity, 'error': error_message,
            'success': success}
    return render(request, "Add_new_medical_Reports.html", Data)


def view_report_detail(request, id):
    pa = request.session.get('id')
    Customer = Patient.objects.filter(id=pa)
    Patients = Patient.objects.get(id=pa)
    Edit_records = Save_Medical_Reports.objects.get(Patient=pa, id=id)
    report_date = Edit_records.Date
    print(report_date)
    labcity = Labcity.objects.all()
    error_message = None
    success = None
    Data = {'Customer': Customer, "Edit_records": Edit_records,
            'labcity': labcity, 'error': error_message,
            'success': success, "report_date": report_date}
    return render(request, "view_report_detail.html", Data)


def Update_Reports(request, id):
    pa = request.session.get('id')
    Customer = Patient.objects.filter(id=pa)
    Patients = Patient.objects.get(id=pa)
    Edit_records = Save_Medical_Reports.objects.get(Patient=pa, id=id)
    report_date = Edit_records.Date
    print(report_date)
    labcity = Labcity.objects.all()
    error_message = None
    success = None
    if request.method == 'POST':
        data = request.POST
        report = request.FILES.get("report")
        Report_Title = data.get("Report_Title")
        Report_Date = data.get("Test_Date")
        Time = data.get("Time")
        Doctor_name = data.get("Doctor_name")
        Patient_name = data.get("Patient_name")
        Notes = data.get("Notes")
        print(report, Report_Title, Patient_name, Doctor_name)

        if report:
            Edit_records.Reports = report

        Edit_records.Report_Title = Report_Title
        Edit_records.Doctor_name = Doctor_name
        Edit_records.Patient_name = Patient_name
        if Report_Date:
            Edit_records.Date = Report_Date
        if Time:
            Edit_records.Report_time = Time
        Edit_records.Note = Notes
        #  Patient=Patients
        Edit_records.save()
        success = " Medical Report Record Updated Successfully"
        return redirect(Save_Records_confirmation, success)

    Data = {'Customer': Customer, "Edit_records": Edit_records,
            'labcity': labcity, 'error': error_message,
            'success': success, "report_date": report_date}
    return render(request, "Update_Reports.html", Data)


def Save_Records_confirmation(request, message):
    pa = request.session.get('id')
    Customer = Patient.objects.filter(id=pa)
    labcity = Labcity.objects.all()
    prescription_records = Appointment.objects.filter(Patients=pa)
    Save_Reports = Save_Medical_Reports.objects.filter(Patient=pa)
    prescription_records_count = Appointment.objects.filter(Patients=pa, Status="Completed").count()
    error_message = None
    success = message

    Data = {"Customer": Customer, "labcity": labcity,
            "prescription_records": prescription_records,
            "prescription_records_count": prescription_records_count,
            "Save_Reports": Save_Reports, "success": success}
    return render(request, "medical_Record.html", Data)


@Patient_middleware
# @login_required(login_url='/Login/')
def Patient_Setting(request):
    pa = request.session.get('id')
    Customer = Patient.objects.filter(id=pa)
    labcity = Labcity.objects.all()
    error_message = None
    success = None
    flag = False
    sa = 0
    if request.method == 'POST':
        data = request.POST
        Current_password = data.get('C_pass')
        New_password = data.get('New_password')
        Confirm_password = data.get('NConform_pass')
        for i in Customer:
            sa = i.password
            print(sa)
            flag = check_password(Current_password, sa)
            print(flag)

        if New_password != Confirm_password:
            error_message = 'Password and Comfort Password must be same'
        elif len(New_password) < 8:
            error_message = " Password must be At-least 8 digit long "
        elif flag:
            Cus = Patient.objects.get(id=pa)
            Cus.password = make_password(New_password)
            Cus.save()
            success = "Your Password Updated Successfully"

        else:
            error_message = "Please Check Your Current Password You Enter"

    patient = Patient.objects.filter(id=pa)
    Data = {'patient': patient, 'Customer': Customer,
            'labcity': labcity, 'error': error_message,
            'success': success}
    return render(request, "Patient_Setting.html", Data)


@Patient_middleware
# @login_required(login_url='/Login/')
def Change_patient_profile_img(request):
    pa = request.session.get('id')
    Customer = Patient.objects.get(id=pa)
    if request.method == 'POST':
        Patient_img = request.FILES.get('image')
        Customer.img = Patient_img
        Customer.save()
    return redirect(Patient_Setting)


@Patient_middleware
def updates_patient_profile(request):
    pa = request.session.get('id')
    Customer = Patient.objects.filter(id=pa)
    labcity = Labcity.objects.all()
    error_message = None
    success = None

    if request.method == 'POST':
        data = request.POST
        name = data.get("username")
        phone = data.get("phone")
        Address = data.get("Address")
        if name:
            name = name.capitalize()
            Profile = Patient.objects.get(id=pa)
            Profile.name = name
            Profile.save()
            success = "Your Username Change Successfully"
        elif phone:
            if len(phone) < 10:
                error_message = " Password must be At-least 10 digit long without first '0' "
            else:
                Profile = Patient.objects.get(id=pa)
                Profile.Mn = phone
                Profile.save()
                success = "Your Phone number Change Successfully"
        elif Address:
            Address = Address.capitalize()
            Profile = Patient.objects.get(id=pa)
            Profile.Address = Address
            Profile.save()
            success = "Your Address Change Successfully"

    patient = Patient.objects.filter(id=pa)
    Data = {'patient': patient, 'Customer': Customer,
            'labcity': labcity, 'error': error_message,
            'success': success}
    return render(request, "Patient_Setting.html", Data)


# ##################################################### Forget Password Email Sent ##############################

def ChangePassword(request, token):
    context = {}

    try:
        profile_obj = Patient.objects.get(forget_password_token=token)
        la = profile_obj.id
        context = {'user_id': la}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = la

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')

            if new_password != confirm_password:
                # messages.success(request, 'both should  be equal.')
                success = "both should  be equal."
                return redirect(f'/change-password/{token}/')

            user_obj = Patient.objects.get(id=user_id)
            user_obj.password = make_password(new_password)
            user_obj.save()
            user_obj = Patient.objects.get(id=la)
            token = str(uuid.uuid4())
            profile_obj = Patient.objects.get(email=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            success_message = 'Your Password has been changed Now '
            return render(request, 'Login.html', {'success': success_message})
        else:
            return render(request, 'change-password.html')


    except Exception as e:
        print(e)
    return render(request, 'Link_experiy.html', context)


def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not Patient.objects.filter(email=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password/')

            user_obj = Patient.objects.get(email=username)
            token = str(uuid.uuid4())
            profile_obj = Patient.objects.get(email=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')



    except Exception as e:
        print(e)
    return render(request, 'forget-password.html')


# ##################################################### Forget Password Email Sent End  ##############################


# def page_not_found_view(request):


# custom not found url page for improve security
def not_found(request, exception):
    labcity = Labcity.objects.all()
    Customer = Patient.objects.all()
    Data = {'labcity': labcity}
    return render(request, "page_not_found.html", Data)
