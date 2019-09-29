from django.contrib import admin
from gho.users import models
register = admin.site.register


register(models.Phonenumber)
register(models.PhoneVerification)
register(models.UserProfile)
register(models.NewUserPhoneVerification)

