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
from orders.models import Order, Invoice, ExtraServices, AmbReport, Region, RegionPoint, City, CityPoint, SpecialLocation, SpecialLocationPoint
from orders.serializers import OrderSerializer, CreateOrderSerializer, GetOrdersSerializer, extraServicesSerializer, UpdateAmbReportSerializer
from rest_framework.response import Response
import requests
import json
from turfpy.measurement import boolean_point_in_polygon, area
from geojson import Point, MultiPolygon, Feature, Polygon
from django.core import serializers
# from turfpy.measurement import area
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
        order = Order.objects.get(id=serializer.data['id'])
        is_flat_rate = True


        gmaps = googlemaps.Client(key='AIzaSyDVWqaOxUtds5e2z9OBWf79q5IASU7uBIs')
        distance = gmaps.distance_matrix((from_location['lat'],from_location['lng']), (to_location['lat'],to_location['lng']), mode='driving')
        print('distance', type(distance))
        distance_in_kilo = round(distance['rows'][0]['elements'][0]['distance']['value'] / 1000, 1);
        duration_in_minutes = round(distance['rows'][0]['elements'][0]['duration']['value'] / 60, 0);
        print('distance_in_kilo', distance_in_kilo)
        print('duration_in_minutes', duration_in_minutes)
        cost = 0

        from_point = Point([from_location['lat'], from_location['lng']])
        to_point = Point([to_location['lat'], to_location['lng']])
        print('choosen from_point', from_point)
        print('choosen to_point', to_point)
        print('==============Update Region==============')
        allRegions = Region.objects.all()
        print('allRegions', allRegions)
        for region in allRegions:
            region_polygon_points = []
            region_related_points = RegionPoint.objects.filter(region=region)
            print('region_related_points', region_related_points)
            for region_point in region_related_points:
                print('point', region_point.lat, region_point.lng)
                region_polygon_points.append((region_point.lat, region_point.lng))
            print('polygon_points After', region_polygon_points)
            region_polygon = Polygon([region_polygon_points])
            if boolean_point_in_polygon(from_point, region_polygon):
                print("order['from_region'] 111", order.from_region)
                order.from_region = region
                order.save()
                print("order['from_region'] 222", order.from_region)
            if boolean_point_in_polygon(to_point, region_polygon):
                print("order['from_region'] 111", order.to_region)
                order.to_region = region
                order.save()
                print("order['from_region'] 222", order.to_region)
        print('order after updating regions:', order)


        print('==============Update City==============')
        allCities = City.objects.all()
        print('allCities', allCities)
        for city in allCities:
            city_polygon_points = []
            city_related_points = CityPoint.objects.filter(city=city)
            print('city_related_points', city_related_points)
            for city_point in city_related_points:
                print('point', city_point.lat, city_point.lng)
                city_polygon_points.append((city_point.lat, city_point.lng))
            print('polygon_points After', city_polygon_points)
            city_polygon = Polygon([city_polygon_points])
            if boolean_point_in_polygon(from_point, city_polygon):
                print("order['from_city'] 111", order.from_city)
                order.from_city = city
                order.save()
                print("order['from_city'] 222", order.from_city)
            if boolean_point_in_polygon(to_point, city_polygon):
                print("order['to_city'] 111", order.to_city)
                order.to_city = city
                order.save()
                print("order['to_city'] 222", order.to_city)
        print('==============Update Special Location==============')
        allSpecialLocations = SpecialLocation.objects.all()
        print('allSpecialLocations', allSpecialLocations)
        for special_location in allSpecialLocations:
            special_location_polygon_points = []
            special_location_related_points = SpecialLocationPoint.objects.filter(special_location=special_location)
            print('special_location_related_points', special_location_related_points)
            for special_location_point in special_location_related_points:
                print('point', special_location_point.lat, special_location_point.lng)
                special_location_polygon_points.append((special_location_point.lat, special_location_point.lng))
            print('polygon_points After', special_location_polygon_points)
            special_location_polygon = Polygon([special_location_polygon_points])
            if boolean_point_in_polygon(from_point, special_location_polygon):
                print("order['from_special_location'] 111", order.from_special_location)
                order.from_special_location = special_location
                order.save()
                print("order['from_special_location'] 222", order.from_special_location)
            if boolean_point_in_polygon(to_point, special_location_polygon):
                print("order['to_special_location'] 111", order.to_special_location)
                order.to_special_location = special_location
                order.save()
                print("order['to_special_location'] 222", order.to_special_location)
        print('order after updating regions:', order)
        serialized_obj = serializers.serialize('json', [order, ])
        print('serialized_obj', serialized_obj)


        print('==============Flat Cost Calculation================')
        if order.to_special_location and order.from_special_location and order.to_special_location.city == order.from_special_location.city:
            print('2 special locations', order.to_special_location, order.from_special_location)
            if (serializer.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = max(order.to_special_location.two_way_price, order.from_special_location.two_way_price)
            else:
                print("not round trip")
                cost = max(order.to_special_location.one_way_price, order.from_special_location.one_way_price)
        elif order.to_special_location and order.from_city == order.to_special_location.city:
            print('1 special locations to_special_location', order.to_special_location)
            if (serializer.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = order.to_special_location.two_way_price
            else:
                print("not round trip")
                cost = order.to_special_location.one_way_price
        elif order.from_special_location and order.to_city == order.from_special_location.city:
            print('1 special locations from_special_location', order.from_special_location)
            if (serializer.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = order.from_special_location.two_way_price
            else:
                print("not round trip")
                cost = order.from_special_location.one_way_price
        else:
            is_flat_rate = False
            print('No Special Locations')
            if (serializer.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = ((distance_in_kilo * 5) + (duration_in_minutes * 3) + 200) * 1.5 + 50 * serializer.data[
                    'waiting_time']
            else:
                print("not round trip")
                cost = (distance_in_kilo * 5) + (duration_in_minutes * 3) + 200







        print('==========================================')
        if is_flat_rate:
            cost_after_vat = cost
        else:
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


# class paymentInfo_view(views.APIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request, paymentId):
#         if paymentId:
#             try:
#                 url = "https://api.tap.company/v2/authorize/" + paymentId
#                 payload = "{}"
#                 headers = {'authorization': 'Bearer sk_test_g5nBLfJUcuVE9mkTKezvlxMF'}
#                 response = requests.request("GET", url, data=payload, headers=headers)
#             except Exception as e:
#                 print('errror', e)
#                 return Response(e)
#         return Response(response.text)
