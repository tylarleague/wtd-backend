from django.db import models
from simple_history.models import HistoricalRecords
# Create your models here.
from accounts.models import ClientProfile, Person, ProviderProfile, OperationProfile
from django.contrib.postgres.fields import JSONField
from datetime import datetime, timedelta
from django.utils import timezone



class Region(models.Model):
    name = models.CharField(max_length=2000)
    operator = models.ForeignKey(
        OperationProfile, related_name="operation_related_regions", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + " region operated by: " + str(self.operator.user.name)


class RegionPoint(models.Model):
    region = models.ForeignKey(
        Region, related_name="region_related_points", on_delete=models.CASCADE)
    name = models.CharField(max_length=2000, null=True, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return str(self.lat) +" , " + str(self.lng) + " related to: " + str(self.region.name)


class City(models.Model):
    name = models.CharField(max_length=2000)
    region = models.ForeignKey(
        Region, related_name="region_related_cities", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class CityPoint(models.Model):
    city = models.ForeignKey(
        City, related_name="city_related_points", on_delete=models.CASCADE)
    name = models.CharField(max_length=2000, null=True, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return str(self.lat) +" , " + str(self.lng) + " related to: " + str(self.city.name)

class SpecialLocation(models.Model):
    name = models.CharField(max_length=2000)
    one_way_price = models.IntegerField()
    two_way_price = models.IntegerField()
    special_price = models.IntegerField(default=0)
    city = models.ForeignKey(
        City, related_name="city_related_special_locations", on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return str(self.name) + ": 1-way: " + str(self.one_way_price) + " - 2-way: " + str(self.two_way_price)


class SpecialLocationPoint(models.Model):
    special_location = models.ForeignKey(
        SpecialLocation, related_name="special_location_related_points", on_delete=models.CASCADE)
    name = models.CharField(max_length=2000, null=True, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return str(self.lat) +" , " + str(self.lng) + " related to: " + str(self.special_location.name)

class Order(models.Model):
    owner = models.ForeignKey(
        ClientProfile, related_name="owner_related_orders", on_delete=models.CASCADE)
    patient = models.ForeignKey(
        Person, related_name="patient_related_orders", on_delete=models.CASCADE)
    from_location = JSONField(null=True, blank=True)
    to_location = JSONField(null=True, blank=True)
    order_date = models.DateField(null=True, blank=True)
    arrival_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by_client = models.BooleanField(default=False)
    payment_authorized = models.BooleanField(default=False)
    order_type = models.CharField(max_length=50, default="ONE_WAY")
    waiting_time = models.IntegerField(null=True, blank=True)
    # need_nurse = models.BooleanField(default=False)
    provider = models.ForeignKey(
        ProviderProfile, related_name="provider_related_orders", on_delete=models.CASCADE, null=True, blank=True)
    operator = models.ForeignKey(
        OperationProfile, related_name="operator_related_orders", on_delete=models.CASCADE, null=True, blank=True)
    approved_by_provider = models.BooleanField(null=True, blank=True)
    notes = models.CharField(max_length=500, null=True, blank=True)
    health_institution = models.BooleanField(default=False)
    appointment_approval = models.FileField(
        upload_to='appointment_approvals', null=True, blank=True)
    discharge_approval = models.FileField(
        upload_to='discharge_approvals', null=True, blank=True)
    from_region = models.ForeignKey(
        Region, related_name="from_region_related_orders", on_delete=models.CASCADE, null=True, blank=True)
    to_region = models.ForeignKey(
        Region, related_name="to_region_related_orders", on_delete=models.CASCADE, null=True, blank=True)
    from_city = models.ForeignKey(
        City, related_name="from_city_related_orders", on_delete=models.CASCADE, null=True, blank=True)
    to_city = models.ForeignKey(
        City, related_name="to_city_related_orders", on_delete=models.CASCADE, null=True, blank=True)
    from_special_location = models.ForeignKey(
        SpecialLocation, related_name="from_special_location_related_orders", on_delete=models.CASCADE, null=True, blank=True)
    to_special_location = models.ForeignKey(
        SpecialLocation, related_name="to_special_location_related_orders", on_delete=models.CASCADE, null=True, blank=True)
    is_overweight = models.BooleanField(null=True, blank=True)
    is_emergency= models.BooleanField(null=True, blank=True)
    is_contagious = models.BooleanField(null=True, blank=True)
    needs_oxygen = models.BooleanField(null=True, blank=True)
    is_discharged = models.BooleanField(null=True, blank=True)
    order_block_start = models.TimeField(null=True, blank=True)
    order_block_end = models.TimeField(null=True, blank=True)
    history = HistoricalRecords()

    # models.ForeignKey(subjects, blank=True, null=True)
    # special_id = models.CharField(max_length=255, null=True, default=None)

    # def save(self, *args, **kwargs):
    #     if not self.special_id:
    #         prefix = 'WTD{}'.format(timezone.now().strftime('%y%m%d')
    #         prev_instances = self.__class__.objects.filter(special_id__contains=prefix))
    #         if prev_instances.exists():
    #             last_instance_id = prev_instances.last().special_id[-4:]
    #             self.special_id = prefix + '{0:04d}'.format(int(last_instance_id) + 1)
    #         else:
    #             self.special_id = prefix + '{0:04d}'.format(1)
    #     super(Order, self).save(*args, **kwargs)
    # def save(self, flag=True, *args, **kwargs):
    #     # Save your object. After this line, value of custom_id will be 0 which is default value
    #     super(Order, self).save(flag=True, *args, **kwargs)
    #     # Here value of custom_id will be updated according to your id value
    #     if flag:
    #         self.custom_id = 'WTD{}{}'.format(timezone.now().strftime('%y%m%d'), self.id)
    #         self.save(flag=False, *args, **kwargs)

    def __str__(self):
        return str(self.id) + " related to user: " + str(self.owner.user.name) + " w/ phone #: " + str(self.owner.user.phone_number)

    @property
    def amb_arrival(self):
        # print('self.arrival_time', str(self.arrival_time))
        # print("teeest", datetime.strptime(str(self.arrival_time), "%H:%M:%S"))
        my_arrival_time = datetime.strptime(str(self.arrival_time), "%H:%M:%S")
        # print('SEEECONDS', self.order_related_invoice.duration_value)
        # print('mytest', my_arrival_time - timedelta(seconds=self.order_related_invoice.duration_value))

        return (my_arrival_time - timedelta(seconds=self.order_related_invoice.duration_value)).time()

    @property
    def custom_id(self):
        print(self)
        if(self):
            return 'WTD{}{}'.format(datetime.strftime(self.order_date, '%y%m%d'), self.id)
        return None

    # return 'WTD{}{}'.format(datetime.strptime(str(self.arrival_time), "%H:%M:%S"), self.id)
    # datetime.strptime(str(self.arrival_time), "%H:%M:%S")
        # return 'WTD{}{}'.format(self.id, self.id)

class Invoice(models.Model):
    order = models.OneToOneField(
        Order, related_name="order_related_invoice", on_delete=models.CASCADE)
    distance_value = models.IntegerField()
    distance_text = models.CharField(max_length=50)
    duration_value = models.IntegerField()
    duration_text = models.CharField(max_length=50)
    cost = models.IntegerField()
    initial_cost = models.IntegerField(default=0)


    def __str__(self):
        return str(self.id) + " related to order: " + str(self.order.id)

class AmbReport(models.Model):
    order = models.OneToOneField(
        Order, related_name="order_related_report", on_delete=models.CASCADE)
    history = models.CharField(max_length=2000, null=True, blank=True)
    temp = models.CharField(max_length=100, null=True, blank=True)
    oxygen = models.CharField(max_length=100, null=True, blank=True)
    BP = models.CharField(max_length=100, null=True, blank=True)
    pulse = models.CharField(max_length=100, null=True, blank=True)
    infectious_diseases = models.BooleanField(default=False)


    def __str__(self):
        return str(self.id) + " related to order: " + str(self.order.id)

class ExtraServices(models.Model):
    service_name = models.CharField(max_length=100)
    service_cost = models.IntegerField()
    # order = models.ManyToManyField(
    #     Order, related_name="ordr_extra_services", null=True, blank=True)

    def __str__(self):
        return str(self.id) + " - " + str(self.service_name )

class OrderPossibleProvider(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_possible_providers", on_delete=models.CASCADE)
    provider = models.ForeignKey(
        ProviderProfile, related_name="provider_possible_orders", on_delete=models.CASCADE)
    importance = models.FloatField()
    order_block_start = models.TimeField(null=True, blank=True)
    order_block_end = models.TimeField(null=True, blank=True)
    # order = models.ManyToManyField(
    #     Order, related_name="ordr_extra_services", null=True, blank=True)

    def __str__(self):
        return "possible provider: " + str(self.provider) + " of order " + str(self.order) + " - importance: " + str(self.importance)
