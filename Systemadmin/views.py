import uuid
from datetime import *

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.utils.timezone import now

from Systemadmin.Middleware.Admin_auth import Admin_middleware, Admin_login_check
from Laboratory.models.Book_lab_test import Book_Test
from Laboratory.models.Lab_tests_list import Test_list
from Laboratory.models.Labcity import Labcity
from Laboratory.models.Samplest import Samplest
from Laboratory.models.add_lab import Lab
from Doctor.models.Doctor_Request import Doctor_request
from Doctor.models.ADD_Docror import Doctors
from mainpage.Sent_Email import send_forget_password_mail_Admin, Doctor_Request_Accepted_Sent_mail_doctor, \
    Doctor_Request_Rejected_Sent_mail_doctor, Pharmacy_Create_FirstPassword_Sent_mail_doctor
from mainpage.models.Patient import Patient
from Systemadmin.models.Super_Admin import SuperAdmin
from Doctor.models.All_Specialist import Special
from Pharmacy_Store.models.Add_pharmacy import Pharmacy
from Doctor.models.ADD_Docror import Doctors


@Admin_middleware
def Super_admin(request):
    all_pat = Patient.objects.all().count()
    Total_labs = Lab.objects.all().count()
    Doctors_count = Doctors.objects.all().count()
    Doctors_request_count = Doctor_request.objects.all().count()
    Pharmacy_count = Pharmacy.objects.all().count()
    current_lab = SuperAdmin.objects.get()
    Doctor = Doctors.objects.all().order_by('-id')

    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)

    data = {'all_pat': all_pat, 'Total_labs': Total_labs,
            'current_lab': current_lab, 'current_admin': current_admin,
            'Doctors_count': Doctors_count, "Pharmacy_count": Pharmacy_count,
            'Doctors_request_count': Doctors_request_count, 'Doctor': Doctor}
    return render(request, "admin_dashboard.html", data)


@Admin_login_check
def SuperAdmin_Login(request):
    if request.method == 'GET':
        return render(request, 'admin_login.html')
    else:
        Data = request.POST
        email = Data.get('email')
        password = Data.get('password')

        # # Validations
        Admin = SuperAdmin.objects.filter(email=email, password=password)
        error_message = None
        #
        if Admin:
            for i in Admin:
                request.session['admin_id'] = i.id
                request.session['admin_email'] = i.email
                return redirect(Super_admin)
        else:
            error_message = "Email or Password Invalid......"

        # return render(request, 'Login.html', {'error': error_message})
    return render(request, 'admin_login.html', {'error': error_message})


@Admin_middleware
def Admin_profile(request):
    lb = request.session.get('admin_id')
    error_message = None
    success = None

    flag = False
    Admin_profile = SuperAdmin.objects.filter(id=lb)
    labcity = Labcity.objects.all()
    current_lab = SuperAdmin.objects.get(id=lb)

    if request.method == 'POST':
        data = request.POST
        Current_password = data.get('C_pass')
        New_password = data.get('New_password')
        Confirm_password = data.get('NConform_pass')
        for i in Admin_profile:
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
            Cus = SuperAdmin.objects.get(id=lb)
            Cus.password = New_password
            Cus.save()
            success = "Your Password Updated Successfully"

        else:
            error_message = "Please Check Your Current Password You Enter"

    Data = {'Admin_profile': Admin_profile, 'labcity': labcity,
            'error': error_message, 'current_lab': current_lab,
            'success': success}
    return render(request, "Laboratory_fuctions/Admin_profile.html", Data)


@Admin_middleware
def Admin_profile_img(request):
    lb = request.session.get('admin_id')
    error_message = None
    success = None

    flag = False
    Admin_profile = SuperAdmin.objects.filter(id=lb)
    labcity = Labcity.objects.all()
    current_lab = SuperAdmin.objects.get(id=lb)

    Admin_img = SuperAdmin.objects.get(id=lb)
    if request.method == 'POST':
        profile_img = request.FILES.get('image')
        Admin_img.img = profile_img
        Admin_img.save()
        success = "Your Profile image Change Successfully"
    else:
        error_message = "Your Profile image Change failed!"

    Data = {'Admin_profile': Admin_profile, 'labcity': labcity,
            'error': error_message, 'current_lab': current_lab,
            'success': success}
    return render(request, "Laboratory_fuctions/Admin_profile.html", Data)


@Admin_middleware
def updates_admin_profile(request):
    lb = request.session.get('admin_id')
    error_message = None
    success = None

    Admin_profile = SuperAdmin.objects.filter(id=lb)
    labcity = Labcity.objects.all()
    current_lab = SuperAdmin.objects.get(id=lb)

    if request.method == 'POST':
        data = request.POST
        name = data.get("username")
        phone = data.get("phone")
        Address = data.get("Address")
        if name:
            name = name.capitalize()
            Profile = SuperAdmin.objects.get(id=lb)
            Profile.Username = name
            Profile.save()
            success = "Your Username Change Successfully"
        elif phone:
            if len(phone) < 10:
                error_message = " Password must be At-least 10 digit long without first '0' "
            else:
                Profile = SuperAdmin.objects.get(id=lb)
                Profile.Callnumber = phone
                Profile.save()
                success = "Your Phone number Change Successfully"
        elif Address:
            Address = Address.capitalize()
            Profile = SuperAdmin.objects.get(id=lb)
            Profile.Address = Address
            Profile.save()
            success = "Your Address Change Successfully"

    Data = {'Admin_profile': Admin_profile, 'labcity': labcity,
            'error': error_message, 'current_lab': current_lab,
            'success': success}
    return render(request, "Laboratory_fuctions/Admin_profile.html", Data)


# /////////////////////////Functions Related Patients Add_New/Edit/Delete/active/deactivate Start/////////////////////////

@Admin_middleware
def add_new_Patient(request):
    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    all_city = Labcity.objects.all()
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)

    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        email = Data.get('email')
        Callnumber = Data.get('phone')
        password = Data.get('password')
        City = Data.get('City')

        Is_Exit = Patient.objects.filter(email=email)
        if Is_Exit:
            error_message = " This CNIC is already exit"
            Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
                    "all_city": all_city, "current_admin": current_admin}
            return render(request, "Admin_site/add_new_Samplest.html", Data)
        elif len(Callnumber) < 10:
            error_message = " This Phone number must be 10 digits"
            Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
                    "all_city": all_city, "current_admin": current_admin}
            return render(request, "Admin_site/add_new_Samplest.html", Data)

        Add_new_Patient = Patient(name=name, email=email, Mn=Callnumber, password=password, is_Active=True)
        Add_new_Patient.password = make_password(Add_new_Patient.password)
        Add_new_Patient.save()
        success = "New Patient/User is Added Sucessfully"
    Data = {"current_lab": current_lab, 'error_message': error_message,
            'success': success, "all_city": all_city, "current_admin": current_admin}
    return render(request, "Add_New_Patient.html", Data)


@Admin_middleware
def view_Patient_list(request):
    current_lab = SuperAdmin.objects.get()
    all_Patients = Patient.objects.all().order_by('-id')
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)
    Data = {"current_lab": current_lab, 'all_Patients': all_Patients, "current_admin": current_admin}
    return render(request, "View_all_patients.html", Data)


@Admin_middleware
def Status_Patients(request):
    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    all_Patients = Patient.objects.all().order_by('-id')
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)

    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        id = Data.get('id')
        Update_Patient = Patient.objects.filter(id=id)
        Update_Patient = Patient.objects.get(id=id)

        if Update_Patient.is_Active:
            Update_Patient.is_Active = False
            success = name + "is Deactivate Successfully"
        else:
            Update_Patient.is_Active = True
            success = name + "is Active Successfully"
        Update_Patient.save()

    Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
            'all_Patients': all_Patients, "current_admin": current_admin}
    return render(request, "View_all_patients.html", Data)


@Admin_middleware
def Patients_del(request):
    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    all_Patients = Patient.objects.all().order_by('-id')
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)

    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        id = Data.get('id')
        d_Patient = Patient.objects.filter(id=id)

        if d_Patient:
            d_Patient = Patient.objects.get(id=id)
            d_Patient.delete()
            success = name + "Deleted Successfully"
        else:
            error_message = name + " Not Exist or already deleted from System"

    Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
            'all_Patients': all_Patients, "current_admin": current_admin}
    return render(request, "View_all_patients.html", Data)


# /////////////////////////Functions Related Patient Add_New/Edit/Delete/active/deactivate END/////////////////////////

# /////////////////////////Functions Related Doctor Add_New/Edit/Delete/active/deactivate Start/////////////////////////

@Admin_middleware
def view_N_D(request):
    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)
    all_new_doctor_request = Doctor_request.objects.filter(is_Accepted=False).order_by('-id')

    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        email = Data.get('email')
        Dname = Data.get('Dname')
        id = Data.get('id')
        # Update_Patient = Lab.objects.filter(id=id)
        Update = Doctor_request.objects.get(id=id)
        if name == 'cancel':
            Update.Status = 'Rejected'
            Update.save()
            # success = Update.Doctor_name + 'is now part of over doctor Team'
            success = Update.Doctor_name + ' Request is  rejected successfully'
            Doctor_Request_Rejected_Sent_mail_doctor(email, Dname)
        else:
            add = Doctor_request.objects.filter(id=id)
            for i in add:
                Doctor_name = i.Doctor_name
                email = i.email
                Callnumber = i.Callnumber
                Speciality = i.Speciality
                city = i.city
                Gender = i.Gender
                Doctor_PMID_number = i.Doctor_PMID_number

            Update.Status = 'Accepted'
            Update.is_Accepted = True
            token = str(uuid.uuid4())
            add = Doctors.objects.filter(email=email)
            if not add:
                add_new_doctor = Doctors(Doctor_name=Doctor_name, email=email,
                                         Callnumber=Callnumber, Speciality=Speciality,
                                         Doctor_PMID_number=Doctor_PMID_number, city=city,
                                         forget_password_token=token, Gender=Gender)
                add_new_doctor.save()
            All_Speciality_count = Special.objects.filter(Doctor_Speciality=Speciality)
            if All_Speciality_count:
                All_Speciality_count = Special.objects.filter(Doctor_Speciality=Speciality).count()
                update_spec = Special.objects.get(Doctor_Speciality=Speciality)
                update_spec.total_doctors = All_Speciality_count
            else:
                update_spec = Special.objects.get(Doctor_Speciality=Speciality)
                update_spec.total_doctors = 1
            Update.save()
            update_spec.save()
            Doctor_Request_Accepted_Sent_mail_doctor(email, Dname, token)

            success = Update.Doctor_name + 'is now part of over doctor Team'

    data = {'error_message': error_message, 'success': success,
            'all_new_doctor_request': all_new_doctor_request,
            "current_lab": current_lab, 'current_admin': current_admin}
    return render(request, 'Doctors_functions/view_new_doctor_requests.html', data)


@Admin_middleware
def all_Register_doctor(request):
    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)
    all_Register_doctor = Doctors.objects.all().order_by('-id')

    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        id = Data.get('id')
        # Update_Patient = Lab.objects.filter(id=id)
        Delete = Doctors.objects.get(id=id)
        if name == 'del':
            Delete.delete()
            # success = Update.Doctor_name + 'is now part of over doctor Team'
            success = Delete.Doctor_name + ' Deleted successfully'

    data = {'error_message': error_message, 'success': success,
            'all_Register_doctor': all_Register_doctor,
            "current_lab": current_lab, 'current_admin': current_admin}
    return render(request, 'Doctors_functions/view_register_docters.html', data)


@Admin_middleware
def Status_doctor(request):
    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)
    all_Register_doctor = Doctors.objects.all().order_by('-id')

    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        id = Data.get('id')
        Update_Patient = Doctors.objects.filter(id=id)
        Update_Doctor = Doctors.objects.get(id=id)

        if Update_Doctor.is_Active:
            Update_Doctor.is_Active = False
            success = name + "is Deactivate Successfully"
        else:
            Update_Doctor.is_Active = True
            success = name + "is Active Successfully"
        Update_Doctor.save()

    data = {'error_message': error_message, 'success': success,
            'all_Register_doctor': all_Register_doctor,
            "current_lab": current_lab, 'current_admin': current_admin}

    return render(request, 'Doctors_functions/view_register_docters.html', data)


@Admin_middleware
def Add_new_Doctor(request):
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)
    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    all_city = Labcity.objects.all()
    All_Speciality = Special.objects.all().order_by('Doctor_Speciality')
    if request.method == 'POST':
        Data = request.POST
        Doctor_name = Data.get('name')
        email = Data.get('email')
        Callnumber = Data.get('phone')
        Speciality = Data.get('Speciality')
        city = Data.get('city')
        Doctor_PMID_number = Data.get('PMID_number')
        Address = Data.get('Address')
        Gender = Data.get('gender')

        Is_Exit = Doctors.objects.filter(email=email)
        Is_PMID_number_Exit = Doctors.objects.filter(Doctor_PMID_number=Doctor_PMID_number)

        if Is_PMID_number_Exit:
            error_message = " Doctor With This PMID Number is already exit"
            Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
                    "all_city": all_city, "current_admin": current_admin, 'All_Speciality': All_Speciality}
            return render(request, "Doctors_functions/Add_new_doctor.html", Data)
        if Is_Exit:
            error_message = " This E-mail Address is already exit"
            Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
                    "all_city": all_city, "current_admin": current_admin, 'All_Speciality': All_Speciality}
            return render(request, "Doctors_functions/Add_new_doctor.html", Data)
        elif len(Callnumber) < 10:
            error_message = " This Phone number must be 10 digits"
            Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
                    "all_city": all_city, "current_admin": current_admin, 'All_Speciality': All_Speciality}
            return render(request, "Doctors_functions/Add_new_doctor.html", Data)
        token = str(uuid.uuid4())
        Add_new_Labs = Doctors(Doctor_name=Doctor_name, email=email,
                               Callnumber=Callnumber, Gender=Gender,
                               Speciality=Speciality, city=city,
                               Doctor_PMID_number=Doctor_PMID_number,
                               forget_password_token=token)

        # Add_new_Patient.password = make_password(Add_new_Patient.password)
        Add_new_Labs.save()
        All_Speciality_count = Special.objects.filter(Doctor_Speciality=Speciality).count()
        update_spec = Special.objects.get(Doctor_Speciality=Speciality)
        update_spec.total_doctors = All_Speciality_count
        update_spec.save()

        success = Doctor_name + 'is now part of over doctor Team'
        Doctor_Request_Accepted_Sent_mail_doctor(email, Doctor_name, token)

    Data = {"current_lab": current_lab, 'error_message': error_message,
            'success': success, "all_city": all_city,
            "current_admin": current_admin, 'All_Speciality': All_Speciality}
    return render(request, "Doctors_functions/Add_new_doctor.html", Data)


# /////////////////////////Functions Related Doctor Add_New/Edit/Delete/active/deactivate End/////////////////////////

# /////////////////////////Functions Related Laboratory Add_New/Edit/Delete/active/deactivate Start/////////////////////////

@Admin_middleware
def add_new_Laboratory(request):
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)
    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    all_city = Labcity.objects.all()

    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        email = Data.get('email')
        Callnumber = Data.get('phone')
        password = Data.get('password')
        City = Data.get('City')
        Address = Data.get('Address')
        city = Labcity.objects.get(Lab_city_name=City)

        Is_Exit = Lab.objects.filter(email=email)
        if Is_Exit:
            error_message = " This E-mail Address is already exit"
            Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
                    "all_city": all_city, "current_admin": current_admin}
            return render(request, "Laboratory_fuctions/add_new_Laboratory.html", Data)
        elif len(Callnumber) < 10:
            error_message = " This Phone number must be 10 digits"
            Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
                    "all_city": all_city, "current_admin": current_admin}
            return render(request, "Laboratory_fuctions/add_new_Laboratory.html", Data)

        Add_new_Labs = Lab(Labname=name, email=email, Callnumber=Callnumber, city=city, password=password,
                           Address=Address,
                           is_Active=True)
        # Add_new_Patient.password = make_password(Add_new_Patient.password)
        Add_new_Labs.save()
        success = "New Laboratory is Added Sucessfully"
    Data = {"current_lab": current_lab, 'error_message': error_message,
            'success': success, "all_city": all_city, "current_admin": current_admin}
    return render(request, "Laboratory_fuctions/add_new_Laboratory.html", Data)


@Admin_middleware
def view_Labs_list(request):
    current_lab = SuperAdmin.objects.get()
    all_Labs = Lab.objects.all().order_by('-id')
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)

    Data = {"current_lab": current_lab, 'all_Labs': all_Labs, "current_admin": current_admin}
    return render(request, "Laboratory_fuctions/View_all_laboratories.html", Data)


@Admin_middleware
def Status_Labs(request):
    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    all_Labs = Lab.objects.all().order_by('-id')
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)

    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        id = Data.get('id')
        # Update_Patient = Lab.objects.filter(id=id)
        Update_Labs = Lab.objects.get(id=id)

        if Update_Labs.is_Active:
            Update_Labs.is_Active = False
            success = name + "is Deactivate Successfully"
        else:
            Update_Labs.is_Active = True
            success = name + "is Active Successfully"
        Update_Labs.save()

    Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
            'all_Labs': all_Labs, "current_admin": current_admin}
    return render(request, "Laboratory_fuctions/View_all_laboratories.html", Data)

    # return redirect(lab_admin)


@Admin_middleware
def Laboratory_del(request):
    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    all_Labs = Lab.objects.all().order_by('-id')
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)

    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        id = Data.get('id')
        d_Lab = Lab.objects.filter(id=id)

        if d_Lab:
            d_Lab = Lab.objects.get(id=id)
            d_Lab.delete()
            success = name + "Deleted Successfully"
        else:
            error_message = name + " is Not Exist or already deleted from System"

    Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
            'all_Labs': all_Labs, "current_admin": current_admin}
    return render(request, "Laboratory_fuctions/View_all_laboratories.html", Data)


def update_Laboratory(request, id):
    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    all_Labs = Lab.objects.all().order_by('-id')
    all_city = Labcity.objects.all()
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)

    Update_Laboratory = Lab.objects.filter(id=id)
    # print(Update_Samplest)
    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        Email = Data.get('email')
        Callnumber = Data.get('phone')
        City = Data.get('City')
        Address = Data.get('Address')
        Id = Data.get('id')
        ci = Labcity.objects.filter(Lab_city_name__startswith=City)
        if ci:
            ci = Labcity.objects.get(Lab_city_name__startswith=City)
            Update_Laboratory = Lab.objects.get(id=id)
            Update_Laboratory.city = ci
        else:
            error_message = City + ' is not valid, Please Enter/Select Valid Option '
            Data = {"current_lab": current_lab, 'Update_Laboratory': Update_Laboratory,
                    'all_city': all_city, "error_message": error_message, "current_admin": current_admin}
            return render(request, "Laboratory_fuctions/Update_laboratory_record.html", Data)

        # img = request.FILES.get('image')
        # if img:
        #     Update_Laboratory.img = img

        print(name, Callnumber)
        Update_Laboratory.name = name
        Update_Laboratory.Callnumber = Callnumber
        Update_Laboratory.email = Email
        Update_Laboratory.Address = Address
        Update_Laboratory.save()

        success = name + "Record is Updated Successfully"
        Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
                'all_Labs': all_Labs, "current_admin": current_admin}
        return render(request, "Laboratory_fuctions/View_all_laboratories.html", Data)

    Data = {"current_lab": current_lab, 'Update_Laboratory': Update_Laboratory, 'all_city': all_city,
            "current_admin": current_admin}
    return render(request, "Laboratory_fuctions/Update_laboratory_record.html", Data)


# /////////////////////////Functions Related Laboratory Add_New/Edit/Delete/active/deactivate END/////////////////////////

# /////////////////////////Functions Related Pharmacy Add_New/Edit/Delete/active/deactivate Start/////////////////////////

@Admin_middleware
def ADD_New_Pharmacy(request):
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)

    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    all_city = Labcity.objects.all()
    if request.method == 'POST':
        Data = request.POST
        Pharmacy_name = Data.get('name')
        email = Data.get('email')
        Callnumber = Data.get('phone')
        City = Data.get('city')
        Pharmacy_Address = Data.get('Pharmacy_Address')
        Notes = Data.get('Address')

        Is_Exit = Pharmacy.objects.filter(email=email)
        Is_Phone_number_Exit = Pharmacy.objects.filter(Callnumber=Callnumber)

        if Is_Phone_number_Exit:
            error_message = " Pharmacy With This Phone Number is already exit"
            Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
                    "all_city": all_city, "current_admin": current_admin,
                    "Pharmacy_name": Pharmacy_name, "email": email, "Pharmacy_Address": Pharmacy_Address,
                    "Notes": Notes, "City": City}
            return render(request, "Pharmacy_fuctions/Add_New_Pharmacy.html", Data)
        if Is_Exit:
            error_message = " This E-mail Address is already exit"
            Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
                    "all_city": all_city, "current_admin": current_admin,
                    "Pharmacy_name": Pharmacy_name, "Pharmacy_Address": Pharmacy_Address,
                    "Notes": Notes, "City": City, "Callnumber": Callnumber
                    }
            return render(request, "Pharmacy_fuctions/Add_New_Pharmacy.html", Data)
        elif len(Callnumber) < 10:
            error_message = " This Phone number must be 10 digits"
            Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
                    "all_city": all_city, "current_admin": current_admin,
                    "Pharmacy_name": Pharmacy_name, "Pharmacy_Address": Pharmacy_Address,
                    "Notes": Notes, "City": City, "Callnumber": Callnumber, "email": email
                    }
            return render(request, "Pharmacy_fuctions/Add_New_Pharmacy.html", Data)
        token = str(uuid.uuid4())
        Add_new_pharmacy = Pharmacy(Pharmacy_name=Pharmacy_name, email=email,
                                    Callnumber=Callnumber, city=City,
                                    Address=Pharmacy_Address,
                                    forget_password_token=token)

        # Add_new_Patient.password = make_password(Add_new_Patient.password)
        Add_new_pharmacy.save()
        # All_Speciality_count = Special.objects.filter(Doctor_Speciality=Speciality).count()
        # update_spec = Special.objects.get(Doctor_Speciality=Speciality)
        # update_spec.total_doctors = All_Speciality_count
        # update_spec.save()

        success = Pharmacy_name + 'is now part of over Pharmacy Team'
        Pharmacy_Create_FirstPassword_Sent_mail_doctor(email, Pharmacy_name, token)

    Data = {"current_lab": current_lab, 'error_message': error_message,
            'success': success, "all_city": all_city,
            "current_admin": current_admin}
    return render(request, "Pharmacy_fuctions/Add_New_Pharmacy.html", Data)


@Admin_middleware
def view_Pharmacy_list(request):
    current_lab = SuperAdmin.objects.get()
    all_Pharmacy = Pharmacy.objects.all().order_by('-id')
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)

    Data = {"current_lab": current_lab, 'all_Pharmacy': all_Pharmacy, "current_admin": current_admin}
    return render(request, "Pharmacy_fuctions/view_all_Pharmacy.html", Data)


@Admin_middleware
def Status_Pharmacy(request):
    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    all_Pharmacy = Pharmacy.objects.all().order_by('-id')
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)

    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        id = Data.get('id')
        # Update_Patient = Lab.objects.filter(id=id)
        Update_Labs = Pharmacy.objects.get(id=id)

        if Update_Labs.is_Active:
            Update_Labs.is_Active = False
            success = name + "is Deactivate Successfully"
        else:
            Update_Labs.is_Active = True
            success = name + "is Active Successfully"
        Update_Labs.save()

    Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
            'all_Pharmacy': all_Pharmacy, "current_admin": current_admin}
    return render(request, "Pharmacy_fuctions/view_all_Pharmacy.html", Data)

    # return redirect(lab_admin)


@Admin_middleware
def Pharmacy_del(request):
    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    all_Pharmacy = Pharmacy.objects.all().order_by('-id')
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)

    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        id = Data.get('id')
        d_Phy = Pharmacy.objects.filter(id=id)

        if d_Phy:
            d_Phy = Pharmacy.objects.get(id=id)
            d_Phy.delete()
            messages.error(request, name + "Deleted Successfully")
            return redirect(Pharmacy_del)
        else:
            error_message = name + " is Not Exist or already deleted from System"

    Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
            'all_Pharmacy': all_Pharmacy, "current_admin": current_admin}
    return render(request, "Pharmacy_fuctions/view_all_Pharmacy.html", Data)


def Update_Pharmacy(request, id):
    error_message = None
    success = None
    current_lab = SuperAdmin.objects.get()
    all_Pharmacy = Pharmacy.objects.all().order_by('-id')
    all_city = Labcity.objects.all()
    lb = request.session.get('admin_id')
    current_admin = SuperAdmin.objects.filter(id=lb)

    Current_Pharmacy = Pharmacy.objects.get(id=id)
    if request.method == 'POST':
        Data = request.POST
        name = Data.get('name')
        Callnumber = Data.get('phone')
        City = Data.get('city')
        Pharmacy_Address = Data.get('Pharmacy_Address')
        Note = Data.get('Note')

        # ci = Labcity.objects.filter(Lab_city_name__startswith=City)
        ci = Labcity.objects.filter(Lab_city_name=City)
        if ci:
            ci = Labcity.objects.get(Lab_city_name__startswith=City)
            Update_Phy = Pharmacy.objects.get(id=id)
            Update_Phy.city = ci
        else:
            messages.error(request, City + ' is not valid, Please Enter/Select Valid Option ')
            return redirect(Update_Pharmacy, id)

        if len(Callnumber) < 10:
            error_message = " This Phone number must be 10 digits"
            Data = {"current_lab": current_lab, 'Current_Pharmacy': Current_Pharmacy,
                    'all_city': all_city, "error_message": error_message, "current_admin": current_admin}
            return render(request, "Pharmacy_fuctions/Update_Pharmacy_record.html", Data)

        # img = request.FILES.get('image')
        # if img:
        #     Update_Laboratory.img = img
        city = Labcity.objects.get(Lab_city_name=City)
        Update_Phy.Pharmacy_name = name
        Update_Phy.Callnumber = Callnumber
        Update_Phy.Address = Pharmacy_Address
        Update_Phy.Note = Note
        Update_Phy.city = city
        Update_Phy.save()

        success = name + "Record is Updated Successfully"
        Data = {"current_lab": current_lab, 'error_message': error_message, 'success': success,
                'all_Pharmacy': all_Pharmacy, "current_admin": current_admin}
        return render(request, "Pharmacy_fuctions/view_all_Pharmacy.html", Data)

    Data = {"current_lab": current_lab, 'Current_Pharmacy': Current_Pharmacy, 'all_city': all_city,
            "current_admin": current_admin}
    return render(request, "Pharmacy_fuctions/Update_Pharmacy_record.html", Data)


# /////////////////////////Functions Related Pharmacy Add_New/Edit/Delete/active/deactivate End/////////////////////////

# ///////////////////////////////////////Forget Password Email Sent ////////////////////////////////////////////////////

def ChangePassword_Admin(request, token):
    context = {}

    try:
        profile_obj = SuperAdmin.objects.get(forget_password_token=token)
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

                return redirect(f'/change-password_Admin/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password_Admin/{token}/')

            user_obj = SuperAdmin.objects.get(id=user_id)
            user_obj.password = new_password
            user_obj.save()
            user_obj = Lab.objects.get(id=la)
            token = str(uuid.uuid4())
            profile_obj = Lab.objects.get(email=user_obj.email)
            profile_obj.forget_password_token = token
            profile_obj.save()
            success_message = 'Your Password has been changed Now '
            return render(request, 'admin_login.html', {'success': success_message})
        else:
            return render(request, 'change-password.html')


    except Exception as e:
        print(e)
    return render(request, 'Link_experiy.html', context)


def ForgetPassword_Admin(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            print(username)

            if not SuperAdmin.objects.filter(email=username).first():
                messages.error(request, 'Not user found with this Email.')
                return redirect('/ForgetPassword_Admin/')

            user_obj = SuperAdmin.objects.get(email=username)
            token = str(uuid.uuid4())
            print(token)
            profile_obj = SuperAdmin.objects.get(email=username)
            print(profile_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail_Admin(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('/ForgetPassword_Admin/')

    except Exception as e:
        print(e)
    return render(request, 'forget-password.html')

# ///////////////////////////////////// Forget Password Email Sent End  ////////////////////////////////////////////////
