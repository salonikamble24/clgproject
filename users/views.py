from cgitb import html
from email import message
import re
import email
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate


cement_bag = 0
sand_bag = 0
aggregate_bag = 0 
steel_qty = 0
total_bricks = 0
metal_sheet = 0
estimated_cost = 0

def home(request):
    return render(request=request, template_name='homepage.html')

def about_us(request):
    return render(request=request, template_name='about_us.html')

def user_reg(request):
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
            user_type = 'user'
        )


        if password != confirm_password:
            messages.error(request, 'password doesnt matched')
            return redirect('user_reg')
        
        if user:
            user.set_password(password)
            user.save()
            return redirect('user_login')
        
        else:
            messages.error(request, "something went wrong")
        
    return render(request=request, template_name='user_reg.html')

def user_login(request):
    
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user is not None:
            return redirect('/user/firstpage/')
        else:
            messages.error(request,'User not found please register')
            return redirect('user_login')
    return render(request=request, template_name='user_login.html')

def firstpage(request):
    return render(request=request, template_name='firstpage.html')

def estimate(request):
    if  request.method == "POST":
        print(request.POST)
        Rooms = request.POST.get('Rooms', None)
        Length = request.POST.get('Length', None)
        Breadth = request.POST.get('Breadth', None)
        soil_Type = request.POST.get('soil_Type', None)
        roofing = request.POST.get('roofing', None)
        arr = {}
        for i in range(0,int(Rooms)):
            h_key = 'h_'+str(i) 
            l_key = 'l_'+str(i)
            print(h_key,l_key)
            arr[i]={
                "L":request.POST[h_key],
                "H":request.POST[l_key]
            }
        print(request.POST)
        calculateEstimate(Rooms,Length,Breadth,soil_Type,arr,roofing)
        return redirect('estimatedcost')
    print("get req")
     
    return render(request=request, template_name='estimate.html')

def tender(request):
    return render(request=request, template_name='tender.html')


def calculateEstimate(no_of_rooms,Length,Breadth,soil_type,rooms_desc,roofing):
    print(f"""
            rooms_count : {no_of_rooms} \n built_length : {Length} \n built_breadth : {Breadth} \n soil_type : {soil_type} \n rooms desc : {rooms_desc}
            roofing : {roofing}
    """)
    global cement_bag
    global sand_bag 
    global aggregate_bag  
    global steel_qty 
    global total_bricks 
    global metal_sheet
    global estimated_cost 
    #area_length=input("Enter length of area:")
    area_length=int(Length)
    #area_breadth=input("Enter breadth of area:")
    area_breadth=int(Breadth)
    #soil_type=int(input("Enter the type of soil \n Enter 1 for Black Hard stone \n Enter 2 for Hard Rock\n Enter 3 for Black Soil\n Enter 4 for Murrum\n Enter 5 for Lime Sand Stone\n "))
    if(soil_type=="Black Hard Stone"):
        soil_type=1
    if(soil_type=="Hard Rock"):
        soil_type=2
    if(soil_type=="Black Soil"):
        soil_type=3
    if(soil_type=="Murrum"):
        soil_type=4
    if(soil_type=="Lime Sand Stone"):
        soil_type=5
    #print(" Soil Type ", soil_type)
    if(roofing=="RCC"):
        roofing=1
    if(roofing=="Metal Sheet"):
        roofing=2
    
   # roofing=int(input("Enter type of roofing: Enter 1 for R.C.c \n Enter 2 for Metal sheet:"))
    built_up_area=area_length*area_breadth
    no_of_rooms=int(no_of_rooms)
    print(built_up_area)    
    def p_c_c_in_fdn(c, t):
        global cement_bag
        global sand_bag
        global aggregate_bag
        len=0
        qty=0
        len= c-0.4*t
        qty=len*0.5*0.20
        #print("Quantity of P.C.C.in foundation {0}".format(qty))
        cem=(qty*1.30)/7
        cem_bags=cem/0.035
        sand_bags=2*cem_bags
        aggre_bags=4*cem_bags
        cement_bag = cement_bag + cem_bags
        sand_bag=sand_bag+sand_bags
        aggregate_bag=aggregate_bag+aggre_bags
        #print(cem_bags,sand_bags,aggre_bags)
    
    def brick_mas_in_fdn(c, t, s):
        global cement_bag
        global sand_bag
        qty_first_footing = 0
        qty_second_footing = 0
        qty_third_footing,total_qty = 0, 0
        first_footing_len,second_footing_len,third_footing_len = 0, 0, 0
        if((s == 1) or (s == 2)):
            first_footing_len=c-(0.5/2)*t
            second_footing_len=c-(0.4/2)*t
            third_footing_len=c-(0.3/2)*t
            qty_first_footing=first_footing_len*0.50*0.30
            qty_second_footing=second_footing_len*0.40*0.30
            qty_third_footing=third_footing_len*0.30*0.65
            total_qty=qty_first_footing+qty_second_footing
            print("Quantity of brick masonaary in foundation {0}".format(total_qty))

        elif((s==5) or (s==3)):
            first_footing_len=c-(0.5/2)*t
            second_footing_len=c-(0.4/2)*t
            third_footing_len=c-(0.3/2)*t
            qty_first_footing=first_footing_len*0.50*0.50
            qty_second_footing=second_footing_len*0.40*0.30
            qty_third_footing=third_footing_len*0.30*0.65
            total_qty=qty_first_footing+qty_second_footing
            print("Quantity of brick masonaary in foundation {0}".format(total_qty))
  
        elif(s==4):
            first_footing_len=c-(0.5/2)*t
            second_footing_len=c-(0.4/2)*t
            third_footing_len=c-(0.3/2)*t
            qty_first_footing=first_footing_len*0.50*0.40
            qty_second_footing=second_footing_len*0.40*0.30
            qty_third_footing=third_footing_len*0.30*0.40
            total_qty=qty_first_footing+qty_second_footing
            print("Quantity of brick masonaary in foundation {0}".format(total_qty))

            morter=(total_qty*40/100)
            cem2=morter/7
            cem_bags2=cem2/0.035
            sand_bags2=6*cem_bags2
            cement_bag=cement_bag+cem_bags2
            sand_bag=sand_bag+sand_bags2
    
    def earth_filling(list_len, list_bre, k, s):
        qty, total_qty = 0, 0
        temp1, temp2 = 0, 0 
        #print("k ",k)
   
        if(s<=2):
            #print("s ",s)
         
            for l in range(k):
                qty=list_len[l]*(list_bre[l])*0.55+(3*1.70*0.55)+(1.3*1.1*0.55)
                #print("list_len[l] =",list_len[l])
                total_qty=total_qty+qty
        #print("Earth filling: {0}".format(total_qty))

    def d_p_c_at_plith(c, t):
        global cement_bag
        global sand_bag
        qty, len = 0,0
        len=c-0.2*t
        qty=len*0.4
        print(len)
        print("Quantity D.P.C at plinth:{0}".format(qty))
        morter=qty*30/100
        cement=morter/7
        cem_bags5=cement/0.035
        sand_bags5=6*cem_bags5
        cement_bag=cement_bag+cem_bags5
        sand_bag=sand_bag+sand_bags5
    
    def brick_mason_in_ss(c,t):
        global cement_bag
        global sand_bag
        global total_bricks
        qty,len,total_qty=0,0,0
        len=c-0.15*t
        qty=len*0.30*3
        total_qty=qty-(qty*20/100)
        print("Quantity of brick masonry is super structure:{0}".format(total_qty))
        morter=(total_qty*30/100)
        cement=morter/7
        cem_bags3=cement/0.035
        sand_bags3=6*cem_bags3
        no_of_bricks=(total_qty*60/100)/0.001
        cement_bag=cement_bag+cem_bags3
        sand_bag=sand_bag+sand_bags3
        total_bricks=total_bricks+no_of_bricks
    
    def roofing_qty(arraylen, arraybre, k,r):
        global cement_bag
        global sand_bag
        global aggregate_bag
        global steel_qty
        global metal_sheet
        qty,total_qty=0,0
        for l in range(k-1):
            qty = arraylen[l]*(arraybre[l])
            total_qty=total_qty+qty
        #print("Total roofing qty is {0}".format(((total_qty))))
        if(r==1):
            print("Total roofing qty is {0}".format(((total_qty))*0.10))
            morter4=1.40*(((total_qty))*0.10)
            cem=morter4/7
            cem_bags4=cem/0.035
            sand_bags4=2*cem_bags4
            aggre_bags4=4*cem_bags4
            steel=(((total_qty))*0.10)*1/100
            cement_bag=cement_bag+cem_bags4
            sand_bag=sand_bag+sand_bags4
            aggregate_bag=aggregate_bag+aggre_bags4
            steel_qty=steel_qty+steel
        if(r==2): 
            metal_sheet=metal_sheet+total_qty
    


    list_len=[10]
    list_bre=[10]
    for i in range(0,no_of_rooms):
        #list_len[i]=int(input("Enter length of room"+str(i+1)+":"))
        #list_bre[i]=int(input("Enter breadth of room"+str(i+1)+":"))
        #print("Enter length of room",i+1)
        room_length=int(rooms_desc[i].get("L"))
        list_len.append(room_length)
        #print("Enter breadth of room",i+1)
        room_breadth=int(rooms_desc[i].get("H"))
        list_bre.append(room_breadth)
        i=i+1



    if(no_of_rooms==1):
        horizontal_length=(((2*list_len[0])+3.30+0.60+2))
        vertical_length=(((2*list_bre[0])+0.60+0.55+(3.10*2)))
        centre_line_length=(horizontal_length+vertical_length)-30
        #print(centre_line_length)
        t_junction=3
 
    elif(no_of_rooms==2):
        horizontal_length=((2*list_len[0])+(2*list_len[1])+3.30+0.60+3)
        vertical_length=((2*list_bre[0])+list_bre[1]+0.60+0.55+(2*3.10))
        centre_line_length=(horizontal_length+vertical_length)-27
        #print(centre_line_length)
        t_junction=5

    elif(no_of_rooms==3):
        horizontal_length=((2*list_len[0])+(2*list_len[1])+list_len[2]+3.30+1.80)
        vertical_length=((2*list_bre[0])+0.55+3.15+2.8+list_bre[1]+(2*list_bre[2]))
        centre_line_length=(horizontal_length+vertical_length)-25
        #print(centre_line_length)
        t_junction=10

    elif(no_of_rooms==4):
        horizontal_length=((2*list_len[0])+(2*list_len[1])+list_len[2]+list_len[3]+3.30+2.10)
        vertical_length=((2*list_bre[0])+list_bre[1]+(2*list_bre[2])+list_bre[3]+(2*3.10)+0.55+0.60)
        centre_line_length=(horizontal_length+vertical_length)-26
        #print(centre_line_length)
        t_junction=7     

    elif(no_of_rooms==5):
        horizontal_length=((2*list_len[0])+(2*list_len[1])+list_len[2]+list_len[3]+list_len[4]+3.30+2.10)
        vertical_length=((2*list_bre[0])+list_bre[1]+(2*list_bre[2])+list_bre[3]+(2*list_bre[4])+3.30+0.55+1.20)
        centre_line_length=(horizontal_length+vertical_length)-26
        #print(centre_line_length)
        t_junction=12

    elif(no_of_rooms==6):
        horizontal_length=((2*list_len[0])+(2*list_len[1])+list_len[2]+list_len[3]+list_len[4]+list_len[5]+3.30+2.70)
        vertical_length=((2*list_bre[0])+list_bre[1]+(2*list_bre[2])+list_bre[3]+(2*list_bre[4])+list_bre[5]+(2*3.10)+0.55+0.66)
        centre_line_length=(horizontal_length+vertical_length)-30
        #print(centre_line_length)
        t_junction=13

    elif(no_of_rooms==7):
        horizontal_length=((2*list_len[0])+(2*list_len[1])+list_len[2]+list_len[3]+list_len[4]+list_len[5]+list_len[6]+3.30+2.10)
        vertical_length=((2*list_bre[0])+list_bre[1]+(2*list_bre[2])+list_bre[3]+(2*list_bre[4])+list_bre[5]+(2*list_bre[6])+(3.10+0.55+0.66))
        centre_line_length=(horizontal_length+vertical_length)-30
        #print(centre_line_length)
        t_junction=15

    elif(no_of_rooms==8):
        horizontal_length=((2*list_len[0])+(2*list_len[1])+list_len[2]+list_len[3]+list_len[4]+list_len[5]+list_len[6]+list_len[7]+3.30+2.70)
        vertical_length=((2*list_bre[0])+list_bre[1]+(2*list_bre[2])+list_bre[3]+(2*list_bre[4])+list_bre[5]+(2*list_bre[6])+list_bre[7]+(2*3.10)+0.55+0.66)
        centre_line_length=(horizontal_length+vertical_length)-30
        print(centre_line_length)
        t_junction=16

    elif(no_of_rooms==9):
        horizontal_length=((2*list_len[0])+(2*list_len[1])+list_len[2]+list_len[3]+list_len[4]+list_len[5]+list_len[6]+list_len[7]+list_len[8]+3.30+2.10)
        vertical_length=((2*list_bre[0])+list_bre[1]+(2*list_bre[2])+list_bre[3]+(2*list_bre[4])+list_bre[5]+(2*list_bre[6])+list_bre[7]+(2*list_bre[8])+(3.10+0.55+0.66))
        centre_line_length=(horizontal_length+vertical_length)-30
        #print(centre_line_length)
        t_junction=17

    elif(no_of_rooms==10):
        horizontal_length=((2*list_len[0])+(2*list_len[1])+list_len[2]+list_len[3]+list_len[4]+list_len[5]+list_len[6]+list_len[7]+list_len[8]+list_len[9]+3.30+2.70)
        vertical_length=((2*list_bre[0])+list_bre[1]+(2*list_bre[2])+list_bre[3]+(2*list_bre[4])+list_bre[5]+(2*list_bre[6])+list_bre[7]+(2*list_bre[8])+list_bre[9]+(2*3.10)+0.55+0.66)
        centre_line_length=(horizontal_length+vertical_length)-30
        #print(centre_line_length)
        t_junction=18

    p_c_c_in_fdn(centre_line_length , t_junction)
    brick_mas_in_fdn(centre_line_length , t_junction,soil_type)
    #earth_filling(list_len,list_bre,no_of_rooms,soil_type)
    d_p_c_at_plith(centre_line_length,t_junction)
    brick_mason_in_ss(centre_line_length,t_junction)
    roofing_qty(list_len,list_bre,no_of_rooms,roofing)
    #plastering(list_len,list_bre,no_of_rooms)
    cement_bag=int(cement_bag)
    print("Cement Bags final:",cement_bag)
    sand_bag=int(sand_bag)
    print("Sand Bags:",sand_bag)
    aggregate_bag=int(aggregate_bag)
    print("Aggregates:",aggregate_bag)

    #print("Steel:",steel_qty)
    total_bricks=int(total_bricks)
    print("bricks:",total_bricks)


    if(roofing==1):
        estimated_cost=(cement_bag*300)+(sand_bag*100)+(aggregate_bag*2800)+(steel_qty*7850*60)+(total_bricks*8)
        print(estimated_cost)

    elif(roofing==2):
        print("Metal Sheet:",metal_sheet)
        estimated_cost=(cement_bag*300)+(sand_bag*100)+(aggregate_bag*2800)+(total_bricks*8)+(metal_sheet*300)
        print(estimated_cost)

    

def estimatedcost(request):
    #c_bag = request.POST[cement_bag]
    #s_bag = request.POST[sand_bag]
    #a_bag = request.POST["aggregate_bag"] 
    #t_bricks = request.POST["total_bricks"] 
    #e_cost = request.POST["estimated_cost"]
    dict1 = {
        'c_bag': cement_bag,
        's_bag': sand_bag,
        'a_bag': aggregate_bag,
        't_bricks': total_bricks,
        'e_cost': estimated_cost
    }
    print(request.POST) 
    return render(request, 'estimatedcost.html',dict1)

    




    







