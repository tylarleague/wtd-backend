from django.contrib import admin
from .models import User, ClientProfile, OperationProfile, ProviderProfile, Person, Organization, SpecialAccounts

# Register your models here.
admin.site.register(ClientProfile)
admin.site.register(OperationProfile)
admin.site.register(ProviderProfile)
admin.site.register(Organization)
admin.site.register(SpecialAccounts)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'name', 'isVerified','isClient','isOperation','isProvider']
    search_fields = ('id','phone_number','name', 'isVerified','isClient','isOperation','isProvider')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender', 'birth_day','nationality','relation']
    search_fields = ('id','name','nationality', 'relation')




