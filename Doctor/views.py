from time import strptime

from django.shortcuts import render, redirect

import datetime
import uuid
from datetime import *
import time
from django.contrib import messages

from Doctor.models.save_reports import Save_Medical_Reports
from Laboratory.models.Labcity import Labcity
from Laboratory.models.Samplest import Samplest
from Laboratory.models.add_lab import Lab

from mainpage.Sent_Email import send_forget_password_mail_doctor, Doctor_Request_Sent_mail_doctor
from mainpage.models.Patient import Patient
from django.core.paginator import Paginator

from Doctor.models.ADD_Docror import Doctors
from Doctor.models.Doctor_Request import Doctor_request
from Doctor.models.Clinic import Clinic
from Doctor.models.All_Specialist import Special
from Doctor.models.Health_blog import Health_blogs
from Doctor.models.appointments import Appointment
from Doctor.models.save_reports import Save_Medical_Reports
from Doctor.Middleware.Doctor_auth import Doctor_middleware, Doctor_login_check


# Create your views here.



def Doctor_request_form(request):
    error_message = None
    success_message = None

    all_sp = Special.objects.all()
    labcitys = Labcity.objects.all()

    if request.method == 'POST':

        Data = request.POST
        email = Data.get('email')
        name = Data.get('name')
        phone_number = Data.get('phone_number')
        city = Data.get('city')
        PMID_number = Data.get('PMID_number')
        Speciality = Data.get('Speciality')
        Gender = Data.get('gender')

        Doctor = Doctor_request.objects.filter(email=email)

        if Doctor:
            error_message = "E-mail is already exited"
            data = {'error': error_message, 'success': success_message,
                    'labcitys': labcitys, 'all_sp': all_sp}
            return render(request, 'Doctor_request_form.html', data)
        Doctor = Doctor_request.objects.filter(Doctor_PMID_number=PMID_number)
        if Doctor:
            error_message = "Request with tis PMID Number is already exited, You cannot send multiple " \
                            "requests with one PMID Number "
            data = {'error': error_message, 'success': success_message,
                    'labcitys': labcitys, 'all_sp': all_sp}
            return render(request, 'Doctor_request_form.html', data)
        Doctor_requests = Doctor_request(Doctor_name=name, email=email,
                                         Callnumber=phone_number, city=city,
                                         Gender=Gender, Speciality=Speciality,
                                         Doctor_PMID_number=PMID_number)

        Doctor_requests.save()
        success_message = 'Request is sent successfully. \n You will be informed about request is accept or not through E-mail'
        Doctor_Request_Sent_mail_doctor(email, name)
        data = {'error': error_message, 'success': success_message,
                'labcitys': labcitys, 'all_sp': all_sp}
        return render(request, 'Doctor_request_form.html', data)

    data = {'error': error_message, 'success': success_message,
            'labcitys': labcitys, 'all_sp': all_sp}
    return render(request, 'Doctor_request_form.html', data)


def Create_password_doctor(request, token):
    context = {}

    try:
        profile_obj = Doctors.objects.get(forget_password_token=token)
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

                return redirect(f'/Create_password_doctor/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/Create_password_doctor/{token}/')

            user_obj = Doctors.objects.get(id=user_id)
            user_obj.password = new_password
            user_obj.save()
            user_obj = Doctors.objects.get(id=la)
            token = str(uuid.uuid4())
            profile_obj = Doctors.objects.get(email=user_obj.email)
            profile_obj.forget_password_token = token
            profile_obj.save()
            success_message = 'Your Password has been Created Successfully now please Login '
            return render(request, 'doctor_login.html', {'success': success_message})
        else:
            return render(request, 'change-password.html')


    except Exception as e:
        print(e)
    return render(request, 'Link_experiy.html', context)


def view_all_doctors(request):
    min_rate = None
    max_rate = None
    ci = None
    S_N = None
    labcitys = Labcity.objects.all()
    All_Speciality = Special.objects.all().order_by('Doctor_Speciality')
    doctor_clinic = Clinic.objects.all()
    labcity = Labcity.objects.all()

    Doctor_list = Doctors.objects.filter(is_Active=True)
    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
    page_number = request.GET.get('page')
    Doctor = paginator.get_page(page_number)

    All_Doctor = Doctors.objects.filter(is_Active=True)
    Doctor_experience = Doctors.objects.filter(is_Active=True).order_by('-Experience')
    F_l_to_H = Doctors.objects.filter(is_Active=True).order_by('Doctor_Clinic__Doctor_Fee')
    F_H_to_l = Doctors.objects.filter(is_Active=True).order_by('-Doctor_Clinic__Doctor_Fee')

    # Data = {'labcity': labcity}
    Customer = Patient.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        Specialist = request.POST.get('Specialist')
        city = request.POST.get('city')
        Range = request.POST.get('Range')
        S_N = Specialist

        if S_N == 'all':
            S_N = None
        # print('Filters = ', Specialist, city, Range)
        if city:
            if city == 'all':
                ci = None
            else:
                ci = Labcity.objects.filter(Lab_city_name__startswith=city)
        else:
            ci = None

        if name == 'filter':
            if city == 'all':
                if Specialist == 'all':
                    if Range == 'all':
                        Doctor_list = Doctors.objects.filter(is_Active=True)
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)

                    elif Range == '0-100':
                        Doctor_list = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(0, 100))
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)
                        Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(0, 100),
                                                                   is_Active=True).order_by('-Experience')
                    elif Range == '100-500':
                        Doctor_list = Doctors.objects.filter(is_Active=True,
                                                             Doctor_Clinic__Doctor_Fee__range=(100, 500))
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)

                        Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(100, 500),
                                                                   is_Active=True).order_by('-Experience')
                    elif Range == '500-1000':
                        Doctor_list = Doctors.objects.filter(is_Active=True,
                                                             Doctor_Clinic__Doctor_Fee__range=(500, 1000))
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)

                        Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(500, 1000),
                                                                   is_Active=True).order_by('-Experience')
                    elif Range == '1000-2000':
                        Doctor = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(1000, 2000))
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)

                        Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(1000, 2000),
                                                                   is_Active=True).order_by('-Experience')
                    elif Range == '2000-3000':
                        Doctor_list = Doctors.objects.filter(is_Active=True,
                                                             Doctor_Clinic__Doctor_Fee__range=(2000, 1000))
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)

                        Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(2000, 1000),
                                                                   is_Active=True).order_by('-Experience')
                    elif Range == '3000-5000':
                        Doctor_list = Doctors.objects.filter(is_Active=True,
                                                             Doctor_Clinic__Doctor_Fee__range=(3000, 5000))
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)

                        Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(3000, 5000),
                                                                   is_Active=True).order_by('-Experience')
                elif Specialist != 'all':
                    if Range == 'all':
                        Doctor_list = Doctors.objects.filter(is_Active=True, Speciality=Specialist)
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)

                    elif Range == '0-100':
                        Doctor_list = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(0, 100),
                                                             Speciality=Specialist)
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)

                        Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(0, 100),
                                                                   Speciality=Specialist,
                                                                   is_Active=True).order_by('-Experience')
                    elif Range == '100-500':
                        Doctor_list = Doctors.objects.filter(is_Active=True,
                                                             Doctor_Clinic__Doctor_Fee__range=(100, 500),
                                                             Speciality=Specialist)
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)

                        Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(100, 500),
                                                                   Speciality=Specialist,
                                                                   is_Active=True).order_by('-Experience')
                    elif Range == '500-1000':
                        Doctor_list = Doctors.objects.filter(is_Active=True,
                                                             Doctor_Clinic__Doctor_Fee__range=(500, 1000),
                                                             Speciality=Specialist)
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)
                        Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(500, 1000),
                                                                   Speciality=Specialist,
                                                                   is_Active=True).order_by('-Experience')
                    elif Range == '1000-2000':
                        Doctor_list = Doctors.objects.filter(is_Active=True,
                                                             Doctor_Clinic__Doctor_Fee__range=(1000, 2000),
                                                             Speciality=Specialist)
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)
                        Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(1000, 2000),
                                                                   Speciality=Specialist,
                                                                   is_Active=True).order_by('-Experience')
                    elif Range == '2000-3000':
                        Doctor_list = Doctors.objects.filter(is_Active=True,
                                                             Doctor_Clinic__Doctor_Fee__range=(2000, 1000),
                                                             Speciality=Specialist)
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)
                        Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(2000, 1000),
                                                                   Speciality=Specialist,
                                                                   is_Active=True).order_by('-Experience')
                    elif Range == '3000-5000':
                        Doctor_list = Doctors.objects.filter(is_Active=True,
                                                             Doctor_Clinic__Doctor_Fee__range=(3000, 5000),
                                                             Speciality=Specialist)
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)
                        Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(3000, 5000),
                                                                   Speciality=Specialist,
                                                                   is_Active=True).order_by('-Experience')
                    else:
                        Doctor_list = Doctors.objects.filter(Speciality=Specialist, is_Active=True)
                        paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                        page_number = request.GET.get('page')
                        Doctor = paginator.get_page(page_number)
                        Doctor_experience = Doctors.objects.filter(Speciality=Specialist, is_Active=True).order_by(
                            '-Experience')

            elif Specialist == 'all':

                if Range == 'all':
                    Doctor_list = Doctors.objects.filter(city__startswith=city, is_Active=True)
                    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                    page_number = request.GET.get('page')
                    Doctor = paginator.get_page(page_number)
                    Doctor_experience = Doctors.objects.filter(city__startswith=city, is_Active=True).order_by(
                        '-Experience')
                elif Range == '0-100':
                    Doctor_list = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(0, 100),
                                                         city__startswith=city)
                    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                    page_number = request.GET.get('page')
                    Doctor = paginator.get_page(page_number)
                    Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(0, 100),
                                                               city__startswith=city,
                                                               is_Active=True).order_by('-Experience')
                elif Range == '100-500':
                    Doctor_list = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(100, 500),
                                                         city__startswith=city)
                    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                    page_number = request.GET.get('page')
                    Doctor = paginator.get_page(page_number)
                    Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(100, 500),
                                                               city__startswith=city,
                                                               is_Active=True).order_by('-Experience')
                elif Range == '500-1000':
                    Doctor_list = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(500, 1000),
                                                         city__startswith=city)
                    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                    page_number = request.GET.get('page')
                    Doctor = paginator.get_page(page_number)
                    Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(500, 1000),
                                                               city__startswith=city,
                                                               is_Active=True).order_by('-Experience')
                elif Range == '1000-2000':
                    Doctor_list = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(1000, 2000),
                                                         city__startswith=city)
                    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                    page_number = request.GET.get('page')
                    Doctor = paginator.get_page(page_number)
                    Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(1000, 2000),
                                                               city__startswith=city,
                                                               is_Active=True).order_by('-Experience')
                elif Range == '2000-3000':
                    Doctor_list = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(2000, 1000),
                                                         city__startswith=city)
                    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                    page_number = request.GET.get('page')
                    Doctor = paginator.get_page(page_number)
                    Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(2000, 1000),
                                                               city__startswith=city,
                                                               is_Active=True).order_by('-Experience')
                elif Range == '3000-5000':
                    Doctor_list = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(3000, 5000),
                                                         city__startswith=city)
                    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                    page_number = request.GET.get('page')
                    Doctor = paginator.get_page(page_number)
                    Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(3000, 5000),
                                                               city__startswith=city,
                                                               is_Active=True).order_by('-Experience')
            else:
                if Range == 'all':
                    Doctor_list = Doctors.objects.filter(city__startswith=city, Speciality=Specialist, is_Active=True)
                    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                    page_number = request.GET.get('page')
                    Doctor = paginator.get_page(page_number)
                    Doctor_experience = Doctors.objects.filter(city__startswith=city, Speciality=Specialist,
                                                               is_Active=True).order_by('-Experience')
                elif Range == '0-100':
                    Doctor_list = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(0, 100),
                                                         city__startswith=city, Speciality=Specialist, )
                    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                    page_number = request.GET.get('page')
                    Doctor = paginator.get_page(page_number)
                    Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(0, 100),
                                                               city__startswith=city, Speciality=Specialist,
                                                               is_Active=True).order_by('-Experience')
                elif Range == '100-500':
                    Doctor_list = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(100, 500),
                                                         city__startswith=city, Speciality=Specialist)
                    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                    page_number = request.GET.get('page')
                    Doctor = paginator.get_page(page_number)
                    Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(100, 500),
                                                               city__startswith=city, Speciality=Specialist,
                                                               is_Active=True).order_by('-Experience')
                elif Range == '500-1000':
                    Doctor_list = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(500, 1000),
                                                         city__startswith=city, Speciality=Specialist)
                    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                    page_number = request.GET.get('page')
                    Doctor = paginator.get_page(page_number)
                    Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(500, 1000),
                                                               city__startswith=city, Speciality=Specialist,
                                                               is_Active=True).order_by('-Experience')
                elif Range == '1000-2000':
                    Doctor_list = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(1000, 2000),
                                                         city__startswith=city, Speciality=Specialist)
                    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                    page_number = request.GET.get('page')
                    Doctor = paginator.get_page(page_number)
                    Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(1000, 2000),
                                                               is_Active=True).order_by('-Experience')
                elif Range == '2000-3000':
                    Doctor_list = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(2000, 1000),
                                                         city__startswith=city, Speciality=Specialist)
                    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                    page_number = request.GET.get('page')
                    Doctor = paginator.get_page(page_number)
                    Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(2000, 1000),
                                                               city__startswith=city, Speciality=Specialist,
                                                               is_Active=True).order_by('-Experience')
                elif Range == '3000-5000':
                    Doctor_list = Doctors.objects.filter(is_Active=True, Doctor_Clinic__Doctor_Fee__range=(3000, 5000),
                                                         city__startswith=city, Speciality=Specialist)
                    paginator = Paginator(Doctor_list, 5)  # Show 5 contacts per page.
                    page_number = request.GET.get('page')
                    Doctor = paginator.get_page(page_number)
                    Doctor_experience = Doctors.objects.filter(Doctor_Clinic__Doctor_Fee__range=(3000, 5000),
                                                               city__startswith=city, Speciality=Specialist,
                                                               is_Active=True).order_by('-Experience')

            Data = {'labcity': labcity, 'ci': ci, 'Customer': Customer,
                    'Doctor': Doctor, 'Doctor_experience': Doctor_experience,
                    'All_Doctor': All_Doctor, 'labcitys': labcitys,
                    'All_Speciality': All_Speciality, 'S_N': S_N,
                    'doctor_clinic': doctor_clinic, 'F_l_to_H': F_l_to_H,
                    'F_H_to_l': F_H_to_l
                    }
            return render(request, 'view_all_specialist.html', Data)
        elif name == 'search':
            ser = request.POST.get('search')
            Doctor = Doctors.objects.filter(Doctor_name__startswith=ser)
            Doctor_experience = Doctors.objects.filter(Doctor_name__startswith=ser).order_by('-Experience')
            if Doctor:
                Data = {'labcity': labcity, 'Customer': Customer,
                        'Doctor': Doctor, 'Doctor_experience': Doctor_experience,

                        'All_Doctor': All_Doctor, 'labcitys': labcitys,
                        'All_Speciality': All_Speciality, 'S_N': S_N,
                        'doctor_clinic': doctor_clinic, 'F_l_to_H': F_l_to_H,
                        'F_H_to_l': F_H_to_l
                        }
                return render(request, 'view_all_specialist.html', Data)
            Doctor = Doctors.objects.filter(Speciality__startswith=ser)
            Doctor_experience = Doctors.objects.filter(Speciality__startswith=ser).order_by('-Experience')
            if Doctor:
                Data = {'labcity': labcity, 'Customer': Customer,
                        'Doctor': Doctor, 'Doctor_experience': Doctor_experience,

                        'All_Doctor': All_Doctor, 'labcitys': labcitys,
                        'All_Speciality': All_Speciality, 'S_N': S_N,
                        'doctor_clinic': doctor_clinic, 'F_l_to_H': F_l_to_H
                        }
                return render(request, 'view_all_specialist.html', Data)

            Doctor = Doctors.objects.filter(city__startswith=ser)
            Doctor_experience = Doctors.objects.filter(city__startswith=ser).order_by('-Experience')
            ci = Labcity.objects.filter(Lab_city_name__startswith=ser)

            if Doctor:
                Data = {'labcity': labcity, 'ci': ci, 'Customer': Customer,
                        'Doctor': Doctor, 'Doctor_experience': Doctor_experience,

                        'All_Doctor': All_Doctor, 'labcitys': labcitys,
                        'All_Speciality': All_Speciality, 'S_N': S_N,
                        'doctor_clinic': doctor_clinic, 'F_l_to_H': F_l_to_H
                        }
                return render(request, 'view_all_specialist.html', Data)

    Data = {'labcity': labcity, 'ci': ci, 'Customer': Customer,
            'Doctor': Doctor, 'Doctor_experience': Doctor_experience,
            'All_Doctor': All_Doctor, 'labcitys': labcitys,
            'All_Speciality': All_Speciality, 'S_N': S_N,
            'doctor_clinic': doctor_clinic, 'F_l_to_H': F_l_to_H,
            'F_H_to_l': F_H_to_l
            }
    return render(request, 'view_all_specialist.html', Data)


def Book_appointment(request, id):
    formatDate1 = None
    formatDate1_back = None
    formatDate3 = None
    formatDate3_back = None
    formatDate4 = None
    formatDate4_back = None
    formatDate5 = None
    formatDate5_back = None
    formatDate6 = None
    formatDate6_back = None
    formatDate7 = None
    formatDate7_back = None
    formatDate8 = None
    formatDate8_back = None
    formatDate9 = None
    formatDate9_back = None
    formatDate10 = None
    formatDate10_back = None
    formatDate11 = None
    formatDate11_back = None
    Booked_Slots_list = []

    Appointment_Slot_list1 = []
    Appointment_Slot_list2 = []
    Appointment_Slot_list3 = []
    Appointment_Slot_list4 = []
    Appointment_Slot_list5 = []
    Appointment_Slot_list6 = []
    Appointment_Slot_list7 = []
    Appointment_Slot_list8 = []
    Appointment_Slot_list9 = []
    Appointment_Slot_list10 = []
    Appointment_Slot_list11 = []

    slot_list1 = []
    slot_list2 = []
    slot_list3 = []
    slot_list4 = []
    slot_list5 = []
    slot_list6 = []
    slot_list7 = []
    slot_list8 = []
    slot_list9 = []
    slot_list10 = []
    slot_list11 = []

    labcitys = Labcity.objects.all()
    All_Speciality = Special.objects.all().order_by('Doctor_Speciality')
    doctor_clinic = Clinic.objects.all()
    labcity = Labcity.objects.all()
    Doctor = Doctors.objects.filter(is_Active=True, id=id)
    Doctor_get = Doctors.objects.get(is_Active=True, id=id)

    Booked_Slots = Appointment.objects.filter(Doctor=id)

    print(Booked_Slots_list)
    Appointment_Slots = Doctors.objects.get(id=id)

    Start_time = Appointment_Slots.Doctor_Clinic.clinic_time_start
    Start_time = str(Start_time)
    End_time = Appointment_Slots.Doctor_Clinic.clinic_time_end
    End_time = str(End_time)

    Appointment_Slots_start = datetime.strptime(Start_time, '%H:%M:%S')
    Appointment_Slots_end = datetime.strptime(End_time, '%H:%M:%S')
    Per_app_time = Appointment_Slots.Doctor_Clinic.Patient_day
    # Appointment_Slot = Appointment_Slots_start + timedelta(minutes=Per_app_time)

    n = 0

    Today = date.today()
    day1 = Today.strftime("%A")
    if day1 == "Monday":
        if Doctor_get.Doctor_Clinic.Monday:
            formatDate1 = Today.strftime("%d-%b")
            formatDate1_back = Today.strftime("%Y-%m-%d")
    elif day1 == "Tuesday":
        if Doctor_get.Doctor_Clinic.Tuesday:
            formatDate1 = Today.strftime("%d-%b")
            formatDate1_back = Today.strftime("%Y-%m-%d")
    elif day1 == "Wednesday":
        if Doctor_get.Doctor_Clinic.Wednesday:
            formatDate1 = Today.strftime("%d-%b")
            formatDate1_back = Today.strftime("%Y-%m-%d")
    elif day1 == "Thursday":
        if Doctor_get.Doctor_Clinic.Thursday:
            formatDate1 = Today.strftime("%d-%b")
            formatDate1_back = Today.strftime("%Y-%m-%d")
    elif day1 == "Friday":
        if Doctor_get.Doctor_Clinic.Friday:
            formatDate1 = Today.strftime("%d-%b")
            formatDate1_back = Today.strftime("%Y-%m-%d")
    elif day1 == "Saturday":
        if Doctor_get.Doctor_Clinic.Saturday:
            formatDate1 = Today.strftime("%d-%b")
            formatDate1_back = Today.strftime("%Y-%m-%d")
    elif day1 == "Sunday":
        if Doctor_get.Doctor_Clinic.Sunday:
            formatDate1 = Today.strftime("%d-%b")
            formatDate1_back = Today.strftime("%Y-%m-%d")

    for i in range(1, 100):
        if Appointment_Slots_start < Appointment_Slots_end:
            n = n + Per_app_time
            Appointment_Slots_start = Appointment_Slots_start + timedelta(minutes=Per_app_time)
            slot = Appointment_Slots_start.strftime('%H:%M:%S')
            current_datetime = datetime.today().strftime('%H:%M:%S')
            if slot > current_datetime:
                Appointment_Slot_list1.append(slot)
    for i in Booked_Slots:
        if i.Appointment_date == Today:
            Booked_Slots_list.append(i.time_start)
    for element in Booked_Slots_list:
        if element in Appointment_Slot_list1:
            Appointment_Slot_list1.remove(element)
    slot_list1 = Appointment_Slot_list1.copy()
    Appointment_Slots_start = Appointment_Slots_start - timedelta(minutes=n)

    next_day = timedelta(days=1)
    date2 = Today + next_day
    day2 = date2.strftime("%A")
    if day2 == "Monday":
        if Doctor_get.Doctor_Clinic.Monday:
            formatDate2 = date2.strftime("%d-%b")
            formatDate2_back = date2.strftime("%Y-%m-%d")
        else:
            formatDate2 = None
            formatDate2_back = None
    elif day2 == "Tuesday":
        if Doctor_get.Doctor_Clinic.Tuesday:
            formatDate2 = date2.strftime("%d-%b")
            formatDate2_back = date2.strftime("%Y-%m-%d")
        else:
            formatDate2 = None
            formatDate2_back = None
    elif day2 == "Wednesday":
        if Doctor_get.Doctor_Clinic.Wednesday:
            formatDate2 = date2.strftime("%d-%b")
            formatDate2_back = date2.strftime("%Y-%m-%d")
        else:
            formatDate2 = None
            formatDate2_back = None
    elif day2 == "Thursday":
        if Doctor_get.Doctor_Clinic.Thursday:
            formatDate2 = date2.strftime("%d-%b")
            formatDate2_back = date2.strftime("%Y-%m-%d")
        else:
            formatDate2 = None
            formatDate2_back = None
    elif day2 == "Friday":
        if Doctor_get.Doctor_Clinic.Friday:
            formatDate2 = date2.strftime("%d-%b")
            formatDate2_back = date2.strftime("%Y-%m-%d")
        else:
            formatDate2 = None
            formatDate2_back = None
    elif day2 == "Saturday":
        if Doctor_get.Doctor_Clinic.Saturday:
            formatDate2 = date2.strftime("%d-%b")
            formatDate2_back = date2.strftime("%Y-%m-%d")
        else:
            formatDate2 = None
            formatDate2_back = None
    elif day2 == "Sunday":
        if Doctor_get.Doctor_Clinic.Sunday:
            formatDate2 = date2.strftime("%d-%b")
            formatDate2_back = date2.strftime("%Y-%m-%d")
        else:
            formatDate2 = None
            formatDate2_back = None
    n = 0
    for i in range(1, 100):
        if Appointment_Slots_start < Appointment_Slots_end:
            n = n + Per_app_time
            Appointment_Slots_start = Appointment_Slots_start + timedelta(minutes=Per_app_time)
            slot = Appointment_Slots_start.strftime('%H:%M:%S')
            Appointment_Slot_list2.append(slot)
    Booked_Slots_list.clear()
    for i in Booked_Slots:
        if i.Appointment_date == date2:
            print("Date Compare = \n\n ")
            Booked_Slots_list.append(i.time_start)
            print(Booked_Slots_list)
    for element in Booked_Slots_list:
        if element in Appointment_Slot_list2:
            Appointment_Slot_list2.remove(element)
    slot_list2 = Appointment_Slot_list2.copy()
    Appointment_Slots_start = Appointment_Slots_start - timedelta(minutes=n)

    next_day = timedelta(days=2)
    date3 = Today + next_day
    day3 = date3.strftime("%A")
    if day3 == "Monday":
        if Doctor_get.Doctor_Clinic.Monday:
            formatDate3 = date3.strftime("%d-%b")
            formatDate3_back = date3.strftime("%Y-%m-%d")
    elif day3 == "Tuesday":
        if Doctor_get.Doctor_Clinic.Tuesday:
            formatDate3 = date3.strftime("%d-%b")
            formatDate3_back = date3.strftime("%Y-%m-%d")
    elif day3 == "Wednesday":
        if Doctor_get.Doctor_Clinic.Wednesday:
            formatDate3 = date3.strftime("%d-%b")
            formatDate3_back = date3.strftime("%Y-%m-%d")
    elif day3 == "Thursday":
        if Doctor_get.Doctor_Clinic.Thursday:
            formatDate3 = date3.strftime("%d-%b")
            formatDate3_back = date3.strftime("%Y-%m-%d")
    elif day3 == "Friday":
        if Doctor_get.Doctor_Clinic.Friday:
            formatDate3 = date3.strftime("%d-%b")
            formatDate3_back = date3.strftime("%Y-%m-%d")
    elif day3 == "Saturday":
        if Doctor_get.Doctor_Clinic.Saturday:
            formatDate3 = date3.strftime("%d-%b")
            formatDate3_back = date3.strftime("%Y-%m-%d")
    elif day3 == "Sunday":
        if Doctor_get.Doctor_Clinic.Sunday:
            formatDate3 = date3.strftime("%d-%b")
            formatDate3_back = date3.strftime("%Y-%m-%d")
    n = 0
    for i in range(1, 100):
        if Appointment_Slots_start < Appointment_Slots_end:
            n = n + Per_app_time
            Appointment_Slots_start = Appointment_Slots_start + timedelta(minutes=Per_app_time)
            slot = Appointment_Slots_start.strftime('%H:%M:%S')
            Appointment_Slot_list3.append(slot)
    Booked_Slots_list.clear()
    for i in Booked_Slots:
        if i.Appointment_date == date3:
            Booked_Slots_list.append(i.time_start)
    for element in Booked_Slots_list:
        if element in Appointment_Slot_list3:
            Appointment_Slot_list3.remove(element)
    slot_list3 = Appointment_Slot_list3.copy()
    Appointment_Slots_start = Appointment_Slots_start - timedelta(minutes=n)

    next_day = timedelta(days=3)
    date4 = Today + next_day
    day4 = date4.strftime("%A")
    if day4 == "Monday":
        if Doctor_get.Doctor_Clinic.Monday:
            formatDate4 = date4.strftime("%d-%b")
            formatDate4_back = date4.strftime("%Y-%m-%d")
    elif day4 == "Tuesday":
        if Doctor_get.Doctor_Clinic.Tuesday:
            formatDate4 = date4.strftime("%d-%b")
            formatDate4_back = date4.strftime("%Y-%m-%d")
    elif day4 == "Wednesday":
        if Doctor_get.Doctor_Clinic.Wednesday:
            formatDate4 = date4.strftime("%d-%b")
            formatDate4_back = date4.strftime("%Y-%m-%d")
    elif day4 == "Thursday":
        if Doctor_get.Doctor_Clinic.Thursday:
            formatDate4 = date4.strftime("%d-%b")
            formatDate4_back = date4.strftime("%Y-%m-%d")
    elif day4 == "Friday":
        if Doctor_get.Doctor_Clinic.Friday:
            formatDate4 = date4.strftime("%d-%b")
            formatDate4_back = date4.strftime("%Y-%m-%d")
    elif day4 == "Saturday":
        if Doctor_get.Doctor_Clinic.Saturday:
            formatDate4 = date4.strftime("%d-%b")
            formatDate4_back = date4.strftime("%Y-%m-%d")
    elif day4 == "Sunday":
        if Doctor_get.Doctor_Clinic.Sunday:
            formatDate4 = date4.strftime("%d-%b")
            formatDate4_back = date4.strftime("%Y-%m-%d")
    n = 0
    for i in range(1, 100):
        if Appointment_Slots_start < Appointment_Slots_end:
            n = n + Per_app_time
            Appointment_Slots_start = Appointment_Slots_start + timedelta(minutes=Per_app_time)
            slot = Appointment_Slots_start.strftime('%H:%M:%S')
            Appointment_Slot_list4.append(slot)
    Booked_Slots_list.clear()
    for i in Booked_Slots:
        if i.Appointment_date == date4:
            Booked_Slots_list.append(i.time_start)
    for element in Booked_Slots_list:
        if element in Appointment_Slot_list4:
            Appointment_Slot_list4.remove(element)
    slot_list4 = Appointment_Slot_list4.copy()
    Appointment_Slots_start = Appointment_Slots_start - timedelta(minutes=n)

    next_day = timedelta(days=4)
    date5 = Today + next_day
    day5 = date5.strftime("%A")
    if day5 == "Monday":
        if Doctor_get.Doctor_Clinic.Monday:
            formatDate5 = date5.strftime("%d-%b")
            formatDate5_back = date5.strftime("%Y-%m-%d")
    elif day5 == "Tuesday":
        if Doctor_get.Doctor_Clinic.Tuesday:
            formatDate5 = date5.strftime("%d-%b")
            formatDate5_back = date5.strftime("%Y-%m-%d")
    elif day5 == "Wednesday":
        if Doctor_get.Doctor_Clinic.Wednesday:
            formatDate5 = date5.strftime("%d-%b")
            formatDate5_back = date5.strftime("%Y-%m-%d")
    elif day5 == "Thursday":
        if Doctor_get.Doctor_Clinic.Thursday:
            formatDate5 = date5.strftime("%d-%b")
            formatDate5_back = date5.strftime("%Y-%m-%d")
    elif day5 == "Friday":
        if Doctor_get.Doctor_Clinic.Friday:
            formatDate5 = date5.strftime("%d-%b")
            formatDate5_back = date5.strftime("%Y-%m-%d")
    elif day5 == "Saturday":
        if Doctor_get.Doctor_Clinic.Saturday:
            formatDate5 = date5.strftime("%d-%b")
            formatDate5_back = date5.strftime("%Y-%m-%d")
    elif day5 == "Sunday":
        if Doctor_get.Doctor_Clinic.Sunday:
            formatDate5 = date5.strftime("%d-%b")
            formatDate5_back = date5.strftime("%Y-%m-%d")
    n = 0
    for i in range(1, 100):
        if Appointment_Slots_start < Appointment_Slots_end:
            n = n + Per_app_time
            Appointment_Slots_start = Appointment_Slots_start + timedelta(minutes=Per_app_time)
            slot = Appointment_Slots_start.strftime('%H:%M:%S')
            Appointment_Slot_list5.append(slot)
    Booked_Slots_list.clear()
    for i in Booked_Slots:
        if i.Appointment_date == date5:
            Booked_Slots_list.append(i.time_start)
    for element in Booked_Slots_list:
        if element in Appointment_Slot_list5:
            Appointment_Slot_list5.remove(element)
    slot_list5 = Appointment_Slot_list5.copy()
    Appointment_Slots_start = Appointment_Slots_start - timedelta(minutes=n)

    next_day = timedelta(days=5)
    date6 = Today + next_day
    day6 = date6.strftime("%A")
    if day6 == "Monday":
        if Doctor_get.Doctor_Clinic.Monday:
            formatDate6 = date6.strftime("%d-%b")
            formatDate6_back = date6.strftime("%Y-%m-%d")
    elif day6 == "Tuesday":
        if Doctor_get.Doctor_Clinic.Tuesday:
            formatDate6 = date6.strftime("%d-%b")
            formatDate6_back = date6.strftime("%Y-%m-%d")
    elif day6 == "Wednesday":
        if Doctor_get.Doctor_Clinic.Wednesday:
            formatDate6 = date6.strftime("%d-%b")
            formatDate6_back = date6.strftime("%Y-%m-%d")
    elif day6 == "Thursday":
        if Doctor_get.Doctor_Clinic.Thursday:
            formatDate6 = date6.strftime("%d-%b")
            formatDate6_back = date6.strftime("%Y-%m-%d")
    elif day6 == "Friday":
        if Doctor_get.Doctor_Clinic.Friday:
            formatDate6 = date6.strftime("%d-%b")
            formatDate6_back = date6.strftime("%Y-%m-%d")
    elif day6 == "Saturday":
        if Doctor_get.Doctor_Clinic.Saturday:
            formatDate6 = date6.strftime("%d-%b")
            formatDate6_back = date6.strftime("%Y-%m-%d")
    elif day6 == "Sunday":
        if Doctor_get.Doctor_Clinic.Sunday:
            formatDate6 = date6.strftime("%d-%b")
            formatDate6_back = date6.strftime("%Y-%m-%d")
    n = 0
    for i in range(1, 100):
        if Appointment_Slots_start < Appointment_Slots_end:
            n = n + Per_app_time
            Appointment_Slots_start = Appointment_Slots_start + timedelta(minutes=Per_app_time)
            slot = Appointment_Slots_start.strftime('%H:%M:%S')
            Appointment_Slot_list6.append(slot)
    Booked_Slots_list.clear()
    for i in Booked_Slots:
        if i.Appointment_date == date6:
            Booked_Slots_list.append(i.time_start)
    for element in Booked_Slots_list:
        if element in Appointment_Slot_list6:
            Appointment_Slot_list6.remove(element)
    slot_list6 = Appointment_Slot_list6.copy()
    Appointment_Slots_start = Appointment_Slots_start - timedelta(minutes=n)

    next_day = timedelta(days=6)
    date7 = Today + next_day
    day7 = date7.strftime("%A")
    if day7 == "Monday":
        if Doctor_get.Doctor_Clinic.Monday:
            formatDate7 = date7.strftime("%d-%b")
            formatDate7_back = date7.strftime("%Y-%m-%d")
    elif day7 == "Tuesday":
        if Doctor_get.Doctor_Clinic.Tuesday:
            formatDate7 = date7.strftime("%d-%b")
            formatDate7_back = date7.strftime("%Y-%m-%d")
    elif day7 == "Wednesday":
        if Doctor_get.Doctor_Clinic.Wednesday:
            formatDate7 = date7.strftime("%d-%b")
            formatDate7_back = date7.strftime("%Y-%m-%d")
    elif day7 == "Thursday":
        if Doctor_get.Doctor_Clinic.Thursday:
            formatDate7 = date7.strftime("%d-%b")
            formatDate7_back = date7.strftime("%Y-%m-%d")
    elif day7 == "Friday":
        if Doctor_get.Doctor_Clinic.Friday:
            formatDate7 = date7.strftime("%d-%b")
            formatDate7_back = date7.strftime("%Y-%m-%d")
    elif day7 == "Saturday":
        if Doctor_get.Doctor_Clinic.Saturday:
            formatDate7 = date7.strftime("%d-%b")
            formatDate7_back = date7.strftime("%Y-%m-%d")
    elif day7 == "Sunday":
        if Doctor_get.Doctor_Clinic.Sunday:
            formatDate7 = date7.strftime("%d-%b")
            formatDate7_back = date7.strftime("%Y-%m-%d")
    n = 0
    for i in range(1, 100):
        if Appointment_Slots_start < Appointment_Slots_end:
            n = n + Per_app_time
            Appointment_Slots_start = Appointment_Slots_start + timedelta(minutes=Per_app_time)
            slot = Appointment_Slots_start.strftime('%H:%M:%S')
            Appointment_Slot_list7.append(slot)
    Booked_Slots_list.clear()
    for i in Booked_Slots:
        if i.Appointment_date == date7:
            Booked_Slots_list.append(i.time_start)
    for element in Booked_Slots_list:
        if element in Appointment_Slot_list7:
            Appointment_Slot_list7.remove(element)
    slot_list7 = Appointment_Slot_list7.copy()
    Appointment_Slots_start = Appointment_Slots_start - timedelta(minutes=n)

    next_day = timedelta(days=7)
    date8 = Today + next_day
    day8 = date8.strftime("%A")
    if day8 == "Monday":
        if Doctor_get.Doctor_Clinic.Monday:
            formatDate8 = date8.strftime("%d-%b")
            formatDate8_back = date8.strftime("%Y-%m-%d")
    elif day8 == "Tuesday":
        if Doctor_get.Doctor_Clinic.Tuesday:
            formatDate8 = date8.strftime("%d-%b")
            formatDate8_back = date8.strftime("%Y-%m-%d")
    elif day8 == "Wednesday":
        if Doctor_get.Doctor_Clinic.Wednesday:
            formatDate8 = date8.strftime("%d-%b")
            formatDate8_back = date8.strftime("%Y-%m-%d")
    elif day8 == "Thursday":
        if Doctor_get.Doctor_Clinic.Thursday:
            formatDate8 = date8.strftime("%d-%b")
            formatDate8_back = date8.strftime("%Y-%m-%d")
    elif day8 == "Friday":
        if Doctor_get.Doctor_Clinic.Friday:
            formatDate8 = date8.strftime("%d-%b")
            formatDate8_back = date8.strftime("%Y-%m-%d")
    elif day8 == "Saturday":
        if Doctor_get.Doctor_Clinic.Saturday:
            formatDate8 = date8.strftime("%d-%b")
            formatDate8_back = date8.strftime("%Y-%m-%d")
    elif day8 == "Sunday":
        if Doctor_get.Doctor_Clinic.Sunday:
            formatDate8 = date8.strftime("%d-%b")
            formatDate8_back = date8.strftime("%Y-%m-%d")
    n = 0
    for i in range(1, 100):
        if Appointment_Slots_start < Appointment_Slots_end:
            n = n + Per_app_time
            Appointment_Slots_start = Appointment_Slots_start + timedelta(minutes=Per_app_time)
            slot = Appointment_Slots_start.strftime('%H:%M:%S')
            Appointment_Slot_list8.append(slot)
    Booked_Slots_list.clear()
    for i in Booked_Slots:
        if i.Appointment_date == date8:
            Booked_Slots_list.append(i.time_start)
    for element in Booked_Slots_list:
        if element in Appointment_Slot_list8:
            Appointment_Slot_list8.remove(element)
    slot_list8 = Appointment_Slot_list8.copy()
    Appointment_Slots_start = Appointment_Slots_start - timedelta(minutes=n)

    next_day = timedelta(days=8)
    date9 = Today + next_day
    day9 = date9.strftime("%A")
    if day9 == "Monday":
        if Doctor_get.Doctor_Clinic.Monday:
            formatDate9 = date9.strftime("%d-%b")
            formatDate9_back = date9.strftime("%Y-%m-%d")
    elif day9 == "Tuesday":
        if Doctor_get.Doctor_Clinic.Tuesday:
            formatDate9 = date9.strftime("%d-%b")
            formatDate9_back = date9.strftime("%Y-%m-%d")
    elif day9 == "Wednesday":
        if Doctor_get.Doctor_Clinic.Wednesday:
            formatDate9 = date9.strftime("%d-%b")
            formatDate9_back = date9.strftime("%Y-%m-%d")
    elif day9 == "Thursday":
        if Doctor_get.Doctor_Clinic.Thursday:
            formatDate9 = date9.strftime("%d-%b")
            formatDate9_back = date9.strftime("%Y-%m-%d")
    elif day9 == "Friday":
        if Doctor_get.Doctor_Clinic.Friday:
            formatDate9 = date9.strftime("%d-%b")
            formatDate9_back = date9.strftime("%Y-%m-%d")
    elif day9 == "Saturday":
        if Doctor_get.Doctor_Clinic.Saturday:
            formatDate9 = date9.strftime("%d-%b")
            formatDate9_back = date9.strftime("%Y-%m-%d")
    elif day9 == "Sunday":
        if Doctor_get.Doctor_Clinic.Sunday:
            formatDate9 = date9.strftime("%d-%b")
            formatDate9_back = date9.strftime("%Y-%m-%d")
    n = 0
    for i in range(1, 100):
        if Appointment_Slots_start < Appointment_Slots_end:
            n = n + Per_app_time
            Appointment_Slots_start = Appointment_Slots_start + timedelta(minutes=Per_app_time)
            slot = Appointment_Slots_start.strftime('%H:%M:%S')
            Appointment_Slot_list9.append(slot)
    Booked_Slots_list.clear()
    for i in Booked_Slots:
        if i.Appointment_date == date9:
            Booked_Slots_list.append(i.time_start)
    for element in Booked_Slots_list:
        if element in Appointment_Slot_list9:
            Appointment_Slot_list9.remove(element)
    slot_list9 = Appointment_Slot_list9.copy()
    Appointment_Slots_start = Appointment_Slots_start - timedelta(minutes=n)

    next_day = timedelta(days=9)
    date10 = Today + next_day
    day10 = date10.strftime("%A")
    if day10 == "Monday":
        if Doctor_get.Doctor_Clinic.Monday:
            formatDate10 = date10.strftime("%d-%b")
            formatDate10_back = date10.strftime("%Y-%m-%d")
    elif day10 == "Tuesday":
        if Doctor_get.Doctor_Clinic.Tuesday:
            formatDate10 = date10.strftime("%d-%b")
            formatDate10_back = date10.strftime("%Y-%m-%d")
    elif day10 == "Wednesday":
        if Doctor_get.Doctor_Clinic.Wednesday:
            formatDate10 = date10.strftime("%d-%b")
            formatDate10_back = date10.strftime("%Y-%m-%d")
    elif day10 == "Thursday":
        if Doctor_get.Doctor_Clinic.Thursday:
            formatDate10 = date10.strftime("%d-%b")
            formatDate10_back = date10.strftime("%Y-%m-%d")
    elif day10 == "Friday":
        if Doctor_get.Doctor_Clinic.Friday:
            formatDate10 = date10.strftime("%d-%b")
            formatDate10_back = date10.strftime("%Y-%m-%d")
    elif day10 == "Saturday":
        if Doctor_get.Doctor_Clinic.Saturday:
            formatDate10 = date10.strftime("%d-%b")
            formatDate10_back = date10.strftime("%Y-%m-%d")
    elif day10 == "Sunday":
        if Doctor_get.Doctor_Clinic.Sunday:
            formatDate10 = date10.strftime("%d-%b")
            formatDate10_back = date10.strftime("%Y-%m-%d")
    n = 0
    for i in range(1, 100):
        if Appointment_Slots_start < Appointment_Slots_end:
            n = n + Per_app_time
            Appointment_Slots_start = Appointment_Slots_start + timedelta(minutes=Per_app_time)
            slot = Appointment_Slots_start.strftime('%H:%M:%S')
            Appointment_Slot_list10.append(slot)
    Booked_Slots_list.clear()
    for i in Booked_Slots:
        if i.Appointment_date == date10:
            Booked_Slots_list.append(i.time_start)
    for element in Booked_Slots_list:
        if element in Appointment_Slot_list10:
            Appointment_Slot_list10.remove(element)
    slot_list10 = Appointment_Slot_list10.copy()
    Appointment_Slots_start = Appointment_Slots_start - timedelta(minutes=n)

    next_day = timedelta(days=10)
    date11 = Today + next_day
    day11 = date11.strftime("%A")
    if day11 == "Monday":
        if Doctor_get.Doctor_Clinic.Monday:
            formatDate11 = date11.strftime("%d-%b")
            formatDate11_back = date11.strftime("%Y-%m-%d")
    elif day11 == "Tuesday":
        if Doctor_get.Doctor_Clinic.Tuesday:
            formatDate11 = date11.strftime("%d-%b")
            formatDate11_back = date11.strftime("%Y-%m-%d")
    elif day11 == "Wednesday":
        if Doctor_get.Doctor_Clinic.Wednesday:
            formatDate11 = date11.strftime("%d-%b")
            formatDate11_back = date11.strftime("%Y-%m-%d")
    elif day11 == "Thursday":
        if Doctor_get.Doctor_Clinic.Thursday:
            formatDate11 = date11.strftime("%d-%b")
            formatDate11_back = date11.strftime("%Y-%m-%d")
    elif day11 == "Friday":
        if Doctor_get.Doctor_Clinic.Friday:
            formatDate11 = date11.strftime("%d-%b")
            formatDate11_back = date11.strftime("%Y-%m-%d")
    elif day11 == "Saturday":
        if Doctor_get.Doctor_Clinic.Saturday:
            formatDate11 = date11.strftime("%d-%b")
            formatDate11_back = date11.strftime("%Y-%m-%d")
    elif day11 == "Sunday":
        if Doctor_get.Doctor_Clinic.Sunday:
            formatDate11 = date11.strftime("%d-%b")
            formatDate11_back = date11.strftime("%Y-%m-%d")
    n = 0
    for i in range(1, 100):
        if Appointment_Slots_start < Appointment_Slots_end:
            n = n + Per_app_time
            Appointment_Slots_start = Appointment_Slots_start + timedelta(minutes=Per_app_time)
            slot = Appointment_Slots_start.strftime('%H:%M:%S')
            Appointment_Slot_list11.append(slot)
    Booked_Slots_list.clear()
    for i in Booked_Slots:
        if i.Appointment_date == date11:
            Booked_Slots_list.append(i.time_start)
    for element in Booked_Slots_list:
        if element in Appointment_Slot_list11:
            Appointment_Slot_list11.remove(element)
    slot_list11 = Appointment_Slot_list11.copy()
    Appointment_Slots_start = Appointment_Slots_start - timedelta(minutes=n)

    Customer = Patient.objects.all()
    if request.method == 'POST':
        pa = request.session.get('id')
        Patient_id = Patient.objects.get(id=pa)
        Data = request.POST
        patient_name = Data.get("patient_name")
        patient_phone = Data.get("patient_phone")
        Gender = Doctor_get.Gender
        patient_problem = Data.get("patient_problem")
        doctor_id = Doctor_get
        appointment_date = Data.get("appointment_date")
        appointment_time = Data.get("appointment_time")
        print(appointment_time)

        Appointment_Book = Appointment(Name=patient_name, patient_phone=patient_phone,
                                       Gender=Gender, Problem_detail=patient_problem,
                                       Doctor=doctor_id, Appointment_date=appointment_date,
                                       Time_slot=appointment_time, time_start=appointment_time,
                                       Patients=Patient_id
                                       )

        Appointment_Book.save()
        app_con = Appointment.objects.get(Name=patient_name, patient_phone=patient_phone,
                                          Gender=Gender, Problem_detail=patient_problem,
                                          Doctor=doctor_id, Appointment_date=appointment_date,
                                          Time_slot=appointment_time, time_start=appointment_time)
        Appointment_con_id = app_con.id
        return redirect("Appointment_Confirmation", id=Appointment_con_id)

    Data = {'labcity': labcity, 'Customer': Customer,
            'Doctor': Doctor, 'labcitys': labcitys,
            'All_Speciality': All_Speciality,
            'doctor_clinic': doctor_clinic, "Doctor_get": Doctor_get,

            "formatDate1": formatDate1, "formatDate1_back": formatDate1_back, "day1": day1,
            "formatDate2_back": formatDate2_back, "formatDate2": formatDate2, "day2": day2,
            "formatDate3_back": formatDate3_back, "formatDate3": formatDate3, "day3": day3,
            "formatDate4_back": formatDate4_back, "formatDate4": formatDate4, "day4": day4,
            "formatDate5_back": formatDate5_back, "formatDate5": formatDate5, "day5": day5,
            "formatDate6_back": formatDate6_back, "formatDate6": formatDate6, "day6": day6,
            "formatDate7_back": formatDate7_back, "formatDate7": formatDate7, "day7": day7,
            "formatDate8_back": formatDate8_back, "formatDate8": formatDate8, "day8": day8,
            "formatDate9_back": formatDate9_back, "formatDate9": formatDate9, "day9": day9,
            "formatDate10_back": formatDate10_back, "formatDate10": formatDate10, "day10": day10,
            "formatDate11_back": formatDate11_back, "formatDate11": formatDate11, "day11": day11,

            "slot_list1": slot_list1, "slot_list2": slot_list2, "slot_list3": slot_list3,
            "slot_list4": slot_list4, "slot_list5": slot_list5, "slot_list6": slot_list6,
            "slot_list7": slot_list7, "slot_list8": slot_list8, "slot_list9": slot_list9,
            "slot_list10": slot_list10, "slot_list11": slot_list11,
            }
    return render(request, 'book_appointment.html', Data)


def appointment_booked_Scheduled(request, id):
    Customer = Patient.objects.all()
    labcity = Labcity.objects.all()
    Appointment_con_id = Appointment.objects.get(id=id)
    print(Appointment_con_id)
    Data = {"Customer": Customer, "labcity": labcity,
            "Appointment_con_id": Appointment_con_id}
    return render(request, "appointment_booked_Scheduled.html", Data)


def Doctors_in_city(request, city):
    ci = None
    S_N = None
    labcitys = Labcity.objects.all()
    All_Speciality = Special.objects.all().order_by('Doctor_Speciality')

    labcity = Labcity.objects.all()
    All_Doctor = Doctors.objects.all()

    Doctor = Doctors.objects.filter(city=city)
    ci = Labcity.objects.filter(Lab_city_name__startswith=city)
    Doctor_experience = Doctors.objects.filter(city=city, is_Active=True).order_by('-Experience')

    F_l_to_H = Doctors.objects.filter(city=city, is_Active=True).order_by('Doctor_Clinic__Doctor_Fee')
    F_H_to_l = Doctors.objects.filter(city=city, is_Active=True).order_by('-Doctor_Clinic__Doctor_Fee')

    # Data = {'labcity': labcity}
    Customer = Patient.objects.all()
    Data = {'labcity': labcity, 'ci': ci, 'Customer': Customer,
            'Doctor': Doctor, 'Doctor_experience': Doctor_experience,
            'All_Doctor': All_Doctor, 'labcitys': labcitys,
            'All_Speciality': All_Speciality, 'S_N': S_N,
            'F_l_to_H': F_l_to_H, 'F_H_to_l': F_H_to_l
            }
    return render(request, 'view_all_specialist.html', Data)


def Doctors_Special(request, Speciality):
    ci = None
    S_N = None
    S_N = Speciality
    labcitys = Labcity.objects.all()
    All_Speciality = Special.objects.all().order_by('Doctor_Speciality')

    labcity = Labcity.objects.all()
    Doctor = Doctors.objects.filter(Speciality=S_N)
    All_Doctor = Doctors.objects.all()

    Doctor_experience = Doctors.objects.filter(Speciality=S_N).order_by('-Experience')

    F_l_to_H = Doctors.objects.filter(Speciality=S_N, is_Active=True).order_by('Doctor_Clinic__Doctor_Fee')
    F_H_to_l = Doctors.objects.filter(Speciality=S_N, is_Active=True).order_by('-Doctor_Clinic__Doctor_Fee')

    # Data = {'labcity': labcity}
    Customer = Patient.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        Specialist = request.POST.get('Specialist')
        city = request.POST.get('city')
        S_N = Speciality
        if city:
            if city == 'all':
                ci = None
            else:
                ci = Labcity.objects.filter(Lab_city_name__startswith=city)
        else:
            ci = None

        if name == 'search':
            ser = request.POST.get('search')
            Doctor = Doctors.objects.filter(Doctor_name__startswith=ser)
            Doctor_experience = Doctors.objects.filter(Doctor_name__startswith=ser).order_by('-Experience')
            if Doctor:
                Data = {'labcity': labcity, 'Customer': Customer,
                        'Doctor': Doctor, 'Doctor_experience': Doctor_experience,
                        'F_l_to_H': F_l_to_H, 'F_H_to_l': F_H_to_l,
                        'All_Doctor': All_Doctor, 'labcitys': labcitys,
                        'All_Speciality': All_Speciality, 'S_N': S_N
                        }
                return render(request, 'view_all_specialist.html', Data)
            Doctor = Doctors.objects.filter(Speciality__startswith=ser)
            Doctor_experience = Doctors.objects.filter(Speciality__startswith=ser).order_by('-Experience')
            if Doctor:
                Data = {'labcity': labcity, 'Customer': Customer,
                        'Doctor': Doctor, 'Doctor_experience': Doctor_experience,
                        'F_l_to_H': F_l_to_H, 'F_H_to_l': F_H_to_l,
                        'All_Doctor': All_Doctor, 'labcitys': labcitys,
                        'All_Speciality': All_Speciality, 'S_N': S_N
                        }
                return render(request, 'view_all_specialist.html', Data)

            Doctor = Doctors.objects.filter(city__startswith=ser)
            Doctor_experience = Doctors.objects.filter(city__startswith=ser).order_by('-Experience')
            ci = Labcity.objects.filter(Lab_city_name__startswith=ser)

            if Doctor:
                Data = {'labcity': labcity, 'ci': ci, 'Customer': Customer,
                        'Doctor': Doctor, 'Doctor_experience': Doctor_experience,
                        'F_l_to_H': F_l_to_H, 'F_H_to_l': F_H_to_l,
                        'All_Doctor': All_Doctor, 'labcitys': labcitys,
                        'All_Speciality': All_Speciality, 'S_N': S_N
                        }
                return render(request, 'view_all_specialist.html', Data)

    Data = {'labcity': labcity, 'ci': ci, 'Customer': Customer,
            'Doctor': Doctor, 'Doctor_experience': Doctor_experience,
            'F_l_to_H': F_l_to_H, 'F_H_to_l': F_H_to_l,
            'All_Doctor': All_Doctor, 'labcitys': labcitys,
            'All_Speciality': All_Speciality, 'S_N': S_N
            }
    return render(request, 'view_all_specialist.html', Data)


def Doctors_Special_in_city(request, Speciality, city):
    ci = None
    S_N = None
    S_N = Speciality
    labcitys = Labcity.objects.all()
    All_Speciality = Special.objects.all().order_by('Doctor_Speciality')

    labcity = Labcity.objects.all()
    All_Doctor = Doctors.objects.all()

    Doctor = Doctors.objects.filter(Speciality=S_N, city=city)
    ci = Labcity.objects.filter(Lab_city_name__startswith=city)
    Doctor_experience = Doctors.objects.filter(Speciality=S_N, city=city).order_by('-Experience')

    F_l_to_H = Doctors.objects.filter(Speciality=S_N, city=city, is_Active=True).order_by('Doctor_Clinic__Doctor_Fee')
    F_H_to_l = Doctors.objects.filter(Speciality=S_N, city=city, is_Active=True).order_by('-Doctor_Clinic__Doctor_Fee')

    # Data = {'labcity': labcity}
    Customer = Patient.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        Specialist = request.POST.get('Specialist')
        city = request.POST.get('city')
        S_N = Speciality
        if city:
            if city == 'all':
                ci = None
            else:
                ci = Labcity.objects.filter(Lab_city_name__startswith=city)
        else:
            ci = None

        if name == 'search':
            ser = request.POST.get('search')
            Doctor = Doctors.objects.filter(Doctor_name__startswith=ser)
            Doctor_experience = Doctors.objects.filter(Doctor_name__startswith=ser).order_by('-Experience')
            if Doctor:
                Data = {'labcity': labcity, 'Customer': Customer,
                        'Doctor': Doctor, 'Doctor_experience': Doctor_experience,
                        'F_l_to_H': F_l_to_H, 'F_H_to_l': F_H_to_l,
                        'All_Doctor': All_Doctor, 'labcitys': labcitys,
                        'All_Speciality': All_Speciality, 'S_N': S_N
                        }
                return render(request, 'view_all_specialist.html', Data)
            Doctor = Doctors.objects.filter(Speciality__startswith=ser)
            Doctor_experience = Doctors.objects.filter(Speciality__startswith=ser).order_by('-Experience')
            if Doctor:
                Data = {'labcity': labcity, 'Customer': Customer,
                        'Doctor': Doctor, 'Doctor_experience': Doctor_experience,
                        'F_l_to_H': F_l_to_H, 'F_H_to_l': F_H_to_l,
                        'All_Doctor': All_Doctor, 'labcitys': labcitys,
                        'All_Speciality': All_Speciality, 'S_N': S_N
                        }
                return render(request, 'view_all_specialist.html', Data)

            Doctor = Doctors.objects.filter(city__startswith=ser)
            Doctor_experience = Doctors.objects.filter(city__startswith=ser).order_by('-Experience')
            ci = Labcity.objects.filter(Lab_city_name__startswith=ser)

            if Doctor:
                Data = {'labcity': labcity, 'ci': ci, 'Customer': Customer,
                        'Doctor': Doctor, 'Doctor_experience': Doctor_experience,
                        'F_l_to_H': F_l_to_H, 'F_H_to_l': F_H_to_l,
                        'All_Doctor': All_Doctor, 'labcitys': labcitys,
                        'All_Speciality': All_Speciality, 'S_N': S_N
                        }
                return render(request, 'view_all_specialist.html', Data)

    Data = {'labcity': labcity, 'ci': ci, 'Customer': Customer,
            'Doctor': Doctor, 'Doctor_experience': Doctor_experience,
            'F_l_to_H': F_l_to_H, 'F_H_to_l': F_H_to_l,
            'All_Doctor': All_Doctor, 'labcitys': labcitys,
            'All_Speciality': All_Speciality, 'S_N': S_N
            }
    return render(request, 'view_all_specialist.html', Data)


def view_specialities(request):
    All_Speciality = Special.objects.all().order_by('Doctor_Speciality')
    labcity = Labcity.objects.all()
    Doctor = Doctors.objects.all()
    All_Doctor = Doctors.objects.all()

    # Data = {'labcity': labcity}
    Customer = Patient.objects.all()
    if request.method == 'POST':
        Data = request.POST
        ser = request.POST.get('search')
        All_Speciality = Special.objects.filter(Doctor_Speciality__startswith=ser).order_by('Doctor_Speciality')

    Data = {'labcity': labcity, 'Customer': Customer,
            'Doctor': Doctor, 'All_Doctor': All_Doctor,
            'All_Speciality': All_Speciality}
    return render(request, 'view_all_specialities.html', Data)


def Health_blog(request):
    Blogs_new_count = 0
    search = None
    labcity = Labcity.objects.all()
    Customer = Patient.objects.all()

    Blogs = Health_blogs.objects.all()
    paginator = Paginator(Blogs, 5)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    Blogs_new = Health_blogs.objects.all().order_by('-blog_create_time')
    if request.method == 'POST':
        data = request.POST
        search = data.get('search')
        Blogs = Health_blogs.objects.filter(Health_blogs_issue__startswith=search)
        Blogs_new = Health_blogs.objects.filter(Health_blogs_issue__startswith=search)
        Blogs_new_count = Health_blogs.objects.filter(Health_blogs_issue__startswith=search).count()

    Data = {'Customer': Customer, 'labcity': labcity,
            'Blogs': Blogs, "Blogs_new": Blogs_new,
            "search": search, "Blogs_new_count": Blogs_new_count,
            'page_obj': page_obj}
    return render(request, 'Health_blogs.html', Data)


def blog_via_issue(request, Health_blogs_issue):
    labcity = Labcity.objects.all()
    Customer = Patient.objects.all()
    Blogs = Health_blogs.objects.filter(Health_blogs_issue=Health_blogs_issue)
    Blogs_new = Health_blogs.objects.filter(Health_blogs_issue=Health_blogs_issue)
    Data = {'Customer': Customer, 'labcity': labcity,
            'Blogs': Blogs, 'Blogs_new': Blogs_new}
    return render(request, 'blog_via_issue.html', Data)


def blog_detail(request, id, Health_blogs_issue):
    labcity = Labcity.objects.all()
    Customer = Patient.objects.all()
    Blogs = Health_blogs.objects.get(id=id, Health_blogs_issue=Health_blogs_issue)
    Blogs_next = Health_blogs.objects.last()
    print(Blogs, '\n', Blogs_next)
    Data = {'Customer': Customer, 'labcity': labcity, 'Blogs': Blogs}
    return render(request, 'Blog_detail.html', Data)


# ///////////////////////////////////////Doctor_Login admin Login ////////////////////////////////////////////////////////
@Doctor_login_check
def Doctor_Login(request):
    success_message = None
    if request.method == 'GET':
        print('doctor login')
        return render(request, 'doctor_login.html')
    else:
        Data = request.POST
        email = Data.get('email')
        password = Data.get('password')

        # # Validations
        Doctor = Doctors.objects.filter(email=email, password=password)

        Doctor_active = Doctors.objects.filter(email=email, password=password, is_Active=True)
        error_message = None
        #

        if Doctor:
            if not Doctor_active:
                error_message = email + " is Deactivated by the TakeCare Team"
            for i in Doctor:
                request.session['doctor_id'] = i.id
                fa = request.session['doctor_email'] = i.email
                success_message = 'Login Successfully'
                return redirect(Doctor_admin)
        else:
            error_message = "Email or Password Invalid......"
        # return render(request, 'Login.html', {'error': error_message})
    return render(request, 'doctor_login.html', {'error': error_message, 'success': success_message})


# ////////////////////////////Functions Related  Doctor Admin Dashboard+profile page start///////////////////////////

@Doctor_middleware
def Doctor_admin(request):
    error_message = None
    success = None
    lb = request.session.get('doctor_id')

    Test_today = 0
    month = datetime.now().month
    year = datetime.now().year
    Appointment_pending = Appointment.objects.filter(Status='Pending', Doctor=lb).count()
    Appointment_conform = Appointment.objects.filter(Status='Accepted', Doctor=lb).count()
    Appointment_today = Appointment.objects.filter(Appointment_date=datetime.now(), Doctor=lb).count()
    total_Appointments = Appointment.objects.filter(Doctor=lb).count()
    Appointments = Appointment.objects.filter(Doctor=lb).order_by('Appointment_date')

    current_doctor = Doctors.objects.get(id=lb)
    Data = {"current_doctor": current_doctor, "Appointments": Appointments,
            "Appointment_pending": Appointment_pending,
            "Appointment_conform": Appointment_conform, "Appointment_today": Appointment_today,
            "total_Appointments": total_Appointments}
    return render(request, 'Doctor_admin_site/index.html', Data)


@Doctor_middleware
def Doctor_profile(request):
    error_message = None
    success = None
    lb = request.session.get('doctor_id')
    # print(lb)
    current_doctor = Doctors.objects.get(id=lb)
    if request.method == 'POST':
        data = request.POST
        Current_password = data.get('C_pass')
        New_password = data.get('New_password')
        Confirm_password = data.get('NConform_pass')
        if current_doctor.password == Current_password:
            if New_password != Confirm_password:
                error_message = 'Password and Comfort Password must be same'
            elif len(New_password) < 8:
                error_message = " Password must be At-least 8 digit long "
            else:
                current_doctor.password = New_password
                current_doctor.save()
                success = "Your Password Updated Successfully"

        else:
            error_message = "Please Check Your Current Password You Enter"

    current_doctor = Doctors.objects.get(id=lb)
    Data = {"current_doctor": current_doctor, 'error': error_message,
            'success': success}
    return render(request, "Doctor_admin_site/Doctor_profile_page.html", Data)


@Doctor_middleware
def updates_Doctor_profile(request):
    error_message = None
    success = None
    lb = request.session.get('doctor_id')
    # print(lb)
    current_doctor = Doctors.objects.get(id=lb)
    if request.method == 'POST':
        data = request.POST
        name = data.get("username")
        phone = data.get("phone")
        Address = data.get("Address")
        Experience = data.get("Experience")
        Doctor_profile_img = request.FILES.get('image')

        if name:
            name = name.capitalize()
            current_doctor.Doctor_name = name
            current_doctor.save()
            success = "Your Name Change Successfully"
        elif phone:
            if len(phone) < 10:
                error_message = " Password must be At-least 10 digit long without first '0' "
            else:
                current_doctor.Callnumber = phone
                current_doctor.save()
                success = "Your Phone number Change Successfully"
        elif Address:
            Address = Address.capitalize()
            current_doctor.Address = Address
            current_doctor.save()
            success = "Your Address Change Successfully"
        elif Experience:
            current_doctor.Experience = Experience
            current_doctor.save()
            success = "Your Medical Profile Updated Successfully"
        elif Doctor_profile_img:
            current_doctor.img = Doctor_profile_img
            current_doctor.save()
            success = "Your Profile Image Change Successfully"

    current_doctor = Doctors.objects.get(id=lb)
    Data = {"current_doctor": current_doctor, 'error': error_message,
            'success': success}
    return render(request, "Doctor_admin_site/Doctor_profile_page.html", Data)


@Doctor_middleware
def clinic_profile(request):
    error_message = None
    success = None
    lb = request.session.get('doctor_id')
    current_doctor = Doctors.objects.get(id=lb)

    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        email = data.get('email')
        Clinic_Address = data.get('Address')
        Fee = data.get('Fee')
        phone = data.get('phone')
        Start_time = data.get('Start_time')
        End_time = data.get("End_time")
        ALL_DAYS = data.getlist('Days')
        N_A_PD = data.get('N_A_PD')
        N_A_PD = int(N_A_PD)
        Monday = False
        Tuesday = False
        Wednesday = False
        Thursday = False
        Friday = False
        Saturday = False
        Sunday = False

        print("type = ", type(N_A_PD))
        for i in ALL_DAYS:
            if i == "Monday":
                Monday = True
            elif i == "Tuesday":
                Tuesday = True
            elif i == "Wednesday":
                Wednesday = True
            elif i == "Thursday":
                Thursday = True
            elif i == "Friday":
                Friday = True
            elif i == "Saturday":
                Saturday = True
            elif i == "Sunday":
                Sunday = True
        #
        time_1 = datetime.strptime(Start_time, "%H:%M")
        time_2 = datetime.strptime(End_time, "%H:%M")
        Time = (time_2 - time_1)
        Per_appointment_time = (time_2 - time_1) / N_A_PD
        print(name, Clinic_Address, Fee, phone, Start_time, End_time, Time, N_A_PD, Per_appointment_time, ALL_DAYS)

        clinic = Clinic(Clinic_Name=name, Doctor_email=email, Location=Clinic_Address,
                        Doctor_Fee=Fee, Clinic_Number=phone, Patient_day=N_A_PD,
                        clinic_time_start=Start_time, clinic_time_end=End_time,
                        Monday=Monday, Tuesday=Tuesday, Wednesday=Wednesday,
                        Thursday=Thursday, Friday=Friday, Saturday=Saturday,
                        Sunday=Sunday
                        )
        clinic.save()
        clinic_name = Clinic.objects.get(Doctor_email=email, Clinic_Name=name)
        if clinic_name:
            current_doctor.Doctor_Clinic = clinic_name
            current_doctor.save()

    Data = {"current_doctor": current_doctor, 'error': error_message,
            'success': success}
    return render(request, "Doctor_admin_site/Clinic_profile.html", Data)


@Doctor_middleware
def updates_clinic_profile(request):
    error_message = None
    success = None
    lb = request.session.get('doctor_id')
    # print(lb)
    current_doctor = Doctors.objects.get(id=lb)
    if request.method == 'POST':
        data = request.POST
        name = data.get("username")
        phone = data.get("phone")
        Address = data.get("Address")
        C_phone = data.get("C_phone")
        Fee = data.get("Fee")
        Start_time = data.get('Start_time')
        End_time = data.get("End_time")
        ALL_DAYS = data.getlist('Days')
        Doctor_profile_img = request.FILES.get('image')

        Monday = False
        Tuesday = False
        Wednesday = False
        Thursday = False
        Friday = False
        Saturday = False
        Sunday = False

        if name:
            name = name.capitalize()
            current_doctor.Doctor_Clinic.Clinic_Name = name
            current_doctor.Doctor_Clinic.save()
            success = "Your Clinic Name Change Successfully"
        elif phone:
            if len(phone) < 10:
                error_message = " Password must be At-least 10 digit long without first '0' "
            else:
                current_doctor.Callnumber = phone
                current_doctor.save()
                success = "Your Phone number Change Successfully"
        elif Address:
            Address = Address.capitalize()
            current_doctor.Doctor_Clinic.Location = Address
            current_doctor.Doctor_Clinic.save()
            success = "Your Clinic Address Change Successfully"
        elif Fee:
            current_doctor.Doctor_Clinic.Doctor_Fee = Fee
            current_doctor.Doctor_Clinic.save()
            success = "Your Clinic Fee Change Successfully"
        elif Start_time:
            current_doctor.Doctor_Clinic.clinic_time_start = Start_time
            current_doctor.Doctor_Clinic.clinic_time_end = End_time
            current_doctor.Doctor_Clinic.save()
            success = "Your Clinic Timing Change Successfully"
        elif ALL_DAYS:
            for i in ALL_DAYS:
                if i == "Monday":
                    Monday = True
                elif i == "Tuesday":
                    Tuesday = True
                elif i == "Wednesday":
                    Wednesday = True
                elif i == "Thursday":
                    Thursday = True
                elif i == "Friday":
                    Friday = True
                elif i == "Saturday":
                    Saturday = True
                elif i == "Sunday":
                    Sunday = True
            current_doctor.Doctor_Clinic.Monday = Monday
            current_doctor.Doctor_Clinic.Tuesday = Tuesday
            current_doctor.Doctor_Clinic.Wednesday = Wednesday
            current_doctor.Doctor_Clinic.Thursday = Thursday
            current_doctor.Doctor_Clinic.Friday = Friday
            current_doctor.Doctor_Clinic.Saturday = Saturday
            current_doctor.Doctor_Clinic.Sunday = Sunday
            current_doctor.Doctor_Clinic.save()
            success = "Your Clinic Days Change Successfully"
        elif C_phone:
            current_doctor.Doctor_Clinic.Clinic_Number = C_phone
            current_doctor.Doctor_Clinic.save()
            success = "Your Clinic Phone number Change Successfully"
        elif Doctor_profile_img:
            current_doctor.img = Doctor_profile_img
            current_doctor.save()
            success = "Your Profile Image Change Successfully"

    current_doctor = Doctors.objects.get(id=lb)

    Data = {"current_doctor": current_doctor, 'error': error_message,
            'success': success}
    return render(request, "Doctor_admin_site/Clinic_profile.html", Data)


@Doctor_middleware
def New_Appointment_Requests(request):
    error_message = None
    success = None
    lb = request.session.get('doctor_id')

    Test_today = 0
    month = datetime.now().month
    year = datetime.now().year
    Appointments = Appointment.objects.filter(Doctor=lb, Status='Pending')
    P_name = None
    current_doctor = Doctors.objects.get(id=lb)

    if request.method == 'POST':
        data = request.POST
        name = data.get("name")
        P_name = data.get("P_name")
        app_id = data.get("id")
        Update_app = Appointment.objects.get(id=app_id)

        if name == "Accepted":
            Update_app.Status = "Accepted"
            Update_app.save()
            success = " Appointment is Accepted Successfully"
        else:
            Update_app.Status = "Cancel"
            Update_app.save()
            error_message = "Appointment is Canceled Successfully"

    Data = {"current_doctor": current_doctor,
            "Appointments": Appointments, "P_name": P_name,
            "success": success, "error_message": error_message}
    return render(request, 'Doctor_admin_site/New_Appointment_Requests.html', Data)


@Doctor_middleware
def Confirm_appointments(request):
    error_message = None
    success = None
    lb = request.session.get('doctor_id')

    Test_today = 0
    month = datetime.now().month
    year = datetime.now().year
    Appointments = Appointment.objects.filter(Doctor=lb, Status='Accepted')
    Appointments_today = Appointment.objects.filter(Doctor=lb, Status='Accepted', Appointment_date=datetime.now(), )

    P_name = None
    current_doctor = Doctors.objects.get(id=lb)

    if request.method == 'POST':
        data = request.POST
        name = data.get("name")
        P_name = data.get("P_name")
        Prescription = data.get("Prescription")
        Cancel_reason = data.get("Cancel_reason")
        app_id = data.get("id")
        Update_app = Appointment.objects.get(id=app_id)

        if name == "Accepted":
            Update_app.Status = "Completed"
            Update_app.Prescription = Prescription
            Update_app.save()
            success = " Prescription is Uploaded Successfully"
        else:
            Update_app.Status = "Cancel"
            Update_app.appointment_cancel_reason = Cancel_reason
            Update_app.save()
            error_message = "Appointment is Canceled Successfully"

    Data = {"current_doctor": current_doctor, "P_name": P_name,
            "Appointments": Appointments, "Appointments_today": Appointments_today,
            "success": success, "error_message": error_message}
    return render(request, 'Doctor_admin_site/View_confirm_appointments.html', Data)


@Doctor_middleware
def add_new_blog(request):
    error_message = None
    success = None
    lb = request.session.get('doctor_id')
    # print(lb)
    current_doctor = Doctors.objects.get(id=lb)
    if request.method == 'POST':
        Data = request.POST
        Img = request.FILES.get('blog_img')
        Health_blogs_issue = Data.get("Health_blogs_issue")
        Main_heading = Data.get("Main_heading")
        Blog_details = Data.get("Blog_details")

        Add_New_Blog = Health_blogs(Doctor=current_doctor, Health_blogs_issue=Health_blogs_issue,
                                    Main_heading=Main_heading, Health_blogs_Detail=Blog_details,
                                    blog_create_time=datetime.now(), img=Img)
        Add_New_Blog.save()
        success = "Your Health Blog added Successfully"
        print(Img, Health_blogs_issue, Main_heading, Blog_details)

    Data = {"current_doctor": current_doctor, 'error': error_message,
            'success': success}
    return render(request, "Doctor_admin_site/add_new_health_blog.html", Data)


@Doctor_middleware
def view_Doctor_blogs(request):
    error_message = None
    success = None
    lb = request.session.get('doctor_id')
    # print(lb)
    current_doctor = Doctors.objects.get(id=lb)
    Health_Blog = Health_blogs.objects.filter(Doctor=current_doctor)
    if request.method == 'POST':
        Data = request.POST
        name = Data.get("name")
        blog_id = Data.get("blog_id")
        print(name, blog_id)
        Health_Blog_exit = Health_blogs.objects.filter()
        if Health_Blog_exit:
            if name == "delete_blog":
                Health_Blog_delete = Health_blogs.objects.get(Doctor=current_doctor, id=blog_id)
                Health_Blog_delete.delete()
                success = "Your Health Blog Deleted Successfully"
            elif name == "update_blog":
                Img = request.FILES.get('blog_img')
                Health_blogs_issue = Data.get("Health_blogs_issue")
                Main_heading = Data.get("Main_heading")
                Blog_details = Data.get("Blog_details")
                Health_Blog_update = Health_blogs.objects.get(Doctor=current_doctor, id=blog_id)
                if Img:
                    Health_Blog_update.img = Img

                Health_Blog_update.Health_blogs_issue = Health_blogs_issue
                Health_Blog_update.Main_heading = Main_heading
                Health_Blog_update.Health_blogs_Detail = Blog_details
                Health_Blog_update.save()
                success = "Your Health Blog Updated Successfully"
                print(Img, Health_blogs_issue, Main_heading, Blog_details)
        else:
            error_message = "Health Blog is already Deleted."
    Data = {"current_doctor": current_doctor, 'error': error_message,
            'success': success, "Health_Blog": Health_Blog}
    return render(request, "Doctor_admin_site/View_all_your_blogs.html", Data)


@Doctor_middleware
def Update_health_blog(request):
    error_message = None
    success = None
    lb = request.session.get('doctor_id')
    # print(lb)
    current_doctor = Doctors.objects.get(id=lb)
    if request.method == 'POST':
        Data = request.POST
        name = Data.get("name")
        blog_id = Data.get("blog_id")
        Health_Blog_exit = Health_blogs.objects.filter(Doctor=current_doctor, id=blog_id)
        if Health_Blog_exit:
            if name == "Update_blog":
                Health_Blog = Health_blogs.objects.get(Doctor=current_doctor, id=blog_id)

    Data = {"current_doctor": current_doctor, 'error': error_message,
            'success': success, "Health_Blog": Health_Blog}
    return render(request, "Doctor_admin_site/Update_health_blog_form.html", Data)


def view_Full_Doctor_blogs(request, id):
    error_message = None
    success = None
    lb = request.session.get('doctor_id')
    # print(lb)
    current_doctor = Doctors.objects.get(id=lb)
    Health_Blog = Health_blogs.objects.filter(Doctor=current_doctor, id=id)
    Data = {"current_doctor": current_doctor, 'error': error_message,
            'success': success, "Health_Blog": Health_Blog}
    return render(request, "Doctor_admin_site/view_Full_Doctor_blogs.html", Data)


# ////////////////////////////Functions Related  Doctor Admin Dashboard+profile page END///////////////////////////

# ///////////////////////////////////////Forget Password Email Sent ////////////////////////////////////////////////////

def ChangePassword_doctor(request, token):
    context = {}

    try:
        profile_obj = Doctors.objects.get(forget_password_token=token)
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

                return redirect(f'/change-password_doctor/{token}/')

            if new_password != confirm_password:
                success = "both should  be equal."
                return redirect(f'/change-password_Lab/{token}/', {"success": success})

            user_obj = Doctors.objects.get(id=user_id)
            user_obj.password = new_password
            user_obj.save()
            user_obj = Doctors.objects.get(id=la)
            token = str(uuid.uuid4())
            profile_obj = Doctors.objects.get(email=user_obj.email)
            profile_obj.forget_password_token = token
            profile_obj.save()
            success_message = 'Your Password has been changed Now '
            return render(request, 'doctor_login.html', {'success': success_message})
        else:
            return render(request, 'change-password.html')


    except Exception as e:
        print(e)
    return render(request, 'Link_experiy.html', context)


def ForgetPassword_doctor(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            print(username)

            if not Doctors.objects.filter(email=username).first():
                messages.error(request, 'Not user found with this username.')
                return redirect('/forget-password_doctor/')

            user_obj = Doctors.objects.get(email=username)
            token = str(uuid.uuid4())
            print(token)
            profile_obj = Doctors.objects.get(email=username)
            print(profile_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail_doctor(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password_doctor/')



    except Exception as e:
        print(e)
    return render(request, 'forget-password.html')

# ///////////////////////////////////// Forget Password Email Sent End  ////////////////////////////////////////////////
