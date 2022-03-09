from django.contrib import admin

# Register your models here.
from orders.models import Order, Invoice, ExtraServices, AmbReport, Region, RegionPoint, CityPoint, City, SpecialLocationPoint, SpecialLocation

# admin.site.register(Order)
admin.site.register(Invoice)
admin.site.register(ExtraServices)
admin.site.register(AmbReport)
admin.site.register(Region)
admin.site.register(RegionPoint)
admin.site.register(City)
admin.site.register(CityPoint)
admin.site.register(SpecialLocation)
admin.site.register(SpecialLocationPoint)



@admin.register(Order)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['owner', 'custom_id','patient','order_date','arrival_time','status']
    readonly_fields = ('custom_id',)
    search_fields = ('id','owner__user__phone_number','status')