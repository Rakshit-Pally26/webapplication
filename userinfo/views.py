from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserInformation, Document, Contact
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm
import sys
from slacker import Slacker
import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.

from django.views.generic import View
from django.template.loader import get_template 
from django_project.utils import render_to_pdf 

def default_map(request):
    # TODO: move this token to Django settings from an environment variable
    # found in the Mapbox account settings and getting started instructions
    # see https://www.mapbox.com/account/ under the "Access tokens" section
    mapbox_access_token = 'pk.eyJ1IjoianBhbGx5IiwiYSI6ImNrYjl3dnNsczBpZTgzNW1kN3pud2VnamMifQ.HcBDAu7yMIcrgtKTedIhjQ'
    return render(request, 'default.html', 
                  { 'mapbox_access_token': mapbox_access_token })

def default_map1(request):
    # TODO: move this token to Django settings from an environment variable
    # found in the Mapbox account settings and getting started instructions
    # see https://www.mapbox.com/account/ under the "Access tokens" section
    mapbox_access_token = 'pk.eyJ1IjoianBhbGx5IiwiYSI6ImNrYjl3dnNsczBpZTgzNW1kN3pud2VnamMifQ.HcBDAu7yMIcrgtKTedIhjQ'
    return render(request, 'default1.html', 
                  { 'mapbox_access_token': mapbox_access_token })

def Generate(request, id):
    user= UserInformation.objects.get(id=id)
    template = get_template('pdf_template.html')
    context = {
        'FirstName' :  user.first_name , 
        'LastName' :  user.last_name, 
        'EmailID' :  user.email, 
        'PhoneNumber' :  user.phone_number,
        'Location' :  user.location_name, 
        'Latitude' :  user.latitude,
        'Longitude' :  user.longitude, 
        'DamageReported' :  user.damage_reported, 
        'Description' :  user.description, 
        'DroughtCondition' :  user.drought_condition, 
        'FloodCondition' :  user.flood_condition, 
        'CountBasinofwithdrawal' :  user.county_basin_withdrawal, 
        'Surfacewaterwithdrawalvolume' :  user.surface_water_withdrawal_volume, 
        'Groundwaterwithdrawalvolume' :  user.ground_water_withdrawal_volume,
        'Groundwaterlevel' :  user.ground_water_level,
        'Reportedusebysector' :  user.reported_use_by_sector, 
        'Numberofintakes' :  user.number_of_intakes, 
        'Surfacewaterwithdrawal' :  user.surface_water_withdrawal, 
        'Groundwaterwithdrawal' :  user.ground_water_withdrawal, 
        'Typeofcrop' :  user.type_of_crop, 
        'Totalacersirrigated' :  user.total_acers_irrigated, 
        'Totalacerspercropirrigated' :  user.total_acers_per_crop_irrigated, 
        'Irrigationtype' :  user.irrigation_type, 
        'Powerrequirementsandoperatingpressurerange' :  user.power_requirements, 
        'Irrigationscheduleinformation' :  user.irrigation_schedule_info, 
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf_template.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "User_%s.pdf" %("details")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def index(request):
    return render(request, "index.html", {'UserName': 'Donnie Sherier'})

def AddUser(request):
    return render(request, "add_user.html")

def drought_monitor(request):
    return render(request, "drought.html")

def ContactUs(request):
    return render(request, "contact.html")

def ContactInfo(request):
    print("Details Submitted")
    firstname= request.POST.get('firstname', False)
    lastname= request.POST.get('lastname', False)
    emailid= request.POST.get('emailid', False)
    subject= request.POST.get('subject', False)
    message= request.POST.get('message', False)
    slack=Slacker('xoxb-1141578750229-1174022059907-4mtT0KHkkKXLikpLAbgvYOg7')
    messages="integration with django web-application"
    message_attachments= [
        {
            "fallback": "This does not work",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "xoxb-1141578750229-1174022059907-4mtT0KHkkKXLikpLAbgvYOg7",
            "actions": [
                {
                    "name": "approveuser",
                    "text": "Approve",
                    "type": "button",
                    "value": firstname,
                },
                {
                    "name": "denyuser",
                    "text": "Deny",
                    "type": "button",
                    "value": firstname,
                }
            ]
        }    
    ]
    slack.chat.post_message('#aedas-message', "Approve User:\nUser: "+firstname+"\nEmail: "+emailid+"\nSubject: "+subject+" ?", attachments=message_attachments)
    user_contact= Contact(firstname=firstname, lastname=lastname, emailid=emailid, subject=subject, message=message)
    user_contact.save()
    return render(request, "contact.html")

@method_decorator(csrf_exempt)
def SlackMenu(request):
    jsonText= request.Post.get("payload", "NO PAYLOAD")
    jsondata= json.loads(jsonText)
    slackToken= str(jsondata["token"])
    print(slackToken)
    if slackToken != "PUapzCnf721752wInCLQ1gJH":
        return
    actionName= jsondata["actions"][0]["name"]
    actionValue= jsondata["actions"][0]["value"]

    if actionName == "approveuser":
        return HttpResponse("user approved!")
    
    if actionName == "denyuser":
        return HttpResponse("user denied!")
    return HttpResponse("No Action! "+actionName)



def AllUsers(request):
    all_users= UserInformation.objects.all()
    return render(request, "all_users.html", {'Users': all_users})

def upload(request):
    context={}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs= FileSystemStorage()
        name= fs.save(uploaded_file.name, uploaded_file)
        context['url']= fs.url(name)
    return render(request, "upload.html", context)

def document_list(request):
    documents = Document.objects.all()
    return render(request, 'document_list.html', {'documents': documents})

def document_upload(request):
    form = DocumentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        
        if form.is_valid():
            form.save()
            return redirect('document_list')
        else:
            form = DocumentForm()
    return render(request, 'document_upload.html', {'form':form})

def add_user_form_submission(request):
    print("The form is submitted")
    first_name= request.POST["first_name"]
    last_name= request.POST["last_name"]
    email= request.POST["email"]
    phone_number= request.POST["phone_number"]
    location_name= request.POST["location_name"]
    latitude= request.POST["latitude"]
    longitude= request.POST["longitude"]
    damage_reported= request.POST["damage_reported"]
    description= request.POST["description"]
    drought_condition= request.POST["drought_condition"]
    flood_condition= request.POST["flood_condition"]
    county_basin_withdrawal= request.POST["county_basin_withdrawal"]
    surface_water_withdrawal_volume= request.POST["surface_water_withdrawal_volume"]
    ground_water_withdrawal_volume= request.POST["ground_water_withdrawal_volume"]
    ground_water_level= request.POST["ground_water_level"]
    reported_use_by_sector= request.POST["reported_use_by_sector"]
    number_of_intakes= request.POST["number_of_intakes"]
    surface_water_withdrawal= request.POST["surface_water_withdrawal"]
    ground_water_withdrawal= request.POST["ground_water_withdrawal"]
    type_of_crop= request.POST["type_of_crop"]
    total_acers_irrigated= request.POST["total_acers_irrigated"]
    total_acers_per_crop_irrigated= request.POST["total_acers_per_crop_irrigated"]
    irrigation_type= request.POST["irrigation_type"]
    power_requirements= request.POST["power_requirements"]
    irrigation_schedule_info= request.POST["irrigation_schedule_info"]

    user_info= UserInformation(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, 
    location_name=location_name, latitude=latitude, longitude=longitude, damage_reported=damage_reported, 
    description=description, drought_condition=drought_condition, flood_condition=flood_condition,
    county_basin_withdrawal=county_basin_withdrawal,surface_water_withdrawal_volume=surface_water_withdrawal_volume,
    ground_water_withdrawal_volume=ground_water_withdrawal_volume, ground_water_level=ground_water_level,
    reported_use_by_sector=reported_use_by_sector, number_of_intakes=number_of_intakes, surface_water_withdrawal=surface_water_withdrawal,
    ground_water_withdrawal=ground_water_withdrawal,type_of_crop=type_of_crop,total_acers_irrigated=total_acers_irrigated,
    total_acers_per_crop_irrigated=total_acers_per_crop_irrigated, irrigation_type=irrigation_type,
    power_requirements=power_requirements,irrigation_schedule_info=irrigation_schedule_info)
    user_info.save()
    template = get_template('pdf_template.html')
    context = {
        'FirstName' :  first_name , 
        'LastName' :  last_name, 
        'EmailID' :  email, 
        'PhoneNumber' :  phone_number,
        'Location' :  location_name, 
        'Latitude' :  latitude,
        'Longitude' :  longitude, 
        'DamageReported' :  damage_reported, 
        'Description' :  description, 
        'DroughtCondition' :  drought_condition, 
        'FloodCondition' :  flood_condition, 
        'CountBasinofwithdrawal' :  county_basin_withdrawal, 
        'Surfacewaterwithdrawalvolume' :  surface_water_withdrawal_volume, 
        'Groundwaterwithdrawalvolume' :  ground_water_withdrawal_volume,
        'Groundwaterlevel' :  ground_water_level,
        'Reportedusebysector' :  reported_use_by_sector, 
        'Numberofintakes' :  number_of_intakes, 
        'Surfacewaterwithdrawal' :  surface_water_withdrawal, 
        'Groundwaterwithdrawal' :  ground_water_withdrawal, 
        'Typeofcrop' :  type_of_crop, 
        'Totalacersirrigated' :  total_acers_irrigated, 
        'Totalacerspercropirrigated' :  total_acers_per_crop_irrigated, 
        'Irrigationtype' :  irrigation_type, 
        'Powerrequirementsandoperatingpressurerange' :  power_requirements, 
        'Irrigationscheduleinformation' :  irrigation_schedule_info, 
        }
    html = template.render(context)
    pdf = render_to_pdf('pdf_template.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "User_%s.pdf" %("Details")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return render(request, "add_user.html")
