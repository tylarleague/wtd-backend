
from otp.models import OTP
from datetime import datetime, timedelta

from accounts.models import User

from celery import shared_task


@shared_task
def otp_handle():
    now = datetime.now()
    OTP.objects.filter(expire__lt=now).delete()
    print(now)
    return True

@shared_task
def inActive_users_handle():
    print('deleting INACTIVE users')
    now = datetime.now()
    User.objects.filter(isVerified=False, delete_at__lt=now).delete()
    return True

# @periodic_task(
#     run_every=(crontab(minute='*/15')),
#     name="task_save_latest_flickr_image",
#     ignore_result=True
# )
# def task_save_latest_flickr_image():
#     """
#     Saves latest image from Flickr
#     """
#     print('helllloooooo')