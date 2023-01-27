from django.contrib import admin
from . models import Products,GuestUser,Cart
# Register your models here.

admin.site.register(Products)
admin.site.register(GuestUser)
admin.site.register(Cart)
