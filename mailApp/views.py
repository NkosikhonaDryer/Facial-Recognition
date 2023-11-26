#from asyncio.windows_events import NULL
import email
from email import message
from hashlib import new
from tracemalloc import DomainFilter
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from management.models import * 

# Create your views here.


def LectureActivationEmail(request, user, to_email,ModuleGroupId, newPassword,is_userExist):
    moduleGroup = get_object_or_404(ModuleGroup, pk = ModuleGroupId)
    
    
    mail_subject = "Group assigned."
    message = render_to_string("mailApp/new_lecture.html",{
        'is_userExist':is_userExist,
        'user':user,
        'newPassword':newPassword,
        'moduleGroup':moduleGroup,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'    
    })
    try:
        if send_mail(mail_subject,f"{message}"  ,'',[f'{to_email}'], fail_silently=False,
        ):
            pass
        # messages.success(request,f"Verification email sent to {to_email}, please verify to access your account.")
        else:
            print(message)
            messages.error(request, f"There was an error sending email, please ensure you enter the correct email")        
    except:
        messages.error(request, "Something went wrong while trying to send email please double check your internet connection, or email spelling")
        
def KeeperActivationEmail(request, user, to_email, newPassword):

    
    
    mail_subject = "Group assigned."
    message = render_to_string("mailApp/new_keeper.html",{
   
        'user':user,
        'newPassword':newPassword,
      
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'    
    })
    try:
        if send_mail(mail_subject,f"{message}"  ,'',[f'{to_email}'], fail_silently=False,
        ):
            pass
        # messages.success(request,f"Verification email sent to {to_email}, please verify to access your account.")
        else:
            print(message)
            messages.error(request, f"There was an error sending email, please ensure you enter the correct email")        
    except:
        messages.error(request, "Something went wrong while trying to send email please double check your internet connection, or email spelling")