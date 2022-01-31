from rest_framework import serializers

from accounts.models import ProviderProfile
from accounts.serializers import ClientProfileSerializer, PersonSerializer, ProvidersSerializer, UserSerializer, SimpleUserSerializer, ClientSerializer
from orders.models import Order, Invoice, ExtraServices, AmbReport


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # 12 characters are more than enough.
            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension,)
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    custom_id = serializers.ReadOnlyField()
    class Meta:
        model = Order
        fields = "__all__"

class extraServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraServices
        fields = ['service_cost', 'service_name']

class CreateOrderSerializer(serializers.ModelSerializer):
    custom_id = serializers.ReadOnlyField()
    appointment_approval = Base64ImageField(
        max_length=None, use_url=True, required=False)
    discharge_approval = Base64ImageField(
        max_length=None, use_url=True, required=False)
    class Meta:
        model = Order
        fields = "__all__"


class UpdateAmbReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmbReport
        fields = "__all__"

class GetOrdersSerializer(serializers.ModelSerializer):
    amb_arrival = serializers.ReadOnlyField()
    custom_id = serializers.ReadOnlyField()
    patient = PersonSerializer()
    order_related_invoice = InvoiceSerializer()
    provider = ProvidersSerializer()
    owner = ClientSerializer(required=False, read_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(source='provider', queryset=ProviderProfile.objects.all(), write_only=True, allow_null=True)
    order_extra_services = extraServicesSerializer(required=False, many=True, read_only=True)
    order_related_report = UpdateAmbReportSerializer()
    appointment_approval = Base64ImageField(
        max_length=None, use_url=True, required=False)
    discharge_approval = Base64ImageField(
        max_length=None, use_url=True, required=False)
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