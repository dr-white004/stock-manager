from django.contrib import admin
from .models import CustomUser, ClockType, Stock, Sale, Return
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass

@admin.register(ClockType)
class ClockTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['user', 'created_at']

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['clock_type', 'user', 'quantity_received', 'defective_quantity', 'good_quantity', 'date_received']
    list_filter = ['clock_type', 'user', 'date_received']
    search_fields = ['clock_type__name']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['clock_type', 'user', 'quantity', 'sale_date']
    list_filter = ['clock_type', 'user', 'sale_date']
    search_fields = ['clock_type__name', 'notes']

@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ['clock_type', 'user', 'quantity', 'return_date']
    list_filter = ['clock_type', 'user', 'return_date']
    search_fields = ['clock_type__name', 'notes']
