from django.urls import path
from .import HODViews
from .import views
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('',HODViews.adminDashboard,name='admin_dashboard'),
    path('admin_user/medicine_form/',HODViews.createMedicine,name='medicine_form'),
    path('admin_user/create_employee/',HODViews.create_employee,name='employee_form'),
    path('admin_user/create_customer/',HODViews.create_customer,name='create_customer'),
    path('admin_user/create_store/',HODViews.create_store,name='create_store'),
    

    path('admin_user/all_medicines/',HODViews.allMedicine,name='all_medicines'),
    path('admin_user/all_employee/',HODViews.allEmployee,name='all_employee'),
    path('admin_user/all_customers/',HODViews.allCustomers,name='all_customers'),
    path('admin_user/all_stores/',HODViews.allStores,name='all_stores'),
    path('admin_user/exipred_medicine/',HODViews.exipred_medicine,name='exipred_medicine'),
    path('admin_user/medicine_out_of_stock/',HODViews.medicine_out_of_stock,name='medicine_out_of_stock'),
    path('admin_user/drug_out_of_stock/',HODViews.drug_out_of_stock,name='drug_out_of_stock'),
    path('admin_user/expired_drug/',HODViews.expired_drug,name='expired_drug'),
    
    
    
    
    path('admin_user/edit_employee/<employee_id>/',HODViews.edit_employee,name='edit_employee'),
    path('admin_user/edit_customer/<customer_id>/',HODViews.edit_customer,name='edit_customer'),
    path('admin_user/edit_store/<store_id>/',HODViews.edit_store,name='edit_store'),
    
    
    path('admin_user/delete_employee/<str:pk>/',HODViews.deleteEmployee,name='deleteEmployee'),
    path('admin_user/deleteCustomer/<str:pk>/',HODViews.deleteCustomer,name='deleteCustomer'),
    path('admin_user/deleteStore/<str:pk>/',HODViews.deleteStore,name='deleteStore'),
    
    
    path('admin_user/employee_details/<pk>/',HODViews.employee_details,name='employee_details'),
    path('admin_user/customer_details/<pk>/',HODViews.customer_details,name='customer_details'),
    path('admin_user/store_details/<pk>/',HODViews.store_details,name='store_details'),
    
    




    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'), 
    # path('get_user_details/', views.get_user_details, name="get_user_details"),

    path('admin_user/add_stock/',HODViews.addStock,name='add_stock'),
    path('admin_user/add_category/',HODViews.addCategory,name='add_category'),
    path('admin_user/manage_stock/',HODViews.manageStock,name='manage_stock'),    
    path('admin_user/edit_medicine/<medicine_id>/',HODViews.editMedicine,name='edit_medicine'),

    path('admin_user/delete_medicine/<str:pk>/',HODViews.confirmDelete,name='delete_medicine'),
    path('admin_user/medicines_Records/<pk>/',HODViews.medicine_details,name='medicine_details'),
    path('admin_user/hod_profile/',HODViews.hodProfile,name='hod_profile'),
    path('admin_user/hod_profile/editAdmin_profile/',HODViews.editAdmin,name='edit-admin'),
    path('admin_user/delete_drug/<str:pk>/',HODViews.deleteDrug,name='delete_drug'),


    path('admin_user/edit_drug/<pk>/', HODViews.editStock, name="edit_drug"),
    path('admin_user/receive_drug/<pk>/', HODViews.receiveDrug, name="receive_drug"),
    path('admin_user/reorder_level/<str:pk>/', HODViews.reorder_level, name="reorder_level"),
    path('admin_user/drug_details/<str:pk>/', HODViews.drugDetails, name="drug_detail"),




 


  
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="reset_password"),

    path('reset_password_sent/',auth_views.PasswordResetDoneView
    .as_view(template_name="password_reset_sent.html"),name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView
    .as_view(template_name="password_reset_form.html"),name="password_reset_confirm"),



    

   path('reset_password_complete/',auth_views.PasswordResetCompleteView
    .as_view(template_name="password_reset_done.html"),name="password_reset_complete"),
]
