from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Contact(models.Model):
    firstname= models.CharField(max_length=100, null=True)
    lastname= models.CharField(max_length=100, null=True)
    emailid= models.EmailField(null=True)
    subject= models.CharField(max_length=200, null=True)
    message= models.TextField(null=True)

class UserInformation(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    first_name= models.CharField(max_length=100, null=True)
    last_name= models.CharField(max_length=100, null=True)
    email= models.EmailField(null=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    datatype= models.CharField(max_length=9, blank=True)
    location_name= models.CharField(max_length=100, null=True)
    latitude= models.CharField(max_length=12, null=True)
    longitude= models.CharField(max_length=13, null=True)
    damage_reported= models.TextField(null=True)
    description= models.TextField(null=True)
    drought_condition= models.TextField(null=True)
    county_basin_withdrawal= models.CharField(max_length=100, null=True)
    surface_water_withdrawal_volume= models.IntegerField(max_length=3, null=True)
    ground_water_withdrawal_volume= models.IntegerField(max_length=3, null=True)
    ground_water_level= models.IntegerField(max_length=7, null=True)
    reported_use_by_sector= models.IntegerField(max_length=7, null=True)
    number_of_intakes= models.IntegerField(max_length=3, null=True)
    surface_water_withdrawal= models.IntegerField(max_length=3, null=True)
    ground_water_withdrawal= models.IntegerField(max_length=3, null=True)
    type_of_crop= models.CharField(max_length=50, null=True)
    total_acers_irrigated= models.IntegerField(max_length=7, null=True)
    total_acers_per_crop_irrigated= models.IntegerField(max_length=7, null=True)
    irrigation_type= models.CharField(max_length=100, null=True)
    power_requirements= models.TextField(max_length=7, null=True)
    irrigation_schedule_info= models.TextField(null=True)
    flood_condition= models.TextField(null=True)
    created_at= models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.first_name

class Document(models.Model):
    title=models.CharField(max_length=100, null=True)
    about=models.CharField(max_length=100, null=True)
    pdf= models.FileField(upload_to='pdfs/')
    image= models.ImageField(upload_to='images/', null=True, blank=True)


    def __str__(self):
        return self.title