import googlemaps as googlemaps
from django.shortcuts import render
import math
from rest_framework import views, permissions, status
# Create your views here.
from googlemaps.distance_matrix import distance_matrix
from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
import http.client
from orders.models import Order, Invoice, ExtraServices, AmbReport
from orders.serializers import OrderSerializer, CreateOrderSerializer, GetOrdersSerializer, extraServicesSerializer, UpdateAmbReportSerializer
from rest_framework.response import Response
import requests
import json
class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer




class CreateOrderView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderSerializer
    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        from_location = eval(serializer.data['from_location'])
        to_location = eval(serializer.data['to_location'])
        gmaps = googlemaps.Client(key='AIzaSyDVWqaOxUtds5e2z9OBWf79q5IASU7uBIs')
        distance = gmaps.distance_matrix((from_location['lat'],from_location['lng']), (to_location['lat'],to_location['lng']), mode='driving')
        print('distance', type(distance))
        distance_in_kilo = round(distance['rows'][0]['elements'][0]['distance']['value'] / 1000, 1);
        duration_in_minutes = round(distance['rows'][0]['elements'][0]['duration']['value'] / 60, 0);
        order = Order.objects.get(id=serializer.data['id'])
        # if(order.need_nurse):
        #     nurse_cost = 150
        # else:
        #     nurse_cost = 0
        print('distance_in_kilo', distance_in_kilo)
        print('duration_in_minutes', duration_in_minutes)
        cost = (distance_in_kilo * 5) + (duration_in_minutes * 3) + 200
        cost_after_vat = (115 * cost) / 100
        print('cost_after_vat', cost_after_vat)
        myInv = Invoice.objects.create(
            order=order,
            distance_value=distance['rows'][0]['elements'][0]['distance']['value'],
            distance_text = distance['rows'][0]['elements'][0]['distance']['text'],
            duration_value=distance['rows'][0]['elements'][0]['duration']['value'],
            duration_text=distance['rows'][0]['elements'][0]['duration']['text'],
            cost= cost_after_vat,
        )
        report = AmbReport.objects.create(order=order)
        print('myInv', myInv)
        print('report', report)
        response_serializer = GetOrdersSerializer(order)
        return Response(response_serializer.data)

@api_view(['POST', ])
def calculateCost_view(request):

    if request.method == 'POST':
        # print('from_location', request.data['from_location'])
        # print('register request.data', request.data['from_location'])
        # print('request.data', request.data)
        from_location = eval(request.data['from_location'])
        to_location = eval(request.data['to_location'])
        gmaps = googlemaps.Client(key='AIzaSyDVWqaOxUtds5e2z9OBWf79q5IASU7uBIs')
        distance = gmaps.distance_matrix((from_location['lat'], from_location['lng']),
                                         (to_location['lat'], to_location['lng']), mode='driving')
        print('distance', type(distance))
        distance_in_kilo = round(distance['rows'][0]['elements'][0]['distance']['value'] / 1000, 1);
        duration_in_minutes = round(distance['rows'][0]['elements'][0]['duration']['value'] / 60, 0);
        cost= (distance_in_kilo * 5) + (duration_in_minutes * 3) + 200
        print('distance_in_kilo', distance_in_kilo)
        print('duration_in_minutes', duration_in_minutes)
        cost_after_vat = (115 * cost) / 100
        print('cost_after_vat', cost_after_vat)
        data = {
            "distance": distance_in_kilo,
            "duration": duration_in_minutes,
            "total": cost_after_vat

        }
        return Response(data)


class GetOrdersOfUserView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetOrdersSerializer
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        # client_profile = Client.objects.get(id=self.request.user.id)
        # print('USSSEERRR')
        # print(user)
        # thoughts_user_can_view = user.user_can_view.values().values_list('id', flat=True)
        # friends_list = Friend.objects.friends(user)
        not_wanted_status = ['done', 'canceled']
        return Order.objects.filter(owner=self.request.user.user_client_profile, approved_by_client=True).exclude(status__in=not_wanted_status).order_by('order_date', 'arrival_time')


class GetDeletedDoneOrdersOfUserView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetOrdersSerializer
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        # client_profile = Client.objects.get(id=self.request.user.id)
        # print('USSSEERRR')
        # print(user)
        # thoughts_user_can_view = user.user_can_view.values().values_list('id', flat=True)
        # friends_list = Friend.objects.friends(user)
        wanted_status = ['done', 'canceled']
        return Order.objects.filter(owner=self.request.user.user_client_profile, approved_by_client=True, status__in=wanted_status).order_by('order_date', 'arrival_time')



# GetDeletedDoneOrdersOfUserView
    # GetOrdersOfAllApprevedByClients
class GetOrdersOperation(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetOrdersSerializer
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        # client_profile = Client.objects.get(id=self.request.user.id)
        # print('USSSEERRR')
        # print(user)
        # thoughts_user_can_view = user.user_can_view.values().values_list('id', flat=True)
        # friends_list = Friend.objects.friends(user)
        not_wanted_status = ['done', 'canceled']
        return Order.objects.filter(approved_by_client=True, payment_authorized=True).exclude(status__in=not_wanted_status).order_by('order_date', 'arrival_time')


class GetDeletedDoneOrdersOperation(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetOrdersSerializer
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        # client_profile = Client.objects.get(id=self.request.user.id)
        # print('USSSEERRR')
        # print(user)
        # thoughts_user_can_view = user.user_can_view.values().values_list('id', flat=True)
        # friends_list = Friend.objects.friends(user)
        wanted_status = ['done', 'canceled']
        return Order.objects.filter(approved_by_client=True, status__in=wanted_status).order_by('order_date', 'arrival_time')


# GetProviderPendingOrders
class GetOrdersProvider(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetOrdersSerializer
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        # client_profile = Client.objects.get(id=self.request.user.id)
        # print('USSSEERRR')
        # print(user)
        # thoughts_user_can_view = user.user_can_view.values().values_list('id', flat=True)
        # friends_list = Friend.objects.friends(user)
        not_wanted_status = ['done', 'canceled']
        return Order.objects.filter(provider=self.request.user.user_provider_profile, approved_by_client=True, payment_authorized=True).exclude(status__in=not_wanted_status).order_by('-created_at')


class GetDeletedDoneOrdersProvider(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetOrdersSerializer
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        # client_profile = Client.objects.get(id=self.request.user.id)
        # print('USSSEERRR')
        # print(user)
        # thoughts_user_can_view = user.user_can_view.values().values_list('id', flat=True)
        # friends_list = Friend.objects.friends(user)
        wanted_status = ['done', 'canceled']
        return Order.objects.filter(provider=self.request.user.user_provider_profile, approved_by_client=True, status__in=wanted_status).order_by('-created_at')

class ApproveOrderByClient(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetOrdersSerializer
    queryset = Order.objects.all()


# SendOrderToAmbView
class SendOrderToAmbView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetOrdersSerializer
    queryset = Order.objects.all()

class UpdateAmbReport(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateAmbReportSerializer
    queryset = AmbReport.objects.all()

class GetExtraServicesView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = extraServicesSerializer
    queryset = ExtraServices.objects.all()


class ActionOrderByProvider(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetOrdersSerializer
    queryset = Order.objects.all()

    # ActionOrderByOperation
class ActionOrderByOperation(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetOrdersSerializer
    queryset = Order.objects.all()


class paymentInfo_view(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, paymentId):
        if paymentId:
            try:
                url = "https://api.tap.company/v2/authorize/" + paymentId
                payload = "{}"
                headers = {'authorization': 'Bearer sk_test_g5nBLfJUcuVE9mkTKezvlxMF'}
                response = requests.request("GET", url, data=payload, headers=headers)
            except Exception as e:
                print('errror', e)
                return Response(e)
        return Response(response.text)
