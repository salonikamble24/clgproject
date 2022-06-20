from cgitb import html
from email import message
import re
import email
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from users.models import User

from django.contrib.auth import authenticate


def contractor_reg(request):
    if request.method=='POST':
        print("------------------------------------------------")
        print(request.POST)
        firstname= request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        area_code=request.POST['area_code']
        contact_no=request.POST['contact_no']
        username=request.POST['username']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        user = User(
            first_name = firstname,
            last_name = lastname,
            email = email,
            username = username,
            contact_no = contact_no,
            area_code = area_code,
            user_type = "contractor",
        )

        

        if password != confirm_password:
            messages.error(request, 'password doesnt matched')
            return redirect('contractor_reg')
        
        if user:
            user.set_password(password)
            user.save()
            return redirect('contractor_login')
        
        else:
            messages.error(request, "something went wrong")
        
    return render(request=request, template_name='contractor_reg.html')

def contractor_login(request):
    
   if request.method == 'POST':
        print("Inside Login post ----------------------",request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(username = username, password = password)

        if user is not None:
            return redirect('/contractor/firstpage/')
        else:
            messages.error(request,'User not found please register')
            return redirect('contractor_login')
   return render(request=request, template_name='contractor_login.html')

def cfirstpage(request):
    return render(request=request, template_name='cfirstpage.html')
