from django.shortcuts import render

# Create your views here.
from otp.models import OTP
from django.shortcuts import render
from datetime import datetime, timedelta
import time
from django_otp.oath import TOTP
from wtd import settings
from accounts.models import User
from rest_framework import views, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.core.mail import send_mail
import json
# Create your views here.
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
# recipient = 966562156104
response_type = 'JSON'
correlation_id = '""'
base_encode = True
status_callback = 'sent'

class OTPAuthentication(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, otpToken=None):
        now = datetime.now()
        OTP.objects.filter(expire__lt=now).delete()
        item = bytes(str(request.auth), 'utf-8')
        user = User.objects.get(id=request.user.id)

        if otpToken:
            otpInfo = OTP.objects.get(user_id=user.id)
            now = str(datetime.now())
            if(str(otpInfo.otp) == str(otpToken) and now < otpInfo.expire):
                responseToken = Token.objects.get(key=request.auth)
                OTP.delete(otpInfo)
                user.isVerified = True
                user.save()
                return Response({'token': responseToken.key, 'id': user.id},
                                status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            OTP.objects.filter(user=user).delete()

        token = TOTP(item)
        otp = token.token()
        # otp = 999999
        # send_mail(
        #     subject="Your OTP Password",
        #     message="Your OTP password is %s" % otp,
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[user]
        # )
        try:
            body = "your OTP number: " + str(otp)
            result = rest_controller.create_send_message(app_sid, sender_id, body,
                                                         '966' + user.phone_number,
                                                         response_type, correlation_id, base_encode,
                                                         status_callback),
            print('RESSSSULT OF SMS', result)
        except APIException as e:
            print('ERRROR OF SMS', e)
        newOTPRow = OTP(otp=otp,
                        expire=str(datetime.now() +
                                   timedelta(minutes=5)),
                        user=user)
        newOTPRow.save()

        # Now we trick form to be invalid
        return Response("Enter OTP you received via e-mail", status=status.HTTP_201_CREATED)


class resetPasswordToken(views.APIView):

    def post(self, request,  *args, **kwargs):
        print('request in resetPasswordToken', request.data)
        user = User.objects.get(phone_number=request.data['phone_number'])
        if ((request.data['platform'] == 'client' and not user.isClient) or (
                request.data['platform'] == 'operation' and not user.isOperation) or (
                request.data['platform'] == 'provider' and not user.isProvider)):
            print('I entered the condition')
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        responseToken = Token.objects.get(user=user)
        return Response({'token': responseToken.key, 'id': user.id},
                        status=status.HTTP_200_OK)
