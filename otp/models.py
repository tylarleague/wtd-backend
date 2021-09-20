import datetime
import json
from accounts.models import User, SpecialAccounts
from django.db import models
import uuid

# Create your models here.


class OTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    otp = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expire = models.CharField(max_length=100)

    @property
    def delete_after_five_minutes(self):
        if self.expire < datetime.datetime.now():
            e = OTP.objects.get(pk=self.pk)
            e.delete()
            return True
        else:
            return False
