from django.urls import path
from .import HODViews
from .import views,clerkViews
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('',HODViews.adminDashboard,name='admin_dashboard'),
    path('admin_user/medicine_form/',HODViews.createMedicine,name='medicine_form'),
    path('admin_user/all_medicines/',HODViews.allMedicine,name='all_medicines'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'), 
    # path('get_user_details/', views.get_user_details, name="get_user_details"),

    path('admin_user/add_pharmacyClerk/',HODViews.createPharmacyClerk,name='add_pharmacyClerk'),
    path('admin_user/admin_user/manage_pharmacyClerk/',HODViews.managePharmacyClerk,name='manage_pharmacyClerk'),
    path('admin_user/add_stock/',HODViews.addStock,name='add_stock'),
    path('admin_user/add_category/',HODViews.addCategory,name='add_category'),
    path('admin_user/manage_stock/',HODViews.manageStock,name='manage_stock'),    
    path('admin_user/edit_medicine/<medicine_id>/',HODViews.editMedicine,name='edit_medicine'),

    path('admin_user/delete_medicine/<str:pk>/',HODViews.confirmDelete,name='delete_medicine'),
    path('admin_user/medicines_Records/<pk>/',HODViews.medicine_details,name='medicine_details'),
    path('admin_user/hod_profile/',HODViews.hodProfile,name='hod_profile'),
    path('admin_user/delete_receptionist/<str:pk>/',HODViews.deletePharmacyClerk,name='delete_clerk'),
    path('admin_user/hod_profile/editAdmin_profile/',HODViews.editAdmin,name='edit-admin'),
    path('admin_user/delete_drug/<str:pk>/',HODViews.deleteDrug,name='delete_drug'),


    path('admin_user/edit_receptionist/<clerk_id>/', HODViews.editPharmacyClerk, name="edit_clerk"),
    path('admin_user/edit_drug/<pk>/', HODViews.editStock, name="edit_drug"),
    path('admin_user/receive_drug/<pk>/', HODViews.receiveDrug, name="receive_drug"),
    path('admin_user/reorder_level/<str:pk>/', HODViews.reorder_level, name="reorder_level"),
    path('admin_user/drug_details/<str:pk>/', HODViews.drugDetails, name="drug_detail"),




    #Receptionist
    path('receptionist_profile/',clerkViews.receptionistProfile,name='clerk_profile'),
    path('receptionist_home/',clerkViews.clerkHome,name='clerk_home'),
    path('receptionist/patient_form/',clerkViews.createPatient,name='patient_form2'),
    path('receptionist/all_patients/',clerkViews.allPatients,name='all_patients2'),
    path('receptionist/edit_patient/<patient_id>/',clerkViews.editPatient,name='edit_patient_clerk'),
    path('receptionist/patient_personalRecords/<str:pk>/',clerkViews.patient_personalRecords,name='patient_record_clerk'),
    path('receptionist/delete_patient/<str:pk>/',clerkViews.confirmDelete,name='delete_patient_clerk'),
    # path('receptionist/dispense_drug/<str:pk>/',pharmacistViews.dispenseDrug,name='dispense_drug'),


  
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="reset_password"),

    path('reset_password_sent/',auth_views.PasswordResetDoneView
    .as_view(template_name="password_reset_sent.html"),name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView
    .as_view(template_name="password_reset_form.html"),name="password_reset_confirm"),



    

   path('reset_password_complete/',auth_views.PasswordResetCompleteView
    .as_view(template_name="password_reset_done.html"),name="password_reset_complete"),
]
