from rest_framework import serializers

from accounts.models import ProviderProfile
from accounts.serializers import ClientProfileSerializer, PersonSerializer, ProvidersSerializer, UserSerializer
from orders.models import Order, Invoice, ExtraServices

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class extraServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraServices
        fields = ['service_cost', 'service_name']

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class GetOrdersSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    amb_arrival = serializers.ReadOnlyField()
    patient = PersonSerializer()
    order_related_invoice = InvoiceSerializer()
    provider = ProvidersSerializer()
    provider_id = serializers.PrimaryKeyRelatedField(source='provider', queryset=ProviderProfile.objects.all(), write_only=True, allow_null=True)
    order_extra_services =extraServicesSerializer(required=False, many=True, read_only=True)
    class Meta:
        model = Order
        fields = "__all__"

# class GetOrdersToAmbSerializer(serializers.ModelSerializer):
#     # owner = ClientProfileSerializer()
#     amb_arrival = serializers.ReadOnlyField()
#     patient = PersonSerializer()
#     order_related_invoice = InvoiceSerializer()
#     # provider = ProvidersSerializer()
#     order_extra_services = extraServicesSerializer(required=False, many=True, read_only=True)
#
#     class Meta:
#         model = Order
#         fields = "__all__"

        # UserSimpleSerializer(required=False, many=True, read_only=True)