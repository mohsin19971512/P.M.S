from pharmacy.clerkViews import receptionistProfile
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import  UserCreationForm
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone, dateformat
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import datetime 

 
from .forms import *
from .models import *


def adminDashboard(request):
    medicines_total=Medicine.objects.all().count()
    
    Employees=Employee.objects.all().count()
    customers=Customer.objects.all().count() 
    receptionist=PharmacyClerk.objects.all().count() 
    out_of_stock=Stock.objects.filter(quantity__lte=0).count()
    total_stock=Stock.objects.all().count()
    stores = Store.objects.all().count()
    exipred=Stock.objects.annotate(
    expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True).count()
     


    context={
        "medicines_total":medicines_total,
        "expired_total":exipred,
        "out_of_stock":out_of_stock,
        "total_drugs":total_stock,
        "Employees":Employees,
        "customers":customers,
        "all_clerks":receptionist,
        "stores":stores

    }
    return render(request,'hod_templates/admin_dashboard.html',context)



def createMedicine(request):
    try:
        form=MedicineForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Medicine added Successfully!")

                return redirect('all_medicines')
    except:
        messages.error(request, "Medicine Not added! Try again")

        return redirect('medicine_form')

    
    context={
        "form":form,
        "title":"Add Medicine"
    }
       
    return render(request,'hod_templates/medicine_form.html',context)





def allMedicine(request):
    form=MedicineForm(request.POST or None)
    medicine=Medicine.objects.all()
    context={
        "medicine":medicine,
        "form":form,
        "title":"Admitted Patients"
    }
    if request.method == 'POST':
        # admin=form['first_name'].value()
        name = request.POST.get('search')
        medicines=Medicine.objects.filter(MEDICINE_NAME__icontains=name) 
       
        context={
            "medicine":medicines,
            form:form
        }
    return render(request,'hod_templates/medicine.html',context)

def confirmDelete(request,pk):
    try:
        medicine=Medicine.objects.get(id=pk)
        if request.method == 'POST':
            medicine.delete()
            return redirect('all_medicines')
    except:
        messages.error(request, "Medicine Cannot be deleted  deleted , Patient is still on medication or an error occured")
        return redirect('all_medicines')

    context={
        "medicine":medicine,

    }
    
    return render(request,'hod_templates/sure_delete.html',context)






def createPharmacyClerk(request):

    if request.method == "POST":
           
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
           
        try:
            user = CustomUser.objects.create_user(username=username, email=email,password=password, first_name=first_name, last_name=last_name, user_type=4)
            user.pharmacyclerk.address = address
            user.pharmacyclerk.mobile = mobile


            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_pharmacyClerk')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('add_pharmacyClerk')

    context = {
    "title":"Add Pharmacy Clerk"

}
    

    return render(request,'hod_templates/add_pharmacyClerk.html',context)

def managePharmacyClerk(request):
   
    


    staffs = PharmacyClerk.objects.all()
    context = {
        "staffs": staffs,
         "title":"Manage PharmacyClerk"
    }

    return render(request,'hod_templates/manage_pharmacyClerk.html',context)


def addStock(request):
    form=StockForm(request.POST,request.FILES)
    if form.is_valid():
        form=StockForm(request.POST,request.FILES)

        form.save()
        return redirect('add_stock')
    
    context={
        "form":form,
        "title":"Add New Drug"
    }
    return render(request,'hod_templates/add_stock.html',context)

    
def manageStock(request):
    stocks = Stock.objects.all().order_by("-id")
    ex=Stock.objects.annotate(
    expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True)
    eo=Stock.objects.annotate(
    expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=False)
    

    context = {
        "stocks": stocks,
        "expired":ex,
        "expa":eo,
        "title":"Manage Stocked Drugs"
    }

    return render(request,'hod_templates/manage_stock.html',context)


def addCategory(request):
    try:
        form=CategoryForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Category added Successfully!")

                return redirect('add_category')
    except:
        messages.error(request, "Category Not added! Try again")

        return redirect('add_category')

    
    context={
        "form":form,
        "title":"Add a New Drug Category"
    }
    return render(request,'hod_templates/add_category.html',context)



    
def editMedicine(request,medicine_id):
    # adds patient id into session variable
    request.session['medicine_id'] = medicine_id

    medicine = Medicine.objects.get(id=medicine_id)

    form = EditMedicineForm()
    

    # filling the form with data from the database
    form.fields['MEDICINE_NAME'].initial = medicine.MEDICINE_NAME
    form.fields['SELLING_PRICE'].initial = medicine.SELLING_PRICE
    form.fields['EXPIRE_DATE'].initial = medicine.EXPIRE_DATE
    form.fields['MANUFACTURE_NAME'].initial = medicine.MANUFACTURE_NAME
    form.fields['UNITARY_PRICE'].initial = medicine.UNITARY_PRICE
    form.fields['QUANTITY'].initial = medicine.QUANTITY
    form.fields['DISCOUNT'].initial = medicine.DISCOUNT
    if request.method == "POST":
        if medicine_id == None:
            return redirect('all_patients')
        form = EditMedicineForm( request.POST)

        if form.is_valid():
            
            MEDICINE_NAME = form.cleaned_data['MEDICINE_NAME']
            SELLING_PRICE = form.cleaned_data['SELLING_PRICE']
            EXPIRE_DATE = form.cleaned_data['EXPIRE_DATE']
            MANUFACTURE_NAME = form.cleaned_data['MANUFACTURE_NAME']
            UNITARY_PRICE = form.cleaned_data['UNITARY_PRICE']
            QUANTITY = form.cleaned_data['QUANTITY']
            DISCOUNT=form.cleaned_data['DISCOUNT']


            try:
            # First Update into Custom User Model
                user = Medicine.objects.get(id=medicine_id)
                user.MEDICINE_NAME = MEDICINE_NAME

                user.SELLING_PRICE = SELLING_PRICE
                user.save()

                # Then Update Students Table
                patients_edit = Medicine.objects.get(id=medicine_id)
                patients_edit.MEDICINE_NAME = MEDICINE_NAME
                patients_edit.SELLING_PRICE = SELLING_PRICE
                patients_edit.EXPIRE_DATE=EXPIRE_DATE
                patients_edit.MANUFACTURE_NAME=MANUFACTURE_NAME
                patients_edit.UNITARY_PRICE = UNITARY_PRICE
                patients_edit.QUANTITY = QUANTITY
                patients_edit.DISCOUNT = DISCOUNT




                
                patients_edit.save()
                messages.success(request, "Patient Updated Successfully!")
                return redirect('all_patients')
            except:
                messages.success(request, "Failed to Update Patient.")
                return redirect('all_patients')


    context = {
        "id": medicine_id,
        # "username": patient.admin.username,
        "form": form,
        "title":"Edit Patient"
    }
    return render(request, "hod_templates/edit_medicine.html", context)


       

    
def medicine_details(request,pk):
    patient=Medicine.objects.get(id=pk)
    

    context={
        "patient":patient,
        

    }
    return render(request,'hod_templates/medicine_details.html',context)



def hodProfile(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    staff=AdminHOD.objects.get(admin=customuser.id)


    form=HodForm()
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
       
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        customuser=CustomUser.objects.get(id=request.user.id)
        customuser.first_name=first_name
        customuser.last_name=last_name
        customuser.save()

        staff=AdminHOD.objects.get(admin=customuser.id)
        form =HodForm(request.POST,request.FILES,instance=staff)
        staff.address = address
       
        staff.mobile=mobile
        staff.save()

        if form.is_valid():
            form.save()

    context={
        "form":form,
        "staff":staff,
        "user":customuser
    }

    return render(request,'hod_templates/hod_profile.html',context)


def deletePharmacyClerk(request,pk):
    try:
        clerk=PharmacyClerk.objects.get(id=pk)
        if request.method == 'POST':
        
       
            clerk.delete()
            messages.success(request, "Pharmacy Clerk  deleted   successfully")
                
            return redirect('manage_pharmacyClerk')

    except:
        messages.error(request, "Pharmacy  Clerk Not deleted")
        return redirect('manage_pharmacyClerk')


   
    return render(request,'hod_templates/sure_delete.html')


def editPharmacyClerk(request,clerk_id):
    clerk=PharmacyClerk.objects.get(admin=clerk_id)
    if request.method == "POST":
        username = request.POST.get('username')
        last_name=request.POST.get('last_name')
        first_name=request.POST.get('first_name')
        address=request.POST.get('address')
        mobile=request.POST.get('mobile')
        gender=request.POST.get('gender')
        email=request.POST.get('email')
    
        try:
            user=CustomUser.objects.get(id=clerk_id)
            user.email=email
            user.username=username
            user.first_name=first_name
            user.last_name=last_name
            user.save()

            clerk =PharmacyClerk.objects.get(admin=clerk_id)
            clerk.address=address
            clerk.mobile=mobile
            clerk.gender=gender
            clerk.save()

            messages.success(request,'Receptionist Updated Succefully')
        except:
            messages.success(request,'An Error Was Encounterd Receptionist Not Updated')


        
    context={
        "staff":clerk,
        "title":"Edit PharmacyClerk"


    }
    return render(request,'hod_templates/edit_clerk.html',context)


def editAdmin(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    staff=AdminHOD.objects.get(admin=customuser.id)


    form=HodForm()
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
       
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        customuser=CustomUser.objects.get(id=request.user.id)
        customuser.first_name=first_name
        customuser.last_name=last_name
        customuser.save()

        staff=AdminHOD.objects.get(admin=customuser.id)
        form =HodForm(request.POST,request.FILES,instance=staff)
        staff.address = address
       
        staff.mobile=mobile
        staff.save()

        if form.is_valid():
            form.save()

    context={
        "form":form,
        "staff":staff,
        "user":customuser
    }

    return render(request,'hod_templates/edit-profile.html',context)


def editStock(request,pk):
    drugs=Stock.objects.get(id=pk)
    form=StockForm(request.POST or None,instance=drugs)

    if request.method == "POST":
        if form.is_valid():
            form=StockForm(request.POST or None ,instance=drugs)

            category=request.POST.get('category')
            drug_name=request.POST.get('drug_name')
            quantity=request.POST.get('quantity')
            # email=request.POST.get('email')

            try:
                drugs =Stock.objects.get(id=pk)
                drugs.drug_name=drug_name
                drugs.quantity=quantity
                drugs.save()
                form.save()
                messages.success(request,'Receptionist Updated Succefully')
            except:
                messages.error(request,'An Error Was Encounterd Receptionist Not Updated')


        
    context={
        "drugs":drugs,
         "form":form,
         "title":"Edit Stock"

    }
    return render(request,'hod_templates/edit_drug.html',context)


def deleteDrug(request,pk):
    try:
    
        drugs=Stock.objects.get(id=pk)
        if request.method == 'POST':
        
            drugs.delete()
            messages.success(request, "Pharmacist  deleted successfully")
                
            return redirect('manage_stock')

    except:
        messages.error(request, "Pharmacist aready deleted")
        return redirect('manage_stock')



    return render(request,'hod_templates/sure_delete.html')

def receiveDrug(request,pk):
    receive=Stock.objects.get(id=pk)
    form=ReceiveStockForm()
    try:
        form=ReceiveStockForm(request.POST or None )

        if form.is_valid():
            form=ReceiveStockForm(request.POST or None ,instance=receive)

            instance=form.save(commit=False) 
            instance.quantity+=instance.receive_quantity
            instance.save()
            form=ReceiveStockForm()

            messages.success(request, str(instance.receive_quantity) + " " + instance.drug_name +" "+ "drugs added successfully")

            return redirect('manage_stock')

      
    except:
        messages.error(request,"An Error occured, Drug quantity Not added")
                
        return redirect('manage_stock')
    context={
            "form":form,
            "title":"Add Drug"
            
        }
    return render(request,'hod_templates/modal_form.html',context)


def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.drug_name) + " is updated to " + str(instance.reorder_level))

        return redirect("manage_stock")
    context ={
        "instance": queryset,
        "form": form,
        "title":"Reorder Level"
    }

    return render(request,'hod_templates/reorder_level.html',context)

def drugDetails(request,pk):
    stocks=Stock.objects.get(id=pk)
    # prescrip=stocks.prescription_set.all()
    # stocks=stocks.dispense_set.all()

    context={
        "stocks":stocks,
        # "prescription":prescrip,
        # "stocks":stocks

    }
    return render(request,'hod_templates/view_drug.html',context)
