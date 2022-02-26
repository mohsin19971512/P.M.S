from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserModel(UserAdmin):
    pass
admin.site.register(Medicine)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Store)
admin.site.register(Location)
admin.site.register(CustomUser, UserModel)
admin.site.register(AdminHOD)
admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(PharmacyClerk)



   



 



