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
    now = datetime.now()
    exipred_medicine = Medicine.objects.filter(EXPIRE_DATE__lt=now)
    medicine_out_of_stock=Medicine.objects.filter(QUANTITY__lte=0).count()
    medicines_total=Medicine.objects.all().count()
    Employees=Employee.objects.all().count()
    customers=Customer.objects.all().count() 
    out_of_stock=Stock.objects.filter(quantity__lte=0).count()
    total_stock=Stock.objects.all().count()
    stores = Store.objects.all().count()
    exipred=Stock.objects.annotate(
    expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True).count()
         
    context={
        'exipred_medicine':len(exipred_medicine),
        'medicine_out_of_stock':medicine_out_of_stock,
        "medicines_total":medicines_total,
        "expired_total":exipred,
        "out_of_stock":out_of_stock,
        "total_drugs":total_stock,
        "Employees":Employees,
        "customers":customers,
        "stores":stores

    }
    return render(request,'hod_templates/admin_dashboard.html',context)


# 2- GET exipred_medicine
def exipred_medicine(request):
    now = datetime.now()
    form=MedicineForm(request.POST or None)
    medicine=Medicine.objects.filter(EXPIRE_DATE__lt=now)
    context={
        "medicine":medicine,
        "form":form,
        "title":"Exipred Medicine"
    }
    if request.method == 'POST':
        # admin=form['first_name'].value()
        name = request.POST.get('search')
        medicines=Medicine.objects.filter(MEDICINE_NAME__icontains=name,EXPIRE_DATE__lt=now) 
       
        context={
            "medicine":medicines,
            form:form
        }
    return render(request,'hod_templates/medicine.html',context)

# 2- GET medicine_out_of_stock
def medicine_out_of_stock(request):
    now = datetime.now()
    form=MedicineForm(request.POST or None)
    medicine=Medicine.objects.filter(QUANTITY__lte=0)
    context={
        "medicine":medicine,
        "form":form,
        "title":"Medicines Out Of Stock"
    }
    if request.method == 'POST':
        # admin=form['first_name'].value()
        name = request.POST.get('search')
        medicines=Medicine.objects.filter(MEDICINE_NAME__icontains=name,QUANTITY__lte=0) 
       
        context={
            "medicine":medicines,
            form:form
        }
    return render(request,'hod_templates/medicine.html',context)



  
def drug_out_of_stock(request):
    stocks = Stock.objects.filter(quantity__lte=0)
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
        "title":" Drugs Out Of Stocks"
    }

    return render(request,'hod_templates/manage_stock.html',context)

def expired_drug(request):
    stocks = Stock.objects.annotate(
    expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True)
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
        "title":"Expired Drugs"
    }

    return render(request,'hod_templates/manage_stock.html',context)
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#Start Medicine
# CRUD Medicine 
# 1- Create Medicine
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

# 2- GET all Medicine
def allMedicine(request):
    form=MedicineForm(request.POST or None)
    medicine=Medicine.objects.all()
    context={
        "medicine":medicine,
        "form":form,
        "title":"Medicine"
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

# 3- Delete Medicine
def confirmDelete(request,pk):
    try:
        medicine=Medicine.objects.get(id=pk)
        if request.method == 'POST':
            medicine.delete()
            return redirect('all_medicines')
    except:
        messages.error(request, "Medicine Cannot be deleted  deleted , Medicine is still on medication or an error occured")
        return redirect('all_medicines')

    context={
        "medicine":medicine,
        'name': "Medicine",
        'redirect':'all_medicines'

    }
    
    return render(request,'hod_templates/sure_delete.html',context)

# 4- Edit Medicine 
def editMedicine(request,medicine_id):
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
            return redirect('all_medicines')
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
                medicines_edit = Medicine.objects.get(id=medicine_id)
                medicines_edit.MEDICINE_NAME = MEDICINE_NAME
                medicines_edit.SELLING_PRICE = SELLING_PRICE
                medicines_edit.EXPIRE_DATE=EXPIRE_DATE
                medicines_edit.MANUFACTURE_NAME=MANUFACTURE_NAME
                medicines_edit.UNITARY_PRICE = UNITARY_PRICE
                medicines_edit.QUANTITY = QUANTITY
                medicines_edit.DISCOUNT = DISCOUNT




                
                medicines_edit.save()
                messages.success(request, "Medicine Updated Successfully!")
                return redirect('all_medicines')
            except:
                messages.success(request, "Failed to Update Medicine.")
                return redirect('all_medicines')


    context = {
        "id": medicine_id,
        "form": form,
        "title":"Edit Medicine"
    }
    return render(request, "hod_templates/edit_medicine.html", context)


def medicine_details(request,pk):
    medicine=Medicine.objects.get(id=pk)
    context={
        "medicine":medicine,
    }
    return render(request,'hod_templates/medicine_details.html',context)

#End Medicine
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------

# start Employee
# 1- create_employee
def create_employee(request):
    try:
        form=EmployeeForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Employee added Successfully!")

                return redirect('all_employee')
    except:
        messages.error(request, "Employee Not added! Try again")

        return redirect('employee_form')

    
    context={
        "form":form,
        "title":"Add Employee"
    }
       
    return render(request,'hod_templates/employee_form.html',context)


# get all employee
def allEmployee(request):
    form=EmployeeForm(request.POST or None)
    employee=Employee.objects.all()
    context={
        "employee":employee,
        "form":form,
        "title":"Employees"
    }
    if request.method == 'POST':
        # admin=form['first_name'].value()
        name = request.POST.get('search')
        employees=Employee.objects.filter(EMPLOYEE_NAME__icontains=name) 
       
        context={
            "employees":employees,
            form:form
        }
    return render(request,'hod_templates/employees.html',context)

#Edit Employee
def edit_employee(request,employee_id):
    employee=Employee.objects.get(id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('all_employee')      

    else:
        form = EmployeeForm(instance=employee)

    return render(request,'hod_templates/employee_form.html',{'form': form,"title":"Edit Employee"})




# delete Employee
def deleteEmployee(request,pk):
    try:
        medicine=Employee.objects.get(id=pk)
        if request.method == 'POST':
            medicine.delete()
            return redirect('all_employee')
    except:
        messages.error(request, "Employee Cannot be deleted  deleted , Employee is still on medication or an error occured")
        return redirect('all_employee')

    context={
        "medicine":medicine,
        'name': "Employee",
        'redirect':'all_employee'

    }
    
    return render(request,'hod_templates/sure_delete.html',context)

def employee_details(request,pk):
    employee=Employee.objects.get(id=pk)
    

    context={
        "employee":employee,
        

    }
    return render(request,'hod_templates/employee_details.html',context)

#end employee
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------


# Start Customer

# 1- ADD Customer
def create_customer(request):
    try:
        form=CustomerForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Customer added Successfully!")

                return redirect('all_customers')
    except:
        messages.error(request, "Customer Not added! Try again")

        return redirect('create_customer')

    
    context={
        "form":form,
        "title":"Add Customer"
    }
       
    return render(request,'hod_templates/edit_customer.html',context)



# get all Customers
def allCustomers(request):
    form=CustomerForm(request.POST or None)
    customer=Customer.objects.all()
    context={
        "customer":customer,
        "form":form,
        "title":"Customers"
    }
    if request.method == 'POST':
        # admin=form['first_name'].value()
        name = request.POST.get('search')
        customers=Employee.objects.filter(CUSTOMER_NAME__icontains=name) 
       
        context={
            "customers":customers,
            form:form
        }
    return render(request,'hod_templates/customers.html',context)



#Edit customer
def edit_customer(request,customer_id):
    customer=Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('all_customers')      

    else:
        form = CustomerForm(instance=customer)

    return render(request,'hod_templates/edit_customer.html',{'form': form,"title":"Edit Customer"})



# Delete Customer
def deleteCustomer(request,pk):
    try:
        customer=Customer.objects.get(id=pk)
        if request.method == 'POST':
            customer.delete()
            return redirect('all_customers')
    except:
        messages.error(request, "Customer Cannot be deleted  deleted , Customer is still  or an error occured")
        return redirect('all_employee')

    context={
        "customer":customer,
        'name': "Customer",
        'redirect':'all_customers'

    }
    
    return render(request,'hod_templates/sure_delete.html',context)



def customer_details(request,pk):
    customer=Customer.objects.get(id=pk)
    

    context={
        "customer":customer,
        

    }
    return render(request,'hod_templates/customer_details.html',context)

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------

# start store
# 1- create_store

def create_store(request):
    try:
        form=StoreForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Store added Successfully!")

                return redirect('all_stores')
    except:
        messages.error(request, "Store Not added! Try again")

        return redirect('create_store')

    
    context={
        "form":form,
        "title":"Add Store"
    }
       
    return render(request,'hod_templates/create_store.html',context)



# get all Stores
def allStores(request):
    form=CustomerForm(request.POST or None)
    store=Store.objects.all()
    context={
        "store":store,
        "form":form,
        "title":"Stores"
    }
    if request.method == 'POST':
        # admin=form['first_name'].value()
        name = request.POST.get('search')
        stores=Store.objects.filter(STORE_NAME__icontains=name) 
       
        context={
            "stores":stores,
            form:form
        }
    return render(request,'hod_templates/stores.html',context)




#Edit Store
def edit_store(request,store_id):
    store=Store.objects.get(id=store_id)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('all_stores')      

    else:
        form = StoreForm(instance=store)

    return render(request,'hod_templates/edit_store.html',{'form': form,"title":"Edit Store"})




# Delete Store
def deleteStore(request,pk):
    try:
        store=Store.objects.get(id=pk)
        if request.method == 'POST':
            store.delete()
            return redirect('all_stores')
    except:
        messages.error(request, "Store Cannot be deleted   , Store is still  or an error occured")
        return redirect('all_stores')

    context={
        "store":store,
        'name': "Store",
        'redirect':'all_stores'

    }
    
    return render(request,'hod_templates/sure_delete.html',context)


#Details
def store_details(request,pk):
    store=Store.objects.get(id=pk)
    

    context={
        "store":store,
        

    }
    return render(request,'hod_templates/store_details.html',context)





#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
# Stock
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

#End stock
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------

       

    





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




