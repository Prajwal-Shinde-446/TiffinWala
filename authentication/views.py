from django.shortcuts import render , redirect , HttpResponse
from authentication.Email_backend import Emailbackend
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from .models import Customuser 
import random
from django.core.mail import send_mail
from django.core.exceptions import ValidationError




def home(request):
    return render(request , "authentication/base1.html")



def login(request):
    if request.method == 'POST':
        user = Emailbackend.authenticate(request,
                                         username=request.POST.get('usermail'),
                                         password=request.POST.get('password'))
        
        if user != None:
            login(request,user)
            user_type = user.user_type

            if user_type == 'user':
                request.session['user_logged_in'] = True
                return redirect('/')  
            
            elif user_type == 'service':
                request.session['user_logged_in'] = True
                return redirect('/')  
                
            else:
                messages.error(request,'Email and password are invalid')
                return redirect('/')
        else:
                messages.error(request,'Email and password are invalid')
                return redirect('/')
    
    return render('authentication/login.html')
# Create your views here.


def Register(request):
    if request.method == 'POST':
        email = request.POST.get('usermail')
        name= request.POST.get('name')
        phone_no = request.POST.get('userphone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print("clear1")

        if password != confirm_password:
            print(type(phone_no))
            messages.error(request,'Passwords do not match!')
            return redirect('Register')

        
        elif Customuser.objects.filter(email=email).exists():
            messages.error(request,'user with this email already exists!')
            return redirect('Register')
        
        elif len(phone_no) != 10 :
            messages.error(request,'Enter a valid 10 digit phone no')
            return redirect('register_service')
        
        else:    
            try:
                user = Customuser.objects.create_user(email = email , password = password, name=name , phone = phone_no)

                user.save()
                print("clear2")
                user.user_type = 'user'
                user.name = name
                user.phone = phone_no
                
                user.save()



                otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
                user.email_otp = otp

                subject = 'Email Verification OTP'
                message = f'Hello! this is a confirmation mail, to activate your account please use the otp given below to verify your email account Your email verification OTP is: {otp}'
                from_email = 'viratshinde877@gmail.com'  # Set this to your email
                recipient_list = [user.email]

                send_mail(subject , message , from_email , recipient_list)

                return redirect('verify_otp' , user_id=user.id)

            except ValidationError as e:
                messages.error(request , str(e))
                return redirect('Register')
    else:

        return render(request,'authentication/base1.html')

def verify_otp(request , user_id):
    user = Customuser.objects.get(id=user_id)
    if request.method == 'POST':
        digit1 = request.POST['digit1']
        digit2 = request.POST['digit2']
        digit3 = request.POST['digit3']
        digit4 = request.POST['digit4']

        combined_otp = digit1+digit2+digit3+digit4

        if combined_otp == user.email_otp:
            user.email_verified=True
            user.save()
            login(request , user)
            return redirect('')
        
        else:
            messages.error(request,'invalid otp')
            return render(request,'authentication/otp_verification.html',{'user': user})

    
    return render(request ,'authentication/otp_verification.html',{'user': user})


        


        


        


