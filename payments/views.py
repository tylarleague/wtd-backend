from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .models import Payment, Order, User
from rest_framework.response import Response
import http.client
import json
import requests
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework import views, permissions, status
from django.core import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from payments.serializers import PaymentSerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token
from decimal import Decimal

# Create your views here.


class paymentInfo_view(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, paymentId):
        if paymentId:
            try:
                url = "https://api.tap.company/v2/charges/" + paymentId
                payload = "{}"
                headers = {
                    'authorization': 'Bearer sk_live_snIkgH9ATpYZMLzl4Sw73rhX'}
                response = requests.request(
                    "GET", url, data=payload, headers=headers)
            except Exception as e:
                print('errror', e)
                return Response(e)

            print('response', json.loads(response.text))
            tapData = json.loads(response.text)
            order_id = tapData['metadata']['order_id']
            order = Order.objects.get(id=tapData['metadata']['order_id'])
            print('ORRRDER', order)
            print('Ussser', request.user)
            payment = Payment.objects.create(
                order=order,
                user=request.user,
                tap_id=tapData['id'],
                status=tapData['status']
            )
            print('payment', payment)
        return Response(response.text)


@api_view(['POST', ])
def pay_view(request):

    if request.method == 'POST':
        # from_location = eval(request.data['from_location'])  How to get data from request
        # order_id = request.data['order']
        order = Order.objects.get(id=request.data['order'])
        user = User.objects.get(id=request.data['user'])
        tap_token_id = request.data['tap_token_id']
        print('order_related_invoice', order.order_related_invoice.cost)

        conn = http.client.HTTPSConnection("api.tap.company")
        requestBody = {
            "amount": order.order_related_invoice.cost,
            "currency": "SAR",
            "threeDSecure": True,
            "save_card": False,
            "description": "payment for order" + str(order.id),
            "statement_descriptor": "Sample",
            "metadata": {
                "udf1": "test 1",
                "udf2": "test 2"
            },
            "reference": {
                "transaction": "txn_0001",
                "order": order.id
            },
            "receipt": {
                "email": False,
                "sms": True
            },
            "customer": {
                "first_name": user.name,
                "middle_name": "test",
                "last_name": "test",
                "email": "test@test.com",
                "phone": {
                    "country_code": "966",
                    "number": user.phone_number
                }
            },
            "merchant": {
                "id": ""
            },
            "source": {
                "id": tap_token_id
            },
            "post": {
                "url": "http://your_website.com/post_url"
            },
            "redirect": {
                "url": "http://your_website.com/redirect_url"
            }
        }

        payload = json.dumps(requestBody)

        headers = {
            'authorization': "Bearer sk_live_snIkgH9ATpYZMLzl4Sw73rhX",
            'content-type': "application/json"
        }
        url = "https://api.tap.company/v2/charges"
        response = requests.request("POST", url, data=payload, headers=headers)
        data = json.loads(response.text)
        payment = Payment.objects.create(
            order=order,
            user=user,
            tap_token_id=tap_token_id,
            tap_charge_id=data['id'],
            status=data['status']
        )
        # serialized_obj = serializers.serialize('json', [payment, ])
        dict_obj = model_to_dict(payment)
        serialized = json.dumps(dict_obj)
        json_payment = json.loads(serialized)

        # HOW TO CREATE RESPONSE DATA
        ResponseData = {
            "payment": json_payment,
            "tap_response": data

        }
        return Response(ResponseData)


class CreatePaymentView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    queryset = Order.objects.all()


@api_view(['POST', 'GET'])
def add_pay_view(request):
    if request.method == 'GET':
        order = Order.objects.get(id=request.GET.get('order_id'))
        headers = {
            'authorization': "Bearer sk_live_snIkgH9ATpYZMLzl4Sw73rhX",
            'content-type': "application/json",
            'lang_code': 'ar'
        }
        innerHeader = {
            'Authorization': "Token " + Token.objects.get(user_id=order.owner.user).key,
            'content-type': "application/json",
        }
        url = "https://api.tap.company/v2/invoices/"+request.GET.get('tap_id')
        response = requests.request("GET", url, data={}, headers=headers)
        data = json.loads(response.text)
        payment = {
            "order": request.GET.get('order_id'),
            "user": order.owner.user.id,
            "tap_id": data['transactions'][0]['id'],
            "tap_refund_id": data['transactions'][0]['id'],
            "status": data['transactions'][0]['status'],
            "amount": int(data['transactions'][0]['amount'])
        }
        response2 = requests.request("POST", 'http://161.35.67.15:1234/payment/',
                                     data=json.dumps(payment),
                                     headers=innerHeader)
        response3 = requests.request("PATCH", 'http://161.35.67.15:1234/order/client_action/'+request.GET.get('order_id'),
                                     data=json.dumps(
                                         {"payment_authorized": True}),
                                     headers=innerHeader)
    return redirect('https://www.wtdcare.com/')


@api_view(['POST'])
def amwal_pay(request, **kwargs):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    order = Order.objects.get(
        id=kwargs['id'], owner=request.user.user_client_profile)
    url = "https://backend.sa.amwal.tech/transactions/" + \
        body['amwal_ref']
    response = requests.request("GET", url, data={})
    data = json.loads(response.text)
    if float(data['amount']) == float("{:2f}".format(order.order_related_invoice.cost)):
        innerHeader = {
            'Authorization': "Token " + Token.objects.get(user_id=order.owner.user).key,
            'content-type': "application/json",
        }
        payment = {
            "order": kwargs['id'],
            "user": order.owner.user.id,
            "tap_id": data['id'],
            "tap_refund_id": data['id'],
            "status": data['status'],
            "amount": float(data['amount'])
        }
        response2 = requests.request("POST", 'http://161.35.67.15:1234/payment/',
                                     data=json.dumps(payment),
                                     headers=innerHeader)
        response3 = requests.request("PATCH", 'http://161.35.67.15:1234/order/client_action/'+ kwargs['id'],
                                     data=json.dumps(
                                         {"payment_authorized": True}),
                                     headers=innerHeader)
        return Response({"status": True})

    return Response({"status": False})
