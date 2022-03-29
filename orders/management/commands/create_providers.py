import random
# from random import randrange
import json
import faker.providers
from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, ClientProfile, ProviderProfile, OperationProfile, Organization, SpecialAccounts
from orders.models import Region, RegionPoint, City, CityPoint, SpecialLocation, SpecialLocationPoint
import random
PHONE_NUMBERS = [
    "562156104",
    "596262736",
    "LocationThought",
    "ImageThought",
    "VideoThought",
    "StatusThought",
]

THOUGHT_STATUS = [
    "sleeping",
    "awake",
    "studying",
    "work",
    "workout",
    "chilling",
]

THOUGHT_EMOTIONS = [
    "sad",
    "laugh",
    "heart",
    "shock",
    "smile",
]


# class Provider(faker.providers.BaseProvider):
    # def thought_type(self):
    #     # return self.random_element(THOUGHT_TYPES)
    #
    # def thought_status(self):
    #     return self.random_element(THOUGHT_STATUS)
    #
    # def thought_emotions(self):
    #     return self.random_element(THOUGHT_EMOTIONS)


class Command(BaseCommand):
    help = "Command information"


    def handle(self, *args, **kwargs):
        fake = Faker()
        allOrganizations = Organization.objects.all()
        for _ in range(10):
            ph_no = []
            generated_phone = ''
            # the first number should be in the range of 6 to 9
            ph_no.append(5)

            # the for loop is used to append the other 9 numbers.
            # the other 9 numbers can be in the range of 0 to 9.
            for i in range(1, 9):
                ph_no.append(random.randint(0, 9))
            for i in ph_no:
                print(i, end="")
                generated_phone += str(i)
            phone_number = generated_phone
            # name = fake.name()
            newUser = User.objects.create(phone_number=phone_number, name=fake.name())
            ProviderProfile.objects.create(user=newUser, organization=random.choice(allOrganizations))

        all_users = User.objects.all()
        for u in all_users:
            SpecialAccounts.objects.create(phone_number=u.phone_number)
        self.stdout.write('Done creating providers')