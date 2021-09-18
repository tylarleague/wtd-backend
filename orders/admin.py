from django.contrib import admin

# Register your models here.
from orders.models import Order, Invoice, ExtraServices, AmbReport

# admin.site.register(Order)
admin.site.register(Invoice)
admin.site.register(ExtraServices)
admin.site.register(AmbReport)



@admin.register(Order)
class InvoiceAdmin(admin.ModelAdmin):
    # list_display = ['owner', 'custom_id',]
    readonly_fields = ('custom_id',)