from django.contrib import admin
from .models import SellerProfile, ClientProfile
from django.contrib.auth.models import User

# Register your models here.


class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop_name')
    search_fields = ['shop_name']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ClientAdmin(admin.ModelAdmin):
    username = User.username
    list_display = ['user']
    # search_fields = ['user']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(SellerProfile, SellerAdmin)
admin.site.register(ClientProfile, ClientAdmin)
