"""Declare models for YOUR_APP app."""
# from orders.models import City, Region
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.postgres.fields import JSONField
import uuid

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone_number:
            raise ValueError('The given phone_number must be set')
        # email = email.lower()
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=30)
    # email = models.EmailField(_('email address'), unique=True)
    # / ^ (5)(5 | 0 | 3 | 6 | 4 | 9 | 1 | 8 | 7)([0 - 9]{7})$ /
    phone_regex = RegexValidator(regex="^(5)(5|0|3|6|4|9|1|8|7)([0-9]{7})$",
                                 message="Phone number must be entered in the format: '555555555'. Up to 9 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=9, unique=True)  # validators should be a list
    isVerified = models.BooleanField(default=False)
    isClient = models.BooleanField(default=True)
    isOperation = models.BooleanField(default=False)
    isProvider = models.BooleanField(default=False)

    # friends_limit = models.IntegerField(default=75)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Organization(models.Model):
    # user = models.OneToOneField(User, related_name="user_provider_profile", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    percentage = models.IntegerField(default=70)

    def __str__(self):
        return str(self.name)

class ClientProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_client_profile", on_delete=models.CASCADE)
    gender = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return str(self.user.phone_number) + " - " + str(self.user.name)

class OperationProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_operation_profile", on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return str(self.user.phone_number) + " - " + str(self.user.name)

class ProviderProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_provider_profile", on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    organization = models.ForeignKey(
        Organization, related_name="organization_providers", on_delete=models.CASCADE, blank=True, null=True)
    # region = models.ForeignKey(
    #     Region, related_name="region_providers", on_delete=models.CASCADE, blank=True, null=True)
    # city = models.ForeignKey(
    #     City, related_name="city_providers", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.user.phone_number) + " - " + str(self.user.name) + " - " + str(self.organization)

class Person(models.Model):
    profile = models.ForeignKey(
        ClientProfile, related_name="related_persons", on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=30, blank=True, null=True)
    birth_day = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=30, blank=True, null=True)
    relation = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return str(self.name) + " related to user: " + str(self.profile.user.phone_number) + " - " + str(self.profile.user.name)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.isClient:
            ClientProfile.objects.create(user=instance)
        if instance.isOperation:
            OperationProfile.objects.create(user=instance)
        if instance.isProvider:
            ProviderProfile.objects.create(user=instance)
    else:
        if instance.isClient and not hasattr(instance, 'user_client_profile'):
            ClientProfile.objects.create(user=instance)
        if instance.isOperation and not hasattr(instance, 'user_operation_profile'):
            OperationProfile.objects.create(user=instance)
        if instance.isProvider and not hasattr(instance, 'user_provider_profile'):
            ProviderProfile.objects.create(user=instance)

# MAYBE i need to update this similar to top hasattr
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
#     if instance.isClient:
#         instance.user_client_profile.save()
#     if instance.isOperation:
#         instance.user_operation_profile.save()
#     if instance.isProvider:
#         instance.user_provider_profile.save()

@receiver(post_save, sender=ProviderProfile)
def create_provider_profile(sender, instance, **kwargs):
        # if not instance.user_provider_profile:
        instance.user.isProvider = True
        instance.user.save()


class SpecialAccounts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    phone_regex = RegexValidator(regex="^(5)(5|0|3|6|4|9|1|8|7)([0-9]{7})$",
                                 message="Phone number must be entered in the format: '555555555'. Up to 9 digits allowed.")
    phone_number = models.CharField(_('special phone number'), validators=[phone_regex], max_length=9, unique=True)  # validators should be a list

    def __str__(self):
        return str(self.phone_number)
