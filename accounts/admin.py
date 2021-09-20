from django.contrib import admin
from .models import User, ClientProfile, OperationProfile, ProviderProfile, Person, Organization, SpecialAccounts

# Register your models here.
admin.site.register(User)
admin.site.register(ClientProfile)
admin.site.register(OperationProfile)
admin.site.register(ProviderProfile)
admin.site.register(Person)
admin.site.register(Organization)
admin.site.register(SpecialAccounts)




