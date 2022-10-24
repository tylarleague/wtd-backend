from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
import requests
# from fcm_django.models import FCMDevice
#
import json
# from accounts.models import User
# from notifications.models import Notification
# from notifications.serializers import NotificationListSerializer
from accounts.models import OperationProfile
from orders.models import Order, AmbReport, OrderPossibleProvider
# from django.core import serializers
# from django.forms.models import model_to_dict
# from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# from social.serializers import ThoughtPolymorphicSerializer, GetTextThoughtSerializer
# from social.serializers import GetCommentSerializer, GetThoughtSerializer
from unifonicnextgen.unifonicnextgen_client import UnifonicnextgenClient
from unifonicnextgen.configuration import Configuration
from unifonicnextgen.exceptions.api_exception import APIException
from payments.models import Payment
from constance import config
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
operation_profiles = OperationProfile.objects.all()
# async = False


@receiver(post_save, sender=Order)
def announce_status_change(sender, instance, created, **kwargs):
    print('INSTANCE: ', "966" + instance.owner.user.phone_number)
    if created:
        print('SIGNALS: created new order', instance.status)
        if instance.payment_authorized:
            if getattr(config, 'ALLOW_SMS_SYSTEM') == True and instance.send_sms:
                print('I am suppose to send sms to client',
                      instance.owner.user.phone_number)
                sendSMS(instance.custom_id, instance.owner.user.phone_number, getattr(config, 'SMS_CLIENT_NEW_ORDER_AR'),
                        getattr(config, 'SMS_CLIENT_NEW_ORDER_EN'))
    else:
        print('SIGNALS: updated order', instance.status)
        if instance.status == 'open' and instance.payment_authorized:
            if getattr(config, 'ALLOW_SMS_SYSTEM') == True:
                print('I am suppose to update operation')
                if instance.operator:
                    sendSMS(instance.custom_id, instance.operator.user.phone_number, getattr(config, 'SMS_OPERATION_NEW_ORDER_AR'),
                            getattr(config, 'SMS_OPERATION_NEW_ORDER_EN'))
                else:
                    for operation_profile in OperationProfile.objects.all():
                        if operation_profile.is_available is True:
                            print('operation_profile',
                                  operation_profile.user.phone_number)
                            sendSMS(instance.custom_id, operation_profile.user.phone_number, getattr(config, 'SMS_OPERATION_NEW_ORDER_AR'),
                                    getattr(config, 'SMS_OPERATION_NEW_ORDER_EN'))
                if instance.send_sms:
                    print('I am suppose to send sms to client',
                          instance.owner.user.phone_number)
                    sendSMS(instance.custom_id, instance.owner.user.phone_number, getattr(
                        config, 'SMS_CLIENT_NEW_ORDER_AR'), getattr(config, 'SMS_CLIENT_NEW_ORDER_EN'))
        elif instance.status == 'sent_to_provider' and instance.payment_authorized:
            if getattr(config, 'ALLOW_SMS_SYSTEM') == True:
                print('I am suppose to send sms to provider',
                      instance.provider.user.phone_number)
                sendSMS(instance.custom_id, instance.provider.user.phone_number, getattr(
                    config, 'SMS_PROVIDER_RECEIVE_ORDER_AR'), getattr(config, 'SMS_PROVIDER_RECEIVE_ORDER_EN'))
        elif instance.status == 'rejected_by_provider':
            if getattr(config, 'ALLOW_SMS_SYSTEM') == True:
                print('I am suppose to update operation')
                if instance.operator:
                    sendSMS(instance.custom_id, instance.operator.user.phone_number, getattr(config, 'SMS_OPERATION_PROVIDER_REJECTED_AR'),
                            getattr(config, 'SMS_OPERATION_PROVIDER_REJECTED_EN'))
                else:
                    for operation_profile in OperationProfile.objects.all():
                        if operation_profile.is_available is True:
                            print('operation_profile',
                                  operation_profile.user.phone_number)
                            sendSMS(instance.custom_id, operation_profile.user.phone_number, getattr(config, 'SMS_OPERATION_PROVIDER_REJECTED_AR'),
                                    getattr(config, 'SMS_OPERATION_PROVIDER_REJECTED_EN'))
        elif instance.status == 'scheduled':
            if getattr(config, 'ALLOW_SMS_SYSTEM') == True:
                # SMS_OPERATION_PROVIDER_ACCEPTED_AR
                if instance.send_sms:
                    print('I am suppose to send sms to client',
                          instance.owner.user.phone_number)
                    sendSMS(instance.custom_id, instance.owner.user.phone_number, getattr(
                        config, 'SMS_CLIENT_ORDER_APPROVED_AR'), getattr(config, 'SMS_CLIENT_ORDER_APPROVED_EN'))

                if instance.operator:
                    sendSMS(instance.custom_id, instance.operator.user.phone_number, getattr(config, 'SMS_OPERATION_PROVIDER_ACCEPTED_AR'),
                            getattr(config, 'SMS_OPERATION_PROVIDER_ACCEPTED_EN'))
                else:
                    for operation_profile in OperationProfile.objects.all():
                        if operation_profile.is_available is True:
                            print('operation_profile',
                                  operation_profile.user.phone_number)
                            sendSMS(instance.custom_id, operation_profile.user.phone_number, getattr(config, 'SMS_OPERATION_PROVIDER_ACCEPTED_AR'),
                                    getattr(config, 'SMS_OPERATION_PROVIDER_ACCEPTED_EN'))
        elif instance.status == 'started_by_provider':
            if getattr(config, 'ALLOW_SMS_SYSTEM') == True:
                print('I am suppose to update operation')
                if instance.operator:
                    sendSMS(instance.custom_id, instance.operator.user.phone_number, getattr(config, 'SMS_OPERATION_PROVIDER_STARTED_AR'),
                            getattr(config, 'SMS_OPERATION_PROVIDER_STARTED_EN'))
                else:
                    for operation_profile in operation_profiles:
                        if operation_profile.is_available is True:
                            print('operation_profile',
                                  operation_profile.user.phone_number)
                            sendSMS(instance.custom_id, operation_profile.user.phone_number, getattr(config, 'SMS_OPERATION_PROVIDER_STARTED_AR'),
                                    getattr(config, 'SMS_OPERATION_PROVIDER_STARTED_EN'))
                if instance.send_sms:
                    print('I am suppose to send sms to client',
                          instance.owner.user.phone_number)

                    sendSMS(instance.custom_id, instance.owner.user.phone_number, getattr(config, 'SMS_CLIENT_PROVIDER_STARTED_AR'),
                            getattr(config, 'SMS_CLIENT_PROVIDER_STARTED_EN'))
        elif instance.status == 'canceled':

            if getattr(config, 'ALLOW_SMS_SYSTEM') == True:
                if instance.owner and instance.send_sms:
                    print('I am suppose to send sms to client',
                          instance.owner.user.phone_number)
                    sendSMS(instance.custom_id, instance.owner.user.phone_number, getattr(config, 'SMS_CLIENT_ORDER_CANCELLED_AR'),
                            getattr(config, 'SMS_CLIENT_ORDER_CANCELLED_EN'))
                if instance.provider:
                    print('I am suppose to send sms to provider',
                          instance.provider.user.phone_number)
                    sendSMS(instance.custom_id, instance.provider.user.phone_number, getattr(config, 'SMS_PROVIDER_ORDER_CANCELLED_AR'),
                            getattr(config, 'SMS_PROVIDER_ORDER_CANCELLED_EN'))
            refundAmount(instance)
        elif instance.status == 'done':
            if getattr(config, 'ALLOW_SMS_SYSTEM') == True:
                print('I am suppose to update operation')
                if instance.operator:
                    sendSMS(instance.custom_id, instance.operator.user.phone_number, getattr(config, 'SMS_OPERATION_ORDER_DONE_AR'),
                            getattr(config, 'SMS_OPERATION_ORDER_DONE_EN'))
                else:
                    for operation_profile in operation_profiles:
                        if operation_profile.is_available is True:
                            print('operation_profile',
                                  operation_profile.user.phone_number)
                            sendSMS(instance.custom_id, operation_profile.user.phone_number, getattr(config, 'SMS_OPERATION_ORDER_DONE_AR'),
                                    getattr(config, 'SMS_OPERATION_ORDER_DONE_EN'))
                if instance.send_sms:
                    print('I am suppose to send sms to client',
                          instance.owner.user.phone_number)
                    sendSMS(instance.custom_id, instance.owner.user.phone_number, getattr(config, 'SMS_CLIENT_ORDER_DONE_AR'),
                            getattr(config, 'SMS_CLIENT_ORDER_DONE_EN'))
        else:
            print('Unknown status at Signals')


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


def refundAmount(order):
    print('inside refund amount', order)
    print('instance.order_related_payments',
          order.order_related_payments.all())
    payment_to_refund = None
    payments = Payment.objects.get(order=order, status='CAPTURED')
    if payments:
        try:
            url = "https://api.tap.company/v2/refunds"

            requestData = {
                "charge_id": payments.tap_id,
                "amount": payments.amount,
                "currency": "SAR",
                "description": "Order Canceled",
                "reason": "requested_by_customer",
                "metadata": {
                    "order_id": order.id,
                },
                "post": {
                    "url": ""
                }
            }

            payload = json.dumps(requestData)

            # payload = "{\"charge_id\":\"chg_86dfjghadfuda7ft\",\"amount\":2,\"currency\":\"KWD\",\"description\":\"Test Description\",\"reason\":\"requested_by_customer\",\"reference\":{\"merchant\":\"txn_0001\"},\"metadata\":{\"udf1\":\"test1\",\"udf2\":\"test2\"},\"post\":{\"url\":\"http://your_url.com/post\"}}"
            headers = {
                'authorization': 'Bearer sk_live_snIkgH9ATpYZMLzl4Sw73rhX',
                'content-type': "application/json"
            }

            response = requests.request(
                "POST", url, data=payload, headers=headers)
            data = json.loads(response.text)
            print('refuuuund response daaataaa', data)
            print('payments before update', payments.tap_refund_id)
            if 'id' in data.keys() and data['id']:
                payments.tap_refund_id = data['id']
                payments.status = "REFUND REQUEST"
                payments.save()
            print('payments after update', payments.tap_refund_id)
            # print('refuuuund response', response.text)
        except APIException as e:
            print('refund error', e)
    else:
        print('No Payment to refund')


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

# def delete_all_related_order_providers(order):
#     order_sorted_providers = order.order_possible_providers.all().order_by('-importance')
#     if order_sorted_providers:
#         OrderPossibleProvider.objects.filter(order=order).delete()
