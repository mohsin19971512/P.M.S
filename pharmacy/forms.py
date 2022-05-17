from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import Form
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import RegexValidator

import json

      
class DateInput(forms.DateInput):
    input_type = "date"

class MedicineForm(forms.ModelForm):
    EXPIRE_DATE= forms.DateField(label="Expiry Date", widget=DateInput(attrs={"class":"form-control"}))
    class Meta:
        model=Medicine
        fields='__all__'

class EmployeeForm(forms.ModelForm):
    PASSWORD = forms.CharField(widget=forms.PasswordInput)
    SELLING_DATE = forms.DateField(label="Expiry Date", widget=DateInput(attrs={"class":"form-control"}))
    class Meta:
        model=Employee
        fields='__all__'
class CustomerForm(forms.ModelForm):
    #PASSWORD = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Customer
        fields='__all__'

class StoreForm(forms.ModelForm):
    class Meta:
        model=Store
        fields='__all__'    

class EditMedicineForm(forms.Form):
    MEDICINE_NAME = forms.CharField(label="Medicine Name", max_length=500, widget=forms.TextInput(attrs={"class":"form-control"}))
    SELLING_PRICE = forms.IntegerField(label="Selling Price", widget=forms.TextInput(attrs={"class":"form-control"}))
    
    EXPIRE_DATE = forms.DateField(label="Expire Date", widget=forms.DateInput(attrs={"class":"form-control"}))
    MANUFACTURE_NAME = forms.CharField(label="Manufacture Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    UNITARY_PRICE = forms.CharField(label="Unitary Price", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    QUANTITY = forms.CharField(label="Quantity", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    DISCOUNT = forms.IntegerField(label="Dicount", widget=forms.TextInput(attrs={"class":"form-control"}))
        



from phonenumber_field.formfields import PhoneNumberField
class ClientForm(forms.Form):
    mobile = PhoneNumberField()

   

    
class StockForm(forms.ModelForm):
    valid_to= forms.DateField(label="Expiry Date", widget=DateInput(attrs={"class":"form-control"}))

    class Meta:
        model=Stock
        fields='__all__'
        exclude=['valid_from','reorder_level','receive_quantity', 'prescrip_drug_acess']

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'




class HodForm(ModelForm):
    class Meta:
        model=AdminHOD
        fields='__all__'
        exclude=['admin','gender','mobile','address']


class ReceiveStockForm(ModelForm):
    valid_to= forms.DateField(label="Expiry Date", widget=DateInput(attrs={"class":"form-control"}))

    class Meta:
        model=Stock
        fields='__all__'
        exclude=['category' ,'drug_name','valid_from','dispense_quantity','reorder_level','date_from','date_to','quantity','manufacture']


class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level']

