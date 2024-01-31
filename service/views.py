from django.shortcuts import render , redirect , HttpResponse
from django.contrib import messages 
import random
from authentication.models import Customuser
from django.core.exceptions import ValidationError
from .models import Service
from django.core.mail import send_mail


def register_service(request):

    if request.method == 'POST':
        name= request.POST.get('name')
        phone_no = request.POST.get('userphone')
        address = request.POST.get('address')
        postal_code = request.POST.get('zip_code')
       

        # if password != confirm_password:
        #     messages.error("Passwords do not match!")
        #     return redirect('register_service')
        
        # elif Customuser.objects.filter(email=email).exists() :
        #     messages.error(request,'user with this email already exists!')
        #     return redirect('register_service')
            
        if len(phone_no) != 10 :
            messages.error(request,'Enter a valid 10 digit phone no')
            return redirect('register_service')
        
        elif len(postal_code) != 6 :
            messages.error(request,'Enter a valid postal code')
            return redirect('register_service')
        
        else:
            try:
                service = Service.objects.create(name = name , phone_no = phone_no)

                service.save()

                service.user_type = 'service'
                service.name = name
                service.address = address
                service.phone = phone_no
                service.pin_code = postal_code

                service.save()

                otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
                service.email_otp = otp

                subject = 'Email Verification OTP'
                message = f'Hello! this is a confirmation mail, to activate your account please use the otp given below to verify your email account Your email verification OTP is: {otp}'
                from_email = 'viratshinde877@gmail.com'
                recipient_list = [service.email]

                send_mail(subject , message , from_email , recipient_list)

                return redirect('verify_otp' , user_id=service.id)

            except ValidationError as e:
                messages.error(request , str(e))
                return redirect('register_service')
            
    else:
        return render(request , 'authentication/register_service.html')
