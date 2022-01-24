from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import UserOTP, UserAgreement
from .otp_generator import generateOTP


def loginacc(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            username = email.split('@')[0]
            user = authenticate(username=username, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR, 'Incorrect details! Try again.')
                return render(request, 'account/loginacc.html')
        else:
            messages.add_message(request, messages.ERROR, 'Details not satisfied!')
            return render(request, 'account/loginacc.html')
    else:
        return render(request, 'account/loginacc.html')

def createacc(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        acc_detail_form = request.POST.get('form_check')

        # checking whether the form is otp form or create account detail form
        if acc_detail_form == 'True':
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            repassword = request.POST.get('repassword')
            agreement = request.POST.get('TAC')

            if repassword == password and len(password) >= 8 and len(firstname) >= 4 and len(lastname) >= 2 and email != None and agreement == 'True':
                # creating inactive user
                username = email.split('@')
                user = User.objects.create_user(username=username[0], email=email, password=password, first_name=firstname, last_name=lastname)
                user.is_active = False
                user.save()
                # generating and sending otp
                otp = generateOTP()
                userotp = UserOTP(username=username[0], otp=otp)
                userotp.save()
                send_mail(
                    'Tenicons Account Verification',
                    f'your verification otp is {otp} and is valid for 1 min.',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )
                # rendering otp html page
                context = {
                    'form': False,
                    'form_title': 'Please Enter the OTP',
                    'form_message': f'Enter OTP sent to email {email} and your username {username[0]}',
                    'username': username[0],
                    'email': email
                }
                return render(request, 'account/createacc.html', context)
            else:
                # rendering error message
                messages.add_message(request, messages.ERROR, 'Try again! It\'s failed')
                context = {
                    'form': True,
                    'form_title': 'create account',
                    'form_message': 'Please Enter the valid details',
                    'username': '',
                    'email': ''
                }
                return render(request, 'account/createacc.html', context)
        else:
            #verifing otp
            entered_otp = request.POST.get('otp')
            username = request.POST.get('username')

            try:
                userotp = UserOTP.objects.get(username=username)
                generated_otp = userotp.otp

                if str(generated_otp) == entered_otp:
                    userotp.delete()

                    # activating user
                    user = User.objects.get(username=username)
                    user.is_active = True
                    user.save()

                    # accepting user agreement (Terms and conditions)
                    agree = UserAgreement(user=user, agreement=True)
                    agree.save()

                    return redirect('loginacc')
                else:
                    return HttpResponse('invalid otp')
            except:
                return HttpResponse('Session ended')
    else:
        context = {
            'form': True,
            'form_title': 'create account',
            'form_message': 'Enter the details to create account',
            'username': '',
            'email': ''
        }
        return render(request, 'account/createacc.html', context)

# API
def changeotpstate(request):
    try:
        username = request.POST.get('username')
        userotp = UserOTP.objects.get(username=username)
        userotp.delete()
        user = User.objects.get(username=username)
        user.delete()
        return HttpResponse('done')
    except:
        return HttpResponse('invalid')

# API
def sendotp(request):
    try:
        username = request.POST.get('username')
        email = request.POST.get('email')
        otp = generateOTP()
        userotp = UserOTP.objects.get(username=username)
        userotp.otp = otp
        userotp.save()
        send_mail(
            'Tenicons Account Verification',
            f'your verification otp is {otp} and is valid for 1 min.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        return HttpResponse('done')
    except:
        return HttpResponse('invalid')

def logoutacc(request):
    if request.user.is_authenticated:
        logout(request=request)
        return render(request, 'account/logoutacc.html')
    else:
        return redirect('home')