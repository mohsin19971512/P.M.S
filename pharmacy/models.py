from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.cache import cache 
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now



class Medicine(models.Model):
    MEDICINE_NAME = models.CharField(verbose_name="Medicine Name",max_length=500)
    SELLING_PRICE = models.IntegerField(verbose_name="Selling Price")
    EXPIRE_DATE = models.DateField(verbose_name="Expire Date")
    MANUFACTURE_NAME = models.CharField(verbose_name="Manufacture Name",max_length=500)
    UNITARY_PRICE = models.IntegerField(verbose_name="Unitary Price")
    QUANTITY = models.IntegerField(verbose_name="Quantity")
    DISCOUNT = models.IntegerField(verbose_name="Dicount")
    def __str__(self) -> str:
        return self.MANUFACTURE_NAME




class Employee(models.Model):
    EMPLOYEE_NAME = models.CharField(verbose_name="Employee Name",max_length=500) 
    ADDRESS = models.CharField(verbose_name="Adress",max_length=500)
    PHONE = models.CharField(verbose_name="phone number",max_length=13)
    USERNAME = models.CharField(verbose_name="Username",max_length=200)
    PASSWORD = models.CharField(verbose_name="Password",max_length=200)
    MEDICINE_SOLD = models.CharField(verbose_name="Medicine Sold",max_length=500)
    SELLING_DATE = models.DateField(verbose_name="Selling Date")
    def __str__(self) -> str:
        return self.EMPLOYEE_NAME

class Customer(models.Model):
    CUSTOMER_NAME = models.CharField(verbose_name="Customer Name",max_length=500)
    ADDRESS = models.CharField(verbose_name="Adress",max_length=500)
    PRODUCT = models.CharField(verbose_name="Product",max_length=500)
    COST = models.IntegerField(verbose_name="Cost")
    PHONE = models.CharField(verbose_name="Phone Number",max_length=13)
    def __str__(self) -> str:
        return self.CUSTOMER_NAME

class Store(models.Model):
    STORE_NAME = models.CharField(verbose_name="Store Name",max_length=500)
    PLACE = models.CharField(verbose_name="Place",max_length=500)
    MANAGERS_STORE = models.CharField(verbose_name="Manager Store",max_length=500)
    def __str__(self) -> str:
        return self.STORE_NAME


class Location(models.Model):
    SHELF = models.IntegerField(verbose_name="Shelf Number")
    CLASSIFICATION =  models.CharField(verbose_name="classification",max_length=500)
    MEDICINE_NAME =  models.CharField(verbose_name="Medicine Name",max_length=500)

    def __str__(self) -> str:
        return self.CLASSIFICATION


class CustomUser(AbstractUser):
    user_type_data = ((1, "AdminHOD"), (2, "Pharmacist"), (3, "Doctor"), (4, "PharmacyClerk"),(5, "Patients"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)




class AdminHOD(models.Model):
    gender_category=(
        ('Male','Male'),
        ('Female','Female'),
    )
    admin = models.OneToOneField(CustomUser,null=True, on_delete = models.CASCADE)
    emp_no= models.CharField(max_length=100,null=True,blank=True)
    gender=models.CharField(max_length=100,null=True,choices=gender_category)
    mobile=models.CharField(max_length=10,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    profile_pic=models.ImageField(default="admin.png",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_employed=models.DateTimeField(auto_now_add=True, auto_now=False)
    objects = models.Manager()
    def __str__(self):
        return str(self.admin)
    



    
class Doctor(models.Model):
    gender_category=(
        ('Male','Male'),
        ('Female','Female'),
    )
    admin = models.OneToOneField(CustomUser,null=True, on_delete = models.CASCADE)
    emp_no=models.CharField(max_length=100,null=True,blank=True)
    age= models.IntegerField(default='0', blank=True, null=True)
    gender=models.CharField(max_length=100,null=True,choices=gender_category)
    mobile=models.CharField(max_length=10,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    profile_pic=models.ImageField(default="doctor.png",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return str(self.admin)
	

class PharmacyClerk(models.Model):
    gender_category=(
        ('Male','Male'),
        ('Female','Female'),
    )
    admin = models.OneToOneField(CustomUser,null=True, on_delete = models.CASCADE)
    emp_no=models.CharField(max_length=100,null=True,blank=True)
    gender=models.CharField(max_length=100,null=True,choices=gender_category)
    mobile=models.CharField(max_length=10,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    profile_pic=models.ImageField(default="images2.png",null=True,blank=True)
    age= models.IntegerField(default='0', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return str(self.admin)
	
    

class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)
    
    def __str__(self):
        return str(self.name)
	

    



class ExpiredManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
        )

class Stock(models.Model):
    category = models.ForeignKey(Category,null=True,on_delete=models.CASCADE,blank=True)
    drug_imprint=models.CharField(max_length=6 ,blank=True, null=True)
    drug_name = models.CharField(max_length=50, blank=True, null=True)
    drug_color = models.CharField(max_length=50, blank=True, null=True)
    drug_shape = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    manufacture= models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    drug_strength= models.CharField(max_length=10, blank=True, null=True)
    valid_from = models.DateTimeField(blank=True, null=True,default=timezone.now)
    valid_to = models.DateTimeField(blank=False, null=True)
    drug_description=models.TextField(blank=True,max_length=1000,null=True)
    drug_pic=models.ImageField(default="images2.png",null=True,blank=True)
    objects = ExpiredManager()
   
    def __str__(self):
        return str(self.drug_name)
  





@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        
        if instance.user_type == 3:
            Doctor.objects.create(admin=instance,address="")
        if instance.user_type == 4:
            PharmacyClerk.objects.create(admin=instance,address="")
        
       
       
       

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 4:
        instance.pharmacyclerk.save()
   


   



 