from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
# from fcm_django.models import FCMDevice
#
# from accounts.models import User
# from notifications.models import Notification
# from notifications.serializers import NotificationListSerializer
from accounts.models import OperationProfile
from orders.models import Order, AmbReport
# from django.core import serializers
# from django.forms.models import model_to_dict
# from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# from social.serializers import ThoughtPolymorphicSerializer, GetTextThoughtSerializer
# from social.serializers import GetCommentSerializer, GetThoughtSerializer
from unifonicnextgen.unifonicnextgen_client import UnifonicnextgenClient
from unifonicnextgen.configuration import Configuration
from unifonicnextgen.exceptions.api_exception import APIException

basic_auth_user_name = 'e637a3df-8da4-4cd2-b524-5a5409e811f9'
basic_auth_password = '0UpBuW8KAxwOWkJn8Y7lKBbrFEz4aTFn87z3kFwwpWhFB3XJAec2Dn4BTeCakSlkdhGAfCbxkWK'

client = UnifonicnextgenClient(basic_auth_user_name, basic_auth_password)
rest_controller = client.rest
app_sid = 'Q0hq8Uu4tcJf1UcsgAP7DSCsP8VHil'
sender_id = 'Wtd.Care'
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
                print('I am suppose to send sms to client', instance.owner.user.phone_number)
                sendSMS(instance.custom_id, instance.owner.user.phone_number, "تم استلامه و في انتظار الموافقة",
                        "has been created, waiting for approval")
    else:
        print('SIGNALS: updated order', instance.status)
        if instance.status == 'open' and instance.payment_authorized:
            print('I am suppose to update operation')
            # channel_layer = get_channel_layer()
            # async_to_sync(channel_layer.group_send)(
            #     "update_order", {"type": "change.update_order",
            #                      "event": "Open",
            #                      "object": instance.id})
            for operation_profile in operation_profiles:
                if operation_profile.is_available is True:
                    print('operation_profile', operation_profile.user.phone_number)
                    sendSMS(instance.custom_id, operation_profile.user.phone_number, "تم انشاؤه",
                            "has been created")
            print('I am suppose to send sms to client', instance.owner.user.phone_number)
            sendSMS(instance.custom_id, instance.owner.user.phone_number, "تم استلامه و في انتظار الموافقة", "has been created, waiting for approval")
        elif instance.status == 'sent_to_provider':
            print('I am suppose to send sms to provider', instance.provider.user.phone_number)
            sendSMS(instance.custom_id, instance.provider.user.phone_number, " تم ارساله إليك من قبل وتد، رجاء تحديث الصفحة و من ثم القبول أو الرفض", "has been sent to you by Wtd, please refresh your page, then approve or decline")
        elif instance.status == 'rejected_by_provider':
            print('I am suppose to update operation')
            # channel_layer = get_channel_layer()
            # async_to_sync(channel_layer.group_send)(
            #     "update_order", {"type": "change.update_order",
            #                      "event": "Rejected By Provider",
            #                      "object": instance.id})
            for operation_profile in operation_profiles:
                if operation_profile.is_available is True:
                    print('operation_profile', operation_profile.user.phone_number)
                    sendSMS(instance.custom_id, operation_profile.user.phone_number, "تم رفضه من مقدم الخدمة",
                            "has been rejected by provider")
        # elif instance.status == 'approved_by_provider':
        #     print('I am suppose to update operation')
        #     # channel_layer = get_channel_layer()
        #     # async_to_sync(channel_layer.group_send)(
        #     #     "update_order", {"type": "change.update_order",
        #     #                      "event": "Approved By Provider",
        #     #                      "object": instance.id})
        #     for operation_profile in operation_profiles:
        #         if operation_profile.is_available is True:
        #             print('operation_profile', operation_profile.user.phone_number)
        #             sendSMS(instance.custom_id, operation_profile.user.phone_number, "تمت الموافقة عليه من مقدم الخدمة",
        #                     "has been accepted by provider")
        elif instance.status == 'scheduled':
            print('I am suppose to send sms to client', instance.owner.user.phone_number)
            sendSMS(instance.custom_id, instance.owner.user.phone_number, "تمت الموافقة عليه و جدولته", "has been approved and scheduled")
            print('I am suppose to send sms to provider', instance.provider.user.phone_number)
            sendSMS(instance.custom_id, instance.provider.user.phone_number, "تمت الموافقة عليه و جدولته",
                    "has been approved and scheduled")
        elif instance.status == 'started_by_provider':
            print('I am suppose to update operation')
            # channel_layer = get_channel_layer()
            # async_to_sync(channel_layer.group_send)(
            #     "update_order", {"type": "change.update_order",
            #                      "event": "Started By Provider",
            #                      "object": instance.id})
            for operation_profile in operation_profiles:
                if operation_profile.is_available is True:
                    print('operation_profile', operation_profile.user.phone_number)
                    sendSMS(instance.custom_id, operation_profile.user.phone_number, "بدأ من قبل مقدم الخدمة",
                            "has been started by provider")
            print('I am suppose to send sms to client', instance.owner.user.phone_number)
            sendSMS(instance.custom_id, instance.owner.user.phone_number, "، سيارة الاسعاف في طريقها إليك",
                    "has been started, an ambulance is on its way to you")
        elif instance.status == 'canceled':
            if instance.owner:
                print('I am suppose to send sms to client', instance.owner.user.phone_number)
                sendSMS(instance.custom_id, instance.owner.user.phone_number, "تم إلغاؤه",
                        "has been canceled")
            if instance.provider:
                print('I am suppose to send sms to provider', instance.provider.user.phone_number)
                sendSMS(instance.custom_id, instance.provider.user.phone_number, "تم إلغاؤه",
                        "has been canceled")
        elif instance.status == 'done':
            print('I am suppose to update operation')
            # channel_layer = get_channel_layer()
            # async_to_sync(channel_layer.group_send)(
            #     "update_order", {"type": "change.update_order",
            #                      "event": "Delivered",
            #                      "object": instance.id})
            for operation_profile in operation_profiles:
                if operation_profile.is_available is True:
                    print('operation_profile', operation_profile.user.phone_number)
                    sendSMS(instance.custom_id, operation_profile.user.phone_number, "تم الانتهاء منه",
                            "has been finished")
            print('I am suppose to send sms to client', instance.owner.user.phone_number)
            sendSMS(instance.custom_id, instance.owner.user.phone_number, "تم الانتهاء منه",
                    "has been finished")
        else:
            print('Unknown status at Signals')


def sendSMS(order_number, phone_number, arabic_text, english_text):
    try:
        body = "Order with number " + str(order_number) + " " + english_text + "\n" + "طلب رقم " + str(order_number) + " " + arabic_text
        result = rest_controller.create_send_message(app_sid, sender_id, body,
                                                     '966' + phone_number,
                                                     response_type, correlation_id, base_encode,
                                                     status_callback),
        print('RESSSSULT OF SMS', result)
    except APIException as e:
        print('ERRROR OF SMS', e)
