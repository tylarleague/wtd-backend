from accounts.models import User, ClientProfile, OperationProfile, ProviderProfile, Person, Organization
from orders.models import Order
from rest_framework import serializers
from datetime import datetime, timedelta



#
# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = "__all__"



class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number']


class ClientProfileSerializer(serializers.ModelSerializer):
    related_persons = serializers.SerializerMethodField()
    user = SimpleUserSerializer()

    def get_related_persons(self, profile):
        qs = Person.objects.filter(is_deleted=False, profile=profile)
        serializer = PersonSerializer(instance=qs, required=False, many=True, read_only=True)
        return serializer.data
    class Meta:
        model = ClientProfile
        fields = "__all__"

class OperationProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationProfile
        fields = "__all__"

class ProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    # user_client_profile = ClientProfileSerializer()
    user_client_profile = ClientProfileSerializer(required=False)
    user_operation_profile = OperationProfileSerializer(required=False)
    user_provider_profile = ProviderProfileSerializer(required=False)
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'isVerified', 'isClient', 'isOperation', 'isProvider', 'user_client_profile', 'user_operation_profile', 'user_provider_profile']
        extra_kwargs = {'password': {'write_only': True}}



class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'name', 'password', 'isClient', 'isOperation', 'isProvider']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.delete_at = (datetime.now() + timedelta(hours=24))
        user.save()

        return user

class ProvidersSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    organization = OrganizationSerializer()
    # provider_related_orders = OrderSerializer(required=False, many=True, read_only=True)
    class Meta:
        model = ProviderProfile
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    # related_persons = PersonSerializer(required=False, many=True, read_only=True)
    user = SimpleUserSerializer()
    class Meta:
        model = ClientProfile
        fields = "__all__"

class UpdateProviderAvailabilityViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = ['is_available']

# class ProviderApprovalSerializer(serializers.ModelSerializer):
#     # user = UserSerializer()
#     # organization = OrganizationSerializer()
#     # provider_related_orders = OrderSerializer(required=False, many=True, read_only=True)
#     class Meta:
#         model = ['approval']