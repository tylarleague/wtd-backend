from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Payment, Order, User
from rest_framework.response import Response
import http.client
import json
import requests
from django.forms.models import model_to_dict
from django.core import serializers
# Create your views here.


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
            'authorization': "Bearer sk_test_g5nBLfJUcuVE9mkTKezvlxMF",
            'content-type': "application/json"
        }
        url = "https://api.tap.company/v2/charges"
        response = requests.request("POST", url, data=payload, headers=headers)
        data = json.loads(response.text)
        print('daaataaa', data)
        # conn.request("POST", "/v2/charges", payload, headers)
        #
        # res = conn.getresponse()
        # data = res.read()
        #
        # print("priiinting respoooonse", data.decode("utf-8"))

        # print("data['id']", data['id'])
        payment = Payment.objects.create(
            order=order,
            user=user,
            tap_token_id= tap_token_id,
            tap_charge_id = data['id'],
            status = data['status']
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