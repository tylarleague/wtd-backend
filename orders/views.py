import googlemaps as googlemaps
from django.shortcuts import render
import math
from discounts.models import Discount
from rest_framework import views, permissions, status
# Create your views here.
from googlemaps.distance_matrix import distance_matrix
from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view,  authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
import http.client
from orders.models import Order, Invoice, ExtraServices, AmbReport, Region, RegionPoint, City, CityPoint, SpecialLocation, SpecialLocationPoint, OrderPossibleProvider
from orders.serializers import OrderSerializer, CreateOrderSerializer, GetOrdersSerializer, extraServicesSerializer, UpdateAmbReportSerializer
from rest_framework.response import Response
import requests
import json
from turfpy.measurement import boolean_point_in_polygon, area, nearest_point
from turfpy.measurement import nearest_point
from geojson import Point, Feature, FeatureCollection
from turfpy.measurement import centroid
from geojson import Point, MultiPolygon, Feature, Polygon, FeatureCollection
from django.core import serializers
from geojson import Point, Feature
# from ipyleaflet import Map, GeoJSON
from turfpy.transformation import circle
from turfpy.measurement import area
from accounts.models import ProviderProfile, User, Organization, OperationProfile
from django.db.models import Q
from datetime import datetime, timedelta
from unifonicnextgen.unifonicnextgen_client import UnifonicnextgenClient
from unifonicnextgen.configuration import Configuration
from unifonicnextgen.exceptions.api_exception import APIException
import heapq
from constance import config
import csv
from django.http import HttpResponse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse


basic_auth_user_name = 'e637a3df-8da4-4cd2-b524-5a5409e811f9'
basic_auth_password = '0UpBuW8KAxwOWkJn8Y7lKBbrFEz4aTFn87z3kFwwpWhFB3XJAec2Dn4BTeCakSlkdhGAfCbxkWK'
client = UnifonicnextgenClient(basic_auth_user_name, basic_auth_password)
rest_controller = client.rest
app_sid = 'Q0hq8Uu4tcJf1UcsgAP7DSCsP8VHil'
sender_id = 'WTDcare'
# body = 'رسااالة من وتد يلد'
recipient = 966562156104
response_type = 'JSON'
correlation_id = '""'
base_encode = True
status_callback = 'sent'


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

        gmaps = googlemaps.Client(
            key='AIzaSyDVWqaOxUtds5e2z9OBWf79q5IASU7uBIs')
        distance = gmaps.distance_matrix((from_location['lat'], from_location['lng']), (
            to_location['lat'], to_location['lng']), mode='driving')
        print('distance', type(distance))
        distance_in_kilo = round(
            distance['rows'][0]['elements'][0]['distance']['value'] / 1000, 1)
        duration_in_minutes = round(
            distance['rows'][0]['elements'][0]['duration']['value'] / 60, 0)
        print('distance_in_kilo', distance_in_kilo)
        print('duration_in_minutes', duration_in_minutes,
              type(duration_in_minutes))
        cost = 0

        from_point = Point([from_location['lat'], from_location['lng']])
        to_point = Point([to_location['lat'], to_location['lng']])
        print('choosen from_point', from_point)
        print('choosen to_point', to_point)
        print('==============Update Region==============')
        allRegions = Region.objects.all()
        allRegionsPolygons = []
        print('allRegions', allRegions)
        for region in allRegions:
            region_polygon_points = []
            region_related_points = RegionPoint.objects.filter(region=region)
            print('region_related_points', region_related_points)
            for region_point in region_related_points:
                print('point', region_point.lat, region_point.lng)
                region_polygon_points.append(
                    (region_point.lat, region_point.lng))
            print('polygon_points After', region_polygon_points)
            if (len(region_polygon_points)):
                region_polygon = Polygon([region_polygon_points])
                allRegionsPolygons.append((region, region_polygon))
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
            if (len(city_polygon_points)):
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
            special_location_related_points = SpecialLocationPoint.objects.filter(
                special_location=special_location)
            print('special_location_related_points',
                  special_location_related_points)
            for special_location_point in special_location_related_points:
                print('point', special_location_point.lat,
                      special_location_point.lng)
                special_location_polygon_points.append(
                    (special_location_point.lat, special_location_point.lng))
            print('polygon_points After', special_location_polygon_points)
            if (len(special_location_polygon_points)):
                special_location_polygon = Polygon(
                    [special_location_polygon_points])
                if boolean_point_in_polygon(from_point, special_location_polygon):
                    print("order['from_special_location'] 111",
                          order.from_special_location)
                    order.from_special_location = special_location
                    order.save()
                    print("order['from_special_location'] 222",
                          order.from_special_location)
                if boolean_point_in_polygon(to_point, special_location_polygon):
                    print("order['to_special_location'] 111",
                          order.to_special_location)
                    order.to_special_location = special_location
                    order.save()
                    print("order['to_special_location'] 222",
                          order.to_special_location)
        print('order after updating regions:', order)
        serialized_obj = serializers.serialize('json', [order, ])
        print('serialized_obj', serialized_obj)
        print('==============Assign Operator================')
        operator_region_temp = None
        # if there is a region, assign region operator. if there is no region, get operator of the closest region
        if order.from_region:
            print('inside order.from_region')
            order.operator = order.from_region.operator
            operator_region_temp = order.from_region
            order.save()
        else:
            print('get mid point of each region, then get the nearest to from location, the operator of that region will be the one for this')
            allRegionsCentroids = []
            allRegionsCentroidsWithRegions = []
            for poly_region in allRegionsPolygons:
                print('poly_region', poly_region)
                print('centroid(poly_region)', centroid(poly_region[1]))
                allRegionsCentroids.append(centroid(poly_region[1]))
                allRegionsCentroidsWithRegions.append(
                    (poly_region[0], centroid(poly_region[1])))
            fc = FeatureCollection(allRegionsCentroids)
            print('nearest_point(from_point, fc)',
                  nearest_point(from_point, fc))
            print('allRegionsCentroidsWithRegions',
                  allRegionsCentroidsWithRegions)
            for cent_with_region in allRegionsCentroidsWithRegions:
                print('$$$FIRST$$$', cent_with_region[1].geometry.coordinates)
                print('$$$SECOND$$$', nearest_point(
                    from_point, fc).geometry.coordinates)
                if cent_with_region[1].geometry.coordinates == nearest_point(from_point, fc).geometry.coordinates:
                    print('they are equaaaaaal', cent_with_region[0].operator)
                    order.operator = cent_with_region[0].operator
                    order.save()
                    operator_region_temp = cent_with_region[0]
            print('operator is:', order.operator, 'FROM', operator_region_temp)
        print('==============Flat Cost Calculation================')
        if order.to_special_location and order.from_special_location and order.to_special_location.city == order.from_special_location.city:
            print('2 special locations', order.to_special_location,
                  order.from_special_location)
            if (serializer.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = max(order.to_special_location.two_way_price,
                           order.from_special_location.two_way_price)
            else:
                print("not round trip")
                cost = max(order.to_special_location.one_way_price,
                           order.from_special_location.one_way_price)
        elif order.to_special_location and order.from_city == order.to_special_location.city:
            print('1 special locations to_special_location',
                  order.to_special_location)
            if (serializer.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = order.to_special_location.two_way_price
            else:
                print("not round trip")
                cost = order.to_special_location.one_way_price
        elif order.to_special_location:
            print('1 special locations to_special_location',
                  order.to_special_location)
            if (serializer.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = order.to_special_location.special_price + ((distance_in_kilo * getattr(config, 'KILO_PRICE')) + (duration_in_minutes * getattr(config, 'MINUTE_PRICE')) + getattr(config, 'STARTING_PRICE')) * getattr(config, 'ROUND_TRIP_RATIO') + getattr(config, 'WAITING_PRICE') * serializer.data[
                    'waiting_time']
            else:
                print("not round trip")
                cost = order.to_special_location.special_price + (distance_in_kilo * getattr(config, 'KILO_PRICE')) + (
                    duration_in_minutes * getattr(config, 'MINUTE_PRICE')) + getattr(config, 'STARTING_PRICE')
        elif order.from_special_location and order.to_city == order.from_special_location.city:
            print('1 special locations from_special_location',
                  order.from_special_location)
            if (serializer.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = order.from_special_location.two_way_price
            else:
                print("not round trip")
                cost = order.from_special_location.one_way_price
        elif order.from_special_location:
            print('1 special locations to_special_location',
                  order.from_special_location)
            if (serializer.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = order.from_special_location.special_price + ((distance_in_kilo * getattr(config, 'KILO_PRICE')) + (duration_in_minutes * getattr(config, 'MINUTE_PRICE')) + getattr(config, 'STARTING_PRICE')) * getattr(config, 'ROUND_TRIP_RATIO') + getattr(config, 'WAITING_PRICE') * serializer.data[
                    'waiting_time']
            else:
                print("not round trip")
                cost = order.from_special_location.special_price + (distance_in_kilo * getattr(config, 'KILO_PRICE')) + (
                    duration_in_minutes * getattr(config, 'MINUTE_PRICE')) + getattr(config, 'STARTING_PRICE')
        else:
            is_flat_rate = False
            print('No Special Locations')
            if (serializer.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = ((distance_in_kilo * getattr(config, 'KILO_PRICE')) + (duration_in_minutes * getattr(config, 'MINUTE_PRICE')) + getattr(config, 'STARTING_PRICE')) * getattr(config, 'ROUND_TRIP_RATIO') + getattr(config, 'WAITING_PRICE') * serializer.data[
                    'waiting_time']
            else:
                print("not round trip")
                cost = (distance_in_kilo * getattr(config, 'KILO_PRICE')) + (duration_in_minutes *
                                                                             getattr(config, 'MINUTE_PRICE')) + getattr(config, 'STARTING_PRICE')
        print('==========================================')
        if is_flat_rate:
            cost_after_vat = cost
        else:
            cost_after_vat = (115 * cost) / 100
            print('cost_after_vat', cost_after_vat)
        final_cost = cost_after_vat
        try:
            if request.data['cost']:
                final_cost = request.data['cost']
        except:
            print("no cost")
        myInv = Invoice.objects.create(
            order=order,
            distance_value=distance['rows'][0]['elements'][0]['distance']['value'],
            distance_text=distance['rows'][0]['elements'][0]['distance']['text'],
            duration_value=distance['rows'][0]['elements'][0]['duration']['value'],
            duration_text=distance['rows'][0]['elements'][0]['duration']['text'],
            cost=final_cost,
            initial_cost=cost_after_vat
        )
        report = AmbReport.objects.create(order=order)
        print('myInv', myInv)
        print('report', report)

        print('===========Automate to Provider============')

        create_order_providers(order, from_location['lat'], from_location['lng'],
                               to_location['lat'], to_location['lng'], duration_in_minutes)
        print('===========FINSH Automate to Provider============')
        response_serializer = GetOrdersSerializer(order)

        if ('isCreatedInOperation' in request.data.keys() and request.data['isCreatedInOperation'] and order.send_sms):
            requestBody = {
                "draft": False,
                "due": int((datetime.now() + timedelta(minutes=1)).timestamp() * 1000),
                "expiry": int((datetime.now() + timedelta(hours=24)).timestamp() * 1000),
                "description": "delivery on " + str(order.order_date) + " invoice",
                "mode": "INVOICE",
                "note":  "delivery on " + str(order.order_date),
                "notifications": {
                    "channels": [
                        "SMS",
                        "EMAIL"
                    ],
                    "dispatch": True
                },
                "currencies": [
                    "SAR"
                ],
                "metadata": {
                    "udf1": "1",
                    "udf2": "2",
                    "udf3": "3"
                },
                "charge": {
                    "receipt": {
                        "email": True,
                        "sms": True
                    },
                    "statement_descriptor": "delivery on "+str(order.order_date)
                },
                "customer": {
                    "email": "payment.wtd.care@gmail.com",
                    "first_name": order.owner.user.name,
                    "last_name": "",
                    "middle_name": "",
                    "phone": {
                        "country_code": "966",
                        "number": order.owner.user.phone_number
                    }
                },
                "order": {
                    "amount": float("{:.2f}".format(myInv.cost)),
                    "currency": "SAR",
                    "items": [
                        {
                            "amount": float("{:.2f}".format(myInv.cost)),
                            "currency": "SAR",
                            "description": "delivery on " + str(order.order_date),
                            "discount": {
                                "type": "P",
                                "value": 0
                            },
                            "image": "",
                            "name": "Delivery "+order.custom_id,
                            "quantity": 1
                        }
                    ]
                },
                "payment_methods": [
                    ""
                ],
                "post": {
                    "url": "https://backend.wtd.care/add/payment"
                },
                "redirect": {
                    "url": "https://backend.wtd.care/add/payment?order_id="+str(order.id)
                },
                "reference": {
                    "invoice": "trans_"+order.custom_id,
                    "order": "order_"+order.custom_id
                }
            }

            payload = json.dumps(requestBody)
            headers = {
                'authorization': "Bearer sk_live_snIkgH9ATpYZMLzl4Sw73rhX",
                'content-type': "application/json",
                'lang_code': 'ar'
            }
            url = "https://api.tap.company/v2/invoices"
            response = requests.request(
                "POST", url, data=payload, headers=headers)
            data = json.loads(response.text)
            print(data)
        return Response(response_serializer.data)


def create_order_providers(order, from_location_lat, from_location_lng, to_location_lat, to_location_lng, duration_in_minutes):
    gmaps = googlemaps.Client(key='AIzaSyDVWqaOxUtds5e2z9OBWf79q5IASU7uBIs')
    center_circle_from_location = Feature(
        geometry=Point((from_location_lat, from_location_lng)))
    circle_of_from_location = circle(center_circle_from_location, radius=getattr(
        config, 'PICKUP_SEARCH_RADIUS'), steps=10, units='km')
    allOrganizations = Organization.objects.all()
    orgsWithinRange = []
    for currentOrg in allOrganizations:
        print('testing OrgLocation', currentOrg, currentOrg.lat)
        if currentOrg.lat and currentOrg.lng:
            currentOrgLocation = Point([currentOrg.lat, currentOrg.lng])
            if boolean_point_in_polygon(currentOrgLocation, circle_of_from_location):
                print('ORG WITHIN RANGE', currentOrgLocation)
                org_to_pickup_distance = gmaps.distance_matrix((currentOrg.lat, currentOrg.lng),
                                                               (from_location_lat,
                                                                from_location_lng),
                                                               mode='driving')
                org_to_pickup_duration_in_minutes = round(
                    org_to_pickup_distance['rows'][0]['elements'][0]['duration']['value'] / 60, 0)
                my_arrival_time_temp = datetime.strptime(
                    str(order.arrival_time), "%H:%M:%S")
                pickup_dropoff_operation_duration = getattr(
                    config, 'PICKUP_DROPOFF_OPERATION_IN_MINUTES')
                full_duration_before = org_to_pickup_duration_in_minutes + float(
                    duration_in_minutes) + pickup_dropoff_operation_duration
                time_block_start = (
                    my_arrival_time_temp - timedelta(minutes=full_duration_before)).time()
                if order.order_type == 'ONE_WAY':
                    dropoff_to_org_distance = gmaps.distance_matrix((to_location_lat, to_location_lng),
                                                                    (currentOrg.lat, currentOrg.lng), mode='driving')
                    dropoff_to_org_duration_in_minutes = round(
                        dropoff_to_org_distance['rows'][0]['elements'][0]['duration']['value'] / 60, 0)
                    time_block_end = (
                        my_arrival_time_temp + timedelta(minutes=dropoff_to_org_duration_in_minutes)).time()
                else:
                    full_duration_after = (order.waiting_time * 60) + (pickup_dropoff_operation_duration*3) + float(
                        duration_in_minutes) + org_to_pickup_duration_in_minutes
                    time_block_end = (
                        my_arrival_time_temp + timedelta(minutes=full_duration_after)).time()

                orgtuple = (currentOrg, org_to_pickup_duration_in_minutes,
                            time_block_start, time_block_end)
                orgsWithinRange.append(orgtuple)
    # print('allOrganizations', allOrganizations, len(allOrganizations))
    # print('orgsWithinRange', orgsWithinRange, len(orgsWithinRange))
    sortedOrgsWithinRange = sorted(
        orgsWithinRange, key=lambda distance_from_location: distance_from_location[1])
    print('sortedOrgsWithinRange', sortedOrgsWithinRange,
          len(sortedOrgsWithinRange))
    for currentOrgWithinRange in sortedOrgsWithinRange:
        for currentProvider in currentOrgWithinRange[0].organization_providers.all():
            add_provider = True
            print('currentProvider for currentOrWithinRange',
                  currentProvider, "-", currentOrgWithinRange)
            provider_orders_for_that_day = currentProvider.provider_related_orders.filter(
                Q(order_date=order.order_date) & Q(approved_by_client=True) & Q(payment_authorized=True))
            print('provider_orders_for_that_day', provider_orders_for_that_day)
            if provider_orders_for_that_day.exists():
                for order_of_provider in provider_orders_for_that_day:
                    print('order_of_provider', order_of_provider.arrival_time, currentOrgWithinRange[2],
                          currentOrgWithinRange[3])
                    if order_of_provider.order_block_start and order_of_provider.order_block_end:
                        # call the overlap function
                        if check_time_block_overlap(order_of_provider.order_block_start, order_of_provider.order_block_end, currentOrgWithinRange[2], currentOrgWithinRange[3]):
                            print('time block overlap!')
                            add_provider = False
                    else:
                        if time_in_range(currentOrgWithinRange[2], currentOrgWithinRange[3],
                                         order_of_provider.arrival_time):
                            print('inside time range!')
                            add_provider = False
                if add_provider:
                    print('not inside time range, I will add provider')
                    OrderPossibleProvider.objects.create(order=order, provider=currentProvider,
                                                         importance=create_provider_score(currentOrgWithinRange[1],
                                                                                          currentOrgWithinRange[
                                                                                              0].percentage))
            else:
                print('no orders that day, so I will add provider')
                OrderPossibleProvider.objects.create(order=order, provider=currentProvider,
                                                     importance=create_provider_score(currentOrgWithinRange[1],
                                                                                      currentOrgWithinRange[
                                                                                          0].percentage))
    # order_sorted_providers = order.order_possible_providers.all().order_by('-importance')
    # print('sortedProvidersFromDB', order_sorted_providers, len(order_sorted_providers))


# def send_order_to_provider(order):
#     order_sorted_providers = order.order_possible_providers.all().order_by('-importance')
#     if order_sorted_providers:
#         print('sortedProvidersFromDB', order_sorted_providers, len(order_sorted_providers))
#         if order.provider:
#             #Remove Old Provider
#             order.provider = None
#             print('order_sorted_providers.first()', order_sorted_providers.first())
#     else:
#         print('No Possible Providers! Assign manually')


def create_provider_score(provider_distance, provider_percentage, emergency=False):
    """Return provider score"""
    distance_importance = 0.4
    percentage_importance = 0.6
    provider_distance_capped = (100*provider_distance)/30
    wtd_percentage = 100-provider_percentage
    if emergency:
        print('Order is Emergency')
        distance_importance = 0.9
        percentage_importance = 0.1
    return ((provider_distance_capped * distance_importance) + (wtd_percentage*percentage_importance))/2


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def check_time_block_overlap(s1, e1, s2, e2):
    print('inside check_time_block_overlap')
    if s1 <= e1:
        return s1 <= s2 <= e1 or s1 <= e2 <= e1
    else:
        return s1 <= s2 or s2 <= e1 or s1 <= e2 or e2 <= e1


@api_view(['POST', ])
def calculateCost_view(request):
    if request.method == 'POST':
        print('request', request.data)
        from_location = eval(request.data['from_location'])
        to_location = eval(request.data['to_location'])
        final_from_region = None
        final_to_region = None
        final_from_city = None
        final_to_city = None
        final_from_special = None
        final_to_special = None
        is_flat_rate = True

        gmaps = googlemaps.Client(
            key='AIzaSyDVWqaOxUtds5e2z9OBWf79q5IASU7uBIs')
        distance = gmaps.distance_matrix((from_location['lat'], from_location['lng']), (
            to_location['lat'], to_location['lng']), mode='driving')
        print('distance', type(distance))
        distance_in_kilo = round(
            distance['rows'][0]['elements'][0]['distance']['value'] / 1000, 1)
        duration_in_minutes = round(
            distance['rows'][0]['elements'][0]['duration']['value'] / 60, 0)
        print('distance_in_kilo', distance_in_kilo)
        print('duration_in_minutes', duration_in_minutes)
        cost = 0

        from_point = Point([from_location['lat'], from_location['lng']])
        to_point = Point([to_location['lat'], to_location['lng']])
        print('choosen from_point', from_point)
        print('choosen to_point', to_point)
        print('==============Update Region==============')
        allRegions = Region.objects.all()
        allRegionsPolygons = []
        print('allRegions', allRegions)
        for region in allRegions:
            region_polygon_points = []
            region_related_points = RegionPoint.objects.filter(region=region)
            print('region_related_points', region_related_points)
            for region_point in region_related_points:
                print('point', region_point.lat, region_point.lng)
                region_polygon_points.append(
                    (region_point.lat, region_point.lng))
            print('polygon_points After', region_polygon_points)
            region_polygon = Polygon([region_polygon_points])
            allRegionsPolygons.append((region, region_polygon))
            if boolean_point_in_polygon(from_point, region_polygon):
                print("order['from_region'] 111", final_from_region)
                final_from_region = region
                # order.save()
                print("order['from_region'] 222", final_from_region)
            if boolean_point_in_polygon(to_point, region_polygon):
                print("order['from_region'] 111", final_to_region)
                final_to_region = region
                # order.save()
                print("order['from_region'] 222", final_to_region)
        print('order after updating regions:',
              final_from_region, final_to_region)

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
                print("order['from_city'] 111", final_from_city)
                final_from_city = city
                # order.save()
                print("order['from_city'] 222", final_from_city)
            if boolean_point_in_polygon(to_point, city_polygon):
                print("order['to_city'] 111", final_to_city)
                final_to_city = city
                # order.save()
                print("order['to_city'] 222",  final_to_city)
        print('==============Update Special Location==============')
        allSpecialLocations = SpecialLocation.objects.all()
        print('allSpecialLocations', allSpecialLocations)
        for special_location in allSpecialLocations:
            special_location_polygon_points = []
            special_location_related_points = SpecialLocationPoint.objects.filter(
                special_location=special_location)
            print('special_location_related_points',
                  special_location_related_points)
            for special_location_point in special_location_related_points:
                print('point', special_location_point.lat,
                      special_location_point.lng)
                special_location_polygon_points.append(
                    (special_location_point.lat, special_location_point.lng))
            print('polygon_points After', special_location_polygon_points)
            special_location_polygon = Polygon(
                [special_location_polygon_points])
            if boolean_point_in_polygon(from_point, special_location_polygon):
                print("order['from_special_location'] 111",
                      final_from_special)
                final_from_special = special_location
                # order.save()
                print("order['from_special_location'] 222", final_from_special)
            if boolean_point_in_polygon(to_point, special_location_polygon):
                print("order['to_special_location'] 111", final_to_special)
                final_to_special = special_location
                # order.save()
                print("order['to_special_location'] 222", final_to_special)
        print('order after updating regions:',
              final_from_special, final_to_special)
        # serialized_obj = serializers.serialize('json', [order, ])
        # print('serialized_obj', serialized_obj)

        print('==============Flat Cost Calculation================')
        if final_to_special and final_from_special and final_to_special.city == final_from_special.city:
            print('2 special locations', final_to_special, final_to_special)
            if (request.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = max(final_to_special.two_way_price,
                           final_from_special.two_way_price)
            else:
                print("not round trip")
                cost = max(final_to_special.one_way_price,
                           final_from_special.one_way_price)
        elif final_to_special and final_from_city == final_to_special.city:
            print('1 special locations to_special_location', final_to_special)
            if (request.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = final_to_special.two_way_price
            else:
                print("not round trip")
                cost = final_to_special.one_way_price
        elif final_to_special:
            print('1 special locations to_special_location', final_to_special)
            if (request.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = final_to_special.special_price + ((distance_in_kilo * getattr(config, 'KILO_PRICE')) + (duration_in_minutes * getattr(config, 'MINUTE_PRICE')) + getattr(config, 'STARTING_PRICE')) * getattr(config, 'ROUND_TRIP_RATIO') + getattr(config, 'WAITING_PRICE') * int(request.data[
                    'waiting_time'])
            else:
                print("not round trip")
                cost = final_to_special.special_price + (distance_in_kilo * getattr(config, 'KILO_PRICE')) + (
                    duration_in_minutes * getattr(config, 'MINUTE_PRICE')) + getattr(config, 'STARTING_PRICE')
        elif final_from_special and final_to_city == final_from_special.city:
            print('1 special locations from_special_location', final_from_special)
            if (request.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = final_from_special.two_way_price
            else:
                print("not round trip")
                cost = final_from_special.one_way_price
        elif final_from_special:
            print('1 special locations to_special_location', final_from_special)
            if (request.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = final_from_special.special_price + ((distance_in_kilo * getattr(config, 'KILO_PRICE')) + (duration_in_minutes * getattr(config, 'MINUTE_PRICE')) + getattr(config, 'STARTING_PRICE')) * getattr(config, 'ROUND_TRIP_RATIO') + getattr(config, 'WAITING_PRICE') * int(request.data[
                    'waiting_time'])
            else:
                print("not round trip")
                cost = final_from_special.special_price + (distance_in_kilo * getattr(config, 'KILO_PRICE')) + (
                    duration_in_minutes * getattr(config, 'MINUTE_PRICE')) + getattr(config, 'STARTING_PRICE')
        else:
            is_flat_rate = False
            print('No Special Locations')
            if (request.data['order_type'] == "ROUND_TRIP"):
                print("is round trip")
                cost = ((distance_in_kilo * getattr(config, 'KILO_PRICE')) + (duration_in_minutes * getattr(config, 'MINUTE_PRICE')) + getattr(config, 'STARTING_PRICE')) * getattr(config, 'ROUND_TRIP_RATIO') + getattr(config, 'WAITING_PRICE') * int(request.data[
                    'waiting_time'])
            else:
                print("not round trip")
                cost = (distance_in_kilo * getattr(config, 'KILO_PRICE')) + (duration_in_minutes *
                                                                             getattr(config, 'MINUTE_PRICE')) + getattr(config, 'STARTING_PRICE')
        print('==========================================')
        if is_flat_rate:
            cost_after_vat = cost
        else:
            cost_after_vat = (115 * cost) / 100
            print('cost_after_vat', cost_after_vat)
        final_cost = cost_after_vat
        try:
            if request.data['cost']:
                final_cost = request.data['cost']
        except:
            print("no cost")
        # myInv = Invoice.objects.create(
        #     order=order,
        #     distance_value=distance['rows'][0]['elements'][0]['distance']['value'],
        #     distance_text = distance['rows'][0]['elements'][0]['distance']['text'],
        #     duration_value=distance['rows'][0]['elements'][0]['duration']['value'],
        #     duration_text=distance['rows'][0]['elements'][0]['duration']['text'],
        #     cost= final_cost,
        #     initial_cost=cost_after_vat
        # )
        # report = AmbReport.objects.create(order=order)
        # print('myInv', myInv)
        # print('report', report)
        # response_serializer = GetOrdersSerializer(order)
        # return Response(response_serializer.data)
        data = {
            "distance": distance_in_kilo,
            "duration": duration_in_minutes,
            "total": final_cost

        }
        return Response(data)


@api_view(['POST', ])
def calculateCost_viewold(request):

    if request.method == 'POST':
        from_location = eval(request.data['from_location'])
        to_location = eval(request.data['to_location'])
        # print('from_location', request.data['from_location'])
        # print('register request.data', request.data['from_location'])
        # print('request.data', request.data)
        from_location = eval(request.data['from_location'])
        to_location = eval(request.data['to_location'])
        gmaps = googlemaps.Client(
            key='AIzaSyDVWqaOxUtds5e2z9OBWf79q5IASU7uBIs')
        distance = gmaps.distance_matrix((from_location['lat'], from_location['lng']),
                                         (to_location['lat'], to_location['lng']), mode='driving')
        print('distance', type(distance))
        distance_in_kilo = round(
            distance['rows'][0]['elements'][0]['distance']['value'] / 1000, 1)
        duration_in_minutes = round(
            distance['rows'][0]['elements'][0]['duration']['value'] / 60, 0)
        cost = (distance_in_kilo * getattr(config, 'KILO_PRICE')) + (duration_in_minutes *
                                                                     getattr(config, 'MINUTE_PRICE')) + getattr(config, 'STARTING_PRICE')
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
        return Order.objects.filter(approved_by_client=True).exclude(status__in=not_wanted_status).order_by('order_date', 'arrival_time')


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

    def perform_update(self, serializer):
        # print('test***************', self.kwargs['pk'], self.request.data['payment_authorized'])
        # print('payment_authorized of serialized', serializer.data['payment_authorized'])
        current_order = Order.objects.get(id=self.kwargs['pk'])
        # print('payment_authorized of current_order', current_order.payment_authorized)
        order_sorted_providers = current_order.order_possible_providers.all().order_by('-importance')
        # if self.request.data['payment_authorized'] == True and current_order.payment_authorized == False:
        # if self.request.data['status'] == 'canceled':
        #     delete_all_related_order_providers(current_order)
        print(type(self.request.data), self.request.data.keys())
        if ('payment_authorized' in self.request.data.keys() or 'is_approved_by_operation' in self.request.data.keys()):
            if ('payment_authorized' in self.request.data.keys() and self.request.data['payment_authorized'] == True and current_order.payment_authorized == False and current_order.is_approved_by_operation):
                while order_sorted_providers:
                    print('sortedProvidersFromDB', order_sorted_providers,
                          len(order_sorted_providers))
                    if order_sorted_providers.first().provider.is_available:
                        serializer.save(provider=order_sorted_providers.first().provider, order_block_start=order_sorted_providers.first(
                        ).order_block_start, order_block_end=order_sorted_providers.first().order_block_end, status='sent_to_provider')
                        OrderPossibleProvider.objects.get(
                            id=order_sorted_providers.first().id).delete()
                        sendSMS(current_order.custom_id, current_order.operator.user.phone_number,
                                getattr(config, 'SMS_OPERATION_AUTO_ASSIGN_AR'),
                                getattr(config, 'SMS_OPERATION_AUTO_ASSIGN_EN'))
                        break
                    else:
                        OrderPossibleProvider.objects.get(
                            id=order_sorted_providers.first().id).delete()
                        order_sorted_providers = current_order.order_possible_providers.all().order_by('-importance')
                        # order.save()
                else:
                    serializer.save(
                        provider=None, order_block_start=None, order_block_end=None)
                    print('No Possible Providers! Assign manually')
                    if current_order.operator:
                        sendSMS(current_order.custom_id, current_order.operator.user.phone_number,
                                getattr(
                                    config, 'SMS_OPERATION_NO_AUTO_ASSIGN_AR'),
                                getattr(config, 'SMS_OPERATION_NO_AUTO_ASSIGN_EN'))
                    else:
                        for operation_profile in OperationProfile.objects.all():
                            if operation_profile.is_available is True:
                                print('operation_profile',
                                      operation_profile.user.phone_number)
                                sendSMS(current_order.custom_id, operation_profile.user.phone_number,
                                        getattr(
                                            config, 'SMS_OPERATION_NO_AUTO_ASSIGN_AR'),
                                        getattr(config, 'SMS_OPERATION_NO_AUTO_ASSIGN_EN'))
            elif ('is_approved_by_operation' in self.request.data.keys() and self.request.data['is_approved_by_operation'] == True and current_order.is_approved_by_operation == False and current_order.payment_authorized):
                while order_sorted_providers:
                    print('sortedProvidersFromDB', order_sorted_providers,
                          len(order_sorted_providers))
                    if order_sorted_providers.first().provider.is_available:
                        serializer.save(provider=order_sorted_providers.first().provider, order_block_start=order_sorted_providers.first(
                        ).order_block_start, order_block_end=order_sorted_providers.first().order_block_end, status='sent_to_provider')
                        OrderPossibleProvider.objects.get(
                            id=order_sorted_providers.first().id).delete()
                        sendSMS(current_order.custom_id, current_order.operator.user.phone_number,
                                getattr(config, 'SMS_OPERATION_AUTO_ASSIGN_AR'),
                                getattr(config, 'SMS_OPERATION_AUTO_ASSIGN_EN'))
                        break
                    else:
                        OrderPossibleProvider.objects.get(
                            id=order_sorted_providers.first().id).delete()
                        order_sorted_providers = current_order.order_possible_providers.all().order_by('-importance')
                        # order.save()
                else:
                    serializer.save(
                        provider=None, order_block_start=None, order_block_end=None)
                    print('No Possible Providers! Assign manually')
                    if current_order.operator:
                        sendSMS(current_order.custom_id, current_order.operator.user.phone_number,
                                getattr(
                                    config, 'SMS_OPERATION_NO_AUTO_ASSIGN_AR'),
                                getattr(config, 'SMS_OPERATION_NO_AUTO_ASSIGN_EN'))
                    else:
                        for operation_profile in OperationProfile.objects.all():
                            if operation_profile.is_available is True:
                                print('operation_profile',
                                      operation_profile.user.phone_number)
                                sendSMS(current_order.custom_id, operation_profile.user.phone_number,
                                        getattr(
                                            config, 'SMS_OPERATION_NO_AUTO_ASSIGN_AR'),
                                        getattr(config, 'SMS_OPERATION_NO_AUTO_ASSIGN_EN'))
            else:
                serializer.save()
        else:
            serializer.save()


# def send_order_to_provider(order):
#     order_sorted_providers = order.order_possible_providers.all().order_by('-importance')
#     if order_sorted_providers:
#         print('sortedProvidersFromDB', order_sorted_providers, len(order_sorted_providers))
#         if order_sorted_providers.first().provider:
#             order.provider= order_sorted_providers.first().provider
#             order.status = 'sent_to_provider'
#             OrderPossibleProvider.objects.get(id=order_sorted_providers.first().id).delete()
#             order.save()
#     else:
#         order.provider = None
#         order.save()
#         print('No Possible Providers! Assign manually')


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

    def perform_update(self, serializer):
        # print('test***************', self.kwargs['pk'], self.request.data['payment_authorized'])
        # print('payment_authorized of serialized', serializer.data['payment_authorized'])
        current_order = Order.objects.get(id=self.kwargs['pk'])
        print('payment_authorized of current_order',
              current_order.payment_authorized)
        order_sorted_providers = current_order.order_possible_providers.all().order_by('-importance')
        if self.request.data['status'] == 'done':
            delete_all_related_order_providers(current_order)
        if self.request.data['status'] == 'rejected_by_provider':
            while order_sorted_providers:
                print('sortedProvidersFromDB', order_sorted_providers,
                      len(order_sorted_providers))
                if order_sorted_providers.first().provider.is_available:
                    serializer.save(provider=order_sorted_providers.first().provider, order_block_start=order_sorted_providers.first(
                    ).order_block_start, order_block_end=order_sorted_providers.first().order_block_end, status='sent_to_provider')
                    OrderPossibleProvider.objects.get(
                        id=order_sorted_providers.first().id).delete()
                    break
                else:
                    OrderPossibleProvider.objects.get(
                        id=order_sorted_providers.first().id).delete()
                    order_sorted_providers = current_order.order_possible_providers.all().order_by('-importance')
            else:
                serializer.save(
                    provider=None, order_block_start=None, order_block_end=None)
                print('No Possible Providers! Assign manually')
                if current_order.operator:
                    sendSMS(current_order.custom_id, current_order.operator.user.phone_number, getattr(config, 'SMS_OPERATION_NO_AUTO_ASSIGN_AR'),
                            getattr(config, 'SMS_OPERATION_NO_AUTO_ASSIGN_EN'))
                else:
                    for operation_profile in OperationProfile.objects.all():
                        if operation_profile.is_available is True:
                            print('operation_profile',
                                  operation_profile.user.phone_number)
                            sendSMS(current_order.custom_id, operation_profile.user.phone_number,
                                    getattr(
                                        config, 'SMS_OPERATION_NO_AUTO_ASSIGN_AR'),
                                    getattr(config, 'SMS_OPERATION_NO_AUTO_ASSIGN_EN'))
        else:
            serializer.save()


class ActionOrderByOperation(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetOrdersSerializer
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        current_order = Order.objects.get(id=self.kwargs['pk'])
        print('payment_authorized of current_order',
              current_order.payment_authorized)
        if self.request.data['status'] == 'canceled':
            print('I am suppose to send sms to provider',
                  current_order.provider.user.phone_number)
            sendSMS(current_order.custom_id, current_order.provider.user.phone_number, getattr(config, 'SMS_PROVIDER_ORDER_CANCELLED_AR'),
                    getattr(config, 'SMS_PROVIDER_ORDER_CANCELLED_EN'))
            serializer.save(
                provider=None, order_block_start=None, order_block_end=None)
            delete_all_related_order_providers(current_order)
        else:
            serializer.save()


def delete_all_related_order_providers(order):
    order_sorted_providers = order.order_possible_providers.all().order_by('-importance')
    if order_sorted_providers:
        OrderPossibleProvider.objects.filter(order=order).delete()


def sendSMS(order_number, phone_number, arabic_text, english_text):
    try:
        body = "Order with number " + \
            str(order_number) + " " + english_text + "\n" + \
            "طلب رقم " + str(order_number) + " " + arabic_text
        result = rest_controller.create_send_message(app_sid, sender_id, body,
                                                     '966' + phone_number,
                                                     response_type, correlation_id, base_encode,
                                                     status_callback),
        print('RESSSSULT OF SMS', result)
    except APIException as e:
        print('ERRROR OF SMS', e)

# class paymentInfo_view(views.APIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request, paymentId):
#         if paymentId:
#             try:
#                 url = "https://api.tap.company/v2/authorize/" + paymentId
#                 payload = "{}"
#                 headers = {'authorization': 'Bearer sk_live_snIkgH9ATpYZMLzl4Sw73rhX'}
#                 response = requests.request("GET", url, data=payload, headers=headers)
#             except Exception as e:
#                 print('errror', e)
#                 return Response(e)
#         return Response(response.text)


@api_view(['POST', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_discount(request):
    if ('code' in request.data and 'id' in request.data):
        order = Order.objects.get(id=request.data['id'])
        try:
            discount = Discount.objects.get(code=request.data['code'])
            order.order_related_invoice.cost = order.order_related_invoice.initial_cost - \
                (order.order_related_invoice.initial_cost * (discount.percentage/100))
            order.order_related_invoice.save()
            response_serializer = GetOrdersSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except Discount.DoesNotExist:
            if ('id' in request.data):
                order = Order.objects.get(id=request.data['id'])
                order.order_related_invoice.cost = order.order_related_invoice.initial_cost
                order.order_related_invoice.save()
                response_serializer = GetOrdersSerializer(order)
                return Response(response_serializer.data, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        if ('id' in request.data):
            order = Order.objects.get(id=request.data['id'])
            order.order_related_invoice.cost = order.order_related_invoice.initial_cost
            order.order_related_invoice.save()
            response_serializer = GetOrdersSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def download_orders_data(request):
    if request.method == "POST":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="wtd_orders.csv"'

        writer = csv.writer(response)
        writer.writerow(
            ['id', 'owner', 'patient', 'from_location', 'to_location', 'order_date', 'arrival_time', 'status', 'created_at',
             'approved_by_client', 'payment_authorized', 'order_type', 'waiting_time', 'provider', 'operator',
             'approved_by_provider', 'notes', 'health_institution', 'appointment_approval', 'discharge_approval',
             'from_region', 'to_region', 'from_city', 'to_city', 'from_special_location', 'to_special_location',
             'is_overweight', 'is_emergency', 'is_contagious', 'needs_oxygen', 'is_approved_by_operation',
             'is_discharged', 'order_block_start', 'order_block_end', 'send_sms'])

        AllOrders = Order.objects.all().values_list('id', 'owner', 'patient', 'from_location', 'to_location', 'order_date',
                                                    'arrival_time', 'status', 'created_at', 'approved_by_client',
                                                    'payment_authorized', 'order_type', 'waiting_time', 'provider',
                                                    'operator', 'approved_by_provider', 'notes', 'health_institution',
                                                    'appointment_approval', 'discharge_approval', 'from_region',
                                                    'to_region', 'from_city', 'to_city', 'from_special_location',
                                                    'to_special_location', 'is_overweight', 'is_emergency',
                                                    'is_contagious', 'needs_oxygen', 'is_approved_by_operation',
                                                    'is_discharged', 'order_block_start', 'order_block_end',
                                                    'send_sms',)
        for order in AllOrders:
            writer.writerow(order)

        return response


@api_view(['POST'])
def download_invoices(request):
    if request.method == "POST":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="wtd_orders.csv"'

        writer = csv.writer(response)
        writer.writerow(
            ['id', 'order', 'distance_value', 'distance_text', 'duration_value', 'duration_text', 'cost', 'initial_cost'])

        AllInvoices = Invoice.objects.all().values_list('id', 'order', 'distance_value', 'distance_text', 'duration_value',
                                                        'duration_text', 'cost', 'initial_cost')
        for invoice in AllInvoices:
            writer.writerow(invoice)

        return response
