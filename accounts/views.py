from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView

from accounts.models import User, Person, ProviderProfile, ClientProfile
from rest_framework import viewsets, generics, views, permissions, status
from accounts.serializers import UserSerializer, RegistrationSerializer, PersonSerializer, ProvidersSerializer, UpdateProviderAvailabilityViewSerializer, ClientProfileSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.http.response import HttpResponseNotAllowed
# Create your views here.
from orders.models import Order


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class AllClientProfilesView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ClientProfileSerializer

    def get_queryset(self):
        return ClientProfile.objects.all()


class GetPersonsOfUserViewByPhone(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PersonSerializer
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        # client_profile = Client.objects.get(id=self.request.user.id)
        # print('USSSEERRR')
        # print(user)
        # thoughts_user_can_view = user.user_can_view.values().values_list('id', flat=True)
        # friends_list = Friend.objects.friends(user)
        print('teeeeeest')
        print('self.kwargs[phone_number]', self.kwargs['phone_number'])
        if self.kwargs['phone_number']:
            needed_user = User.objects.get(phone_number=self.kwargs['phone_number'])
            return Person.objects.filter(profile=needed_user.user_client_profile)
        return Person.objects.filter(profile=self.request.user.user_client_profile)

class GetPersonsOfUserView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PersonSerializer

        # pagination_class = PageNumberPagination

    def get_queryset(self):
        return Person.objects.filter(profile=self.request.user.user_client_profile)

    # GetAvailableProvider
class GetAvailableProviderView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProvidersSerializer
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        # client_profile = Client.objects.get(id=self.request.user.id)
        # print('USSSEERRR')
        # print(user)
        # thoughts_user_can_view = user.user_can_view.values().values_list('id', flat=True)
        # friends_list = Friend.objects.friends(user)
        # print('provider_related_orders', self);
        print('self:', self.kwargs['order_id'])
        current_order = Order.objects.get(id=self.kwargs['order_id'])
        # Compare all related orders on the same day and if they conflict with the current one
        providers = ProviderProfile.objects.filter(is_available=True)
        for provider in providers:
            # print('provider_related_orders', provider, provider.__dict__, provider.provider_related_orders)
            related_orders = Order.objects.filter(provider=provider)
            for related_order in related_orders:
                print('related_order.order_date', related_order.order_date)
                if(related_order.order_date == current_order.order_date):
                    print('FOUND ON THE SAME DATE')
                    if(related_order.arrival_time == current_order.arrival_time):

                        # print('test plus minus', (related_order.arrival_time + timedelta(hours=3)), related_order.arrival_time)
                        print('FOUND ON THE SAME Time', related_order.arrival_time, current_order.arrival_time)
                    else:
                        print("But not the same time", related_order.arrival_time, current_order.arrival_time)
                else:
                    print('Not on the same data')
                # print('related_order.arrival_time', related_order.arrival_time)
                # print('related_order.order_related_invoice.duration_value', related_order.order_related_invoice.duration_value)

        return providers

class CreatePersonView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

class UpdatePersonView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()



class DeletePersonView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

# class GetProvidelApproval(RetrieveAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = ProviderProfile.objects.all()
#     serializer_class = ProviderApprovalSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     thought = Thought.objects.get(id=serializer.data['id'])
    #     response_serializer = ThoughtPolymorphicSerializer(thought)
    #     return Response(response_serializer.data)


@api_view(['POST', ])
def registration_view(request):

    if request.method == 'POST':
        print('register request.data', request.data['platform'])
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['id'] = user.id
            token = Token.objects.get(user=user).key
            data['token'] = token
            if ((request.data['platform'] == 'client' and not user.isClient) or (request.data['platform'] == 'operation' and not user.isOperation) or (request.data['platform'] == 'provider' and not user.isProvider)):
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            data = serializer.errors
        return Response(data)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print('in CustomObtainAuthToken request', request.data)
        print('in CustomObtainAuthToken self', self.args)
        user = User.objects.get(phone_number=request.data['username'])
        if ((request.data['platform'] == 'client' and not user.isClient) or (
                request.data['platform'] == 'operation' and not user.isOperation) or (
                request.data['platform'] == 'provider' and not user.isProvider)):
            print('I entered the condition')
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        response = super(CustomObtainAuthToken, self).post(
            request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        print('heeeere', response.data, token)
        return Response({'token': token.key, 'id': token.user_id})


class UpdateUserPasswordView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # instance = User.objects.get(phone_number=request.user.phone_number)
        # print('I am inside update password and the platform is: ', request.data['platform'])
        # if ((request.data['platform'] == 'client' and not instance.isClient) or (
        #         request.data['platform'] == 'operation' and not instance.isOperation) or (
        #         request.data['platform'] == 'provider' and not instance.isProvider)):
        #     print('I entered the condition')
        #     return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        print('yeeeees in UPDAAATE password')
        # print('olllld pass', request.data['oldPassword'])
        # print('request.data.keys()', request.data.keys())
        if('oldPassword' in request.data.keys()):
            print('yeeeees in old password')
            print('olllld pass', request.data['oldPassword'])
            if(request.user.check_password(request.data['oldPassword'])):
                request.user.set_password(request.data['newPassword'])
                request.user.save()
                token = Token.objects.get(key=request.auth)
                return Response({'token': token.key, 'id': token.user_id})
            else:
                return Response({'error':'Incorrect old password'}, HttpResponseNotAllowed)
            # return Response({'error': 'Incorrect old password'}, HttpResponseNotAllowed)
        else:
            request.user.set_password(request.data['newPassword'])
            request.user.save()
            token = Token.objects.get(key=request.auth)
            return Response({'token': token.key, 'id': token.user_id})


class UpdateProviderAvailabilityView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProviderAvailabilityViewSerializer
    queryset = ProviderProfile.objects.all()