from typing import NoReturn
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from mysite.models import agent ,farmer,transaction
from django.contrib.auth.decorators import login_required

from mysite import utils
from datetime import date
from mysite.sendsms import send_msg
from django.contrib.auth import authenticate,login,logout

# Create your views here.
@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))

def user_login(request):

    if request.method == 'POST':
      username =  request.POST.get('username')
      password = request.POST.get('password')
      print(username,password)

      user = authenticate(username=username,password=password)
      print("this is user data")
      print(user)

      if user:
          if user.is_active:


            login(request,user)
            return HttpResponseRedirect(reverse('homepage'))
    return render(request,'login.html')


@login_required(login_url='login')
def homepage(request):
    farmers_obj = farmer.objects.all() 
    total_amount = 0
    total_amount_returned =0
    for a in farmers_obj:
        total_amount =int(a.total_balance) + int(total_amount)
        total_amount_returned=int(a.returned) + int(total_amount_returned)

    remaning_amount = total_amount - total_amount_returned
    return render(request,'home.html',{'total_amount':total_amount,'total_amount_returned':total_amount_returned,'remaning_amount':remaning_amount})


@login_required(login_url='login')
def farmerpage(request):
    agent_obj = agent.objects.all()
    farmer_obj =farmer.objects.all()
    if request.method == 'POST' and 'form1' in request.POST:
        print(request.POST)
        name = request.POST.get('name')
        agent_name =request.POST.get('anmae')
        phone_number = request.POST.get('phone')
        quantity = request.POST.get('quantity')
        rate = request.POST.get('rate')
        total_balance = float(rate) * float(quantity)
        agentname =agent.objects.get(name =agent_name)
        returned = 0
        print(agentname)
        print(name,agent_name,phone_number,quantity,rate,total_balance)
        save = farmer.objects.create(name=name,agent=agentname,phone_number =phone_number,total_balance =total_balance,returned=returned,quantity=quantity,rate =rate)
        return HttpResponse("FARMER ADDED")

    if request.method == 'POST' and 'form2' in request.POST:
        farmer_name = request.POST.get('fname')
        farmer_delete = farmer.objects.get(name =farmer_name)
        farmer_delete.delete()
        return HttpResponse("FARMER DELETED ")

    return render(request,'farmer.html',{'data':agent_obj,'farmerdata':farmer_obj})


@login_required(login_url='login')

def agentpage(request):
    global pdfdata


    agent_obj = agent.objects.all()

    if request.method == 'POST' and 'form1' in request.POST:
        print(request.POST)
        name = request.POST.get('agent')
        phone_number = request.POST.get('number')

        if name =='' or phone_number == None:
            HttpResponse("Fields cant be empty")

        
        elif len(phone_number)>10:
            return HttpResponse("Enter Correct Phone Number")
        else:
            save = agent.objects.create(name =name,phone_number =phone_number)
            return HttpResponse("AGENT ADDED")

    if request.method == 'POST' and 'form2' in request.POST:
        agent_name = request.POST.get('aname')
        agent_delete = agent.objects.get(name = agent_name)
        agent_delete.delete()
        return HttpResponse("AGENT DELETED")

    if request.method == 'POST' and 'displayfarmer' in request.POST:

        agent_name_= request.POST.get('anamedisplay')
        farmer_obj =farmerunderagent(request,agent_name_)
        total_amount =0
        total_amount_returend = 0
        for a in farmer_obj:
            total_amount = int(a.total_balance) + int(total_amount)
            total_amount_returend = int(a.returned) + int(total_amount_returend)
        remaining_amount = int(total_amount) - int(total_amount_returend)
        
        pdfdata = {'data':farmer_obj,'agentname':agent_name_,'total_amount':total_amount,'total_amount_returned':total_amount_returend,'remaining_amount':remaining_amount}

        return render(request,'farmerunderagent.html',{'data':farmer_obj,'agentname':agent_name_,'total_amount':total_amount,'total_amount_returned':total_amount_returend,'remaining_amount':remaining_amount})

    return render(request,'agent.html',{"data":agent_obj})


@login_required(login_url='login')

def transactionpage(request):

    data = farmer.objects.all()
    transaction_obj = transaction.objects.all()


    if request.method == 'POST' and 'pay' in request.POST:
        farmer_name = request.POST.get('name')
        amount = request.POST.get('amount')
        remark = request.POST.get('remark')
        datenow = date.today()
        farmername = farmer.objects.get(name=farmer_name)

        farmeramountaddition = int(farmername.returned) + int(amount)
        if farmeramountaddition > farmername.total_balance:
            return HttpResponse("RETURUNG AMOUNT IS GREATER THAN TOTAL AMOUNT")
        else:
            remaining =int(farmername.total_balance) -    int(farmeramountaddition) 
            farmername.returned = farmeramountaddition
            save = transaction.objects.create(name =farmername,paid =amount,remark=remark,date=datenow)
            farmername.save()
            sms = "Hello, {} You Have Deposited Rs{} . Your Remaining Amount is {} Rs".format(farmer_name,amount,remaining) 
            send_msg(sms,farmername.phone_number)
            print("msg send")
        


        

        return HttpResponse("TRANSACTION ADDED")

    if request.method =='POST' and 'displaytran' in request.POST:
        farmer_name = request.POST.get('fnamedisplay')
        farmer_obj = farmer.objects.get(name =farmer_name)
        transaction_obj = transaction.objects.all().filter(name =farmer_obj)
        print(farmer_obj.total_balance)
        remaining_amount = int(farmer_obj.total_balance) - int(farmer_obj.returned)
        return render(request,'farmersalltransactions.html',{'data':transaction_obj,'total_amount':farmer_obj.total_balance,'total_amount_returned':farmer_obj.returned,'remaining_amount':remaining_amount})



    return render(request,'transaction.html',{'data':data,'transactiondata':transaction_obj})




@login_required(login_url='login')

def farmerunderagent(request,name):
    agent_obj = agent.objects.get(name =name)
    farmer_obj = farmer.objects.all().filter(agent =agent_obj)
    # print(farmer_obj)
    print(farmer_obj)
        
        
    return (farmer_obj)
    
@login_required(login_url='login')

def downloadpdf(request):

    print("hey")
    print(pdfdata)
    pdf = utils.render_to_pdf('pdf.html',pdfdata)
    return HttpResponse(pdf, content_type='application/pdf')
