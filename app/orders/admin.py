from django.contrib import admin
from . import models




class LaborItemAdmin(admin.TabularInline): 
    model = models.OrderLineItem
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'due_date', 'date_completed', 'equipment_description', 'os_version', 'customer_po')
    search_fields = ('customer', 'equipment_description', 'os_version', 'customer_po')
    list_filter = ('due_date', 'date_completed')
    inlines = [LaborItemAdmin]    
    
 
    
admin.site.register(models.Order, OrderAdmin)

admin.site.register(models.OrderConfig)

class LaborItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_taxable', 'default_labor_description', 'labor_rate', 'is_active')
    
admin.site.register(models.LaborItem, LaborItemAdmin)