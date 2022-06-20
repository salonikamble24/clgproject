from cgitb import html
from email import message
import re
import email
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from vendor.models import Vendor
from users.models import User

from django.contrib.auth import authenticate, login, logout

from vendor.models import Vendor


def vendor_reg(request):
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
            user_type = "vendor",
        )

        

        if password != confirm_password:
            messages.error(request, 'password doesnt matched')
            return redirect('vendor_reg')
        
        if user:
            user.set_password(password)
            user.save()
            return redirect('vendor_login')
        
        else:
            messages.error(request, "something went wrong")
        
    return render(request=request, template_name='vendor_reg.html')

def vendor_login(request):
    
    if request.method == 'POST':
        print("Inside Login post ----------------------",request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request,user)
            return redirect('/vendor/firstpage/')
        else:
            messages.error(request,'User not found please register')
            return redirect('vendor_login')
    return render(request=request, template_name='vendor_login.html')

def vfirstpage(request):
    if request.method=='POST':
        print("------------------------------------------------")
        print(request.POST)
        print(request.user.id)
        user=User.objects.get(id=request.user.id)
        company_name=request.POST['company_name']
        company_address=request.POST['company_address']
        material_name=request.POST['material_name']
        phone_no=request.POST['phone_no']
    
        temp_vendor=Vendor(user=user,company_name=company_name,company_address=company_address,material_name=material_name,phone_no=phone_no)
        temp_vendor.save()
        logout(request)
        return redirect('home')

    return render(request=request, template_name='vfirstpage.html')
