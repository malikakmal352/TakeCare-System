from django.core.mail import send_mail

from django.conf import settings


# ////////////////////////////////////////// Send Super Admin E-mails ////////////////////////////////
def send_forget_password_mail_Admin(email, token):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://takecaresystem.pythonanywhere.com/ChangePassword_Admin/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

# ////////////////////////////////////////// Send  Patients E-mails ////////////////////////////////
def send_forget_password_mail(email, token):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://takecaresystem.pythonanywhere.com/change-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

# ////////////////////////////////////////// Send Laboratory Admin E-mails ////////////////////////////////
def send_forget_password_mail_Lab(email, token):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://takecaresystem.pythonanywhere.com/change-password_Lab/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


# ////////////////////////////////////////// Send Doctor Admin E-mails ////////////////////////////////
def send_forget_password_mail_doctor(email, token):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://takecaresystem.pythonanywhere.com/change-password_doctor/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def Doctor_Request_Sent_mail_doctor(email, name):
    subject = 'Your Request Sent Successfully'
    message = f'Hi  {name}  \n\n, Your Request is Sent Successfully, You will be inform About your request is Accept or not through E-mail'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def Doctor_Request_Rejected_Sent_mail_doctor(email, Dname):
    subject = 'Your Request of join TakeCare Doctors Team'
    message = f'Hi {Dname}  \n\n, Sorry , Your Request of join over Doctor Team is not Accepted  \n\n ' \
              f' \n  If you Think this is Mistake then you can Contact Us on the following E-mail \n\n\t\t' \
              f'takecaresupporst033@gmail.com'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def Doctor_Request_Accepted_Sent_mail_doctor(email, Dname, token):
    subject = 'Your Request of join TakeCare Doctors Team'
    message = f'Hi Dr.{Dname}  \n\n, Your Request is Request is Accepted Sucessfully \n\n Now You part of over medical team.p' \
              f' \n  Please Click on this Link to Create a Password and then Login into You Account\n\n' \
              f' http://127.0.0.1:8000/Create_password_doctor/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

# ////////////////////////////////////////// Send Pharmacy Admin E-mails ////////////////////////////////


def send_forget_password_mail_Pharmacy(email, token):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://takecaresystem.pythonanywhere.com/change-password_Pharmacy/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def Pharmacy_Create_FirstPassword_Sent_mail_doctor(email, Dname, token):
    subject = 'Your Request of join TakeCare Pharmacy Team'
    message = f'Hi Dr.{Dname}  \n\n, Your Pharmacy is Add to Over Pharmacies Team Sucessfully \n\n' \
              f' Now You part of over medical team' \
              f' \n  Please Click on this Link to Create a Password and then Login into You Account\n\n' \
              f' http://takecaresystem.pythonanywhere.com/Create_password_Pharmacy/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


