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
        # fake.add_provider(Provider)
        #
        allOrganizations = []
        dallah_namar = Organization.objects.create(name='Dallah Hospital - Namar - RUH', lat=24.560707198645762,
                                                   lng=46.67695999145508, percentage=70)
        allOrganizations.append(dallah_namar)
        bakhsh_hospital = Organization.objects.create(name='Dr.Bakhsh Hospital - JED', lat=21.519763440311554,
                                                      lng=39.191147054813676, percentage=80)
        allOrganizations.append(bakhsh_hospital)

        for _ in range(5):
            allOrganizations.append(Organization.objects.create(name=fake.company(), lat=random.uniform(24, 25),
                                                          lng=random.uniform(45, 47), percentage=random.randint(50, 90)))


        # for _ in range(12):
        #     ph_no = []
        #     generated_phone = ''
        #     # the first number should be in the range of 6 to 9
        #     ph_no.append(5)
        #
        #     # the for loop is used to append the other 9 numbers.
        #     # the other 9 numbers can be in the range of 0 to 9.
        #     for i in range(1, 9):
        #         ph_no.append(random.randint(0, 9))
        #     for i in ph_no:
        #         print(i, end="")
        #         generated_phone += str(i)
        #     phone_number = generated_phone
        #     name = fake.name()
        #     newUser = User.objects.create(phone_number=phone_number, name=name)
        #     ProviderProfile.objects.create(user=newUser, organization=random.choice(allOrganizations))



        bara_phone = '566122132'
        rakan_phone = '596262736'
        madani_phone = '562156104'

        # madani = User.objects.create(phone_number=madani_phone, name='Madani', isOperation=True, isProvider=True, is_superuser=True)
        rakan = User.objects.create(phone_number=rakan_phone, name='Rakan', isOperation=True)
        albara = User.objects.create(phone_number=bara_phone, name='Albara', isOperation=True)


        riyadh_region = Region.objects.create(name='Riyadh', operator=OperationProfile.objects.get(user=albara))
        hijaz_region = Region.objects.create(name='Hijaz', operator=OperationProfile.objects.get(user=rakan))

        RegionPoint.objects.create(region=riyadh_region, lat=25.073128176505616, lng=45.9939258063895)
        RegionPoint.objects.create(region=riyadh_region, lat=25.247147711080856, lng=47.185942407952)
        RegionPoint.objects.create(region=riyadh_region, lat=24.429613346049088, lng=47.4331347907645)
        RegionPoint.objects.create(region=riyadh_region, lat=24.21437187840885, lng=46.2026660407645)


        RegionPoint.objects.create(region=hijaz_region, lat=28.140980421341627, lng=34.68539202855463)
        RegionPoint.objects.create(region=hijaz_region, lat=29.066927179628706, lng=37.14632952855463)
        RegionPoint.objects.create(region=hijaz_region, lat=19.92295432816771, lng=43.82601702855463)
        RegionPoint.objects.create(region=hijaz_region, lat=19.094514593171215, lng=40.57406390355463)


        # r1 = Region.objects.create(name=fake.company(), operator=random.choice(OperationProfile.objects.all()))
        # RegionPoint.objects.create(region=r1, lat=25.073126536505616, lng=45.9943258063895)
        # RegionPoint.objects.create(region=r1, lat=25.247147456080856, lng=47.185943207952)
        # RegionPoint.objects.create(region=r1, lat=24.429613343249088, lng=47.4331437907645)
        # RegionPoint.objects.create(region=r1, lat=24.21437134540885, lng=46.2026543407645)





        ProviderProfile.objects.create(user=albara, organization=dallah_namar)
        ProviderProfile.objects.create(user=rakan, organization=bakhsh_hospital)





        #
        # allUsers = User.objects.all()
        # for user in allUsers:
        #     all_friends = list(User.objects.exclude(id=user.id))
        #     for to_be_friend in random.sample(all_friends, random.randint(5, 8)):
        #         if not FriendshipManager.are_friends(FriendshipManager, to_be_friend, user):
        #             Friend.objects.create(from_user=user, to_user=to_be_friend)
        #             Friend.objects.create(from_user=to_be_friend, to_user=user)
        #         for _ in range(random.randint(1, 5)):
        #             thoughtType = fake.thought_type()
        #             print('thoughtType', thoughtType)
        #             if bool(random.getrandbits(1)):
        #                 lat = fake.latitude()
        #                 lng = fake.longitude()
        #                 locationName = fake.street_address()
        #                 json_location = {
        #                     'lat': str(lat),
        #                     'lng': str(lng),
        #                     'locationName': locationName,
        #                     'selectedLocationImage': "https://maps.googleapis.com/maps/api/staticmap?center=" + str(lat) + "," + str(lng)
        #                                              + "&zoom=14&size=500x300&maptype=roadmap&markers=color:red%7Clabel:Place%7C24.8354896,46.6003797&key=AIzaSyBRmUPUO4Y0209cXL0GTfkqoAtlBeg4NHg"
        #                 }
        #                 location = json.dumps(json_location)
        #             else:
        #                 location= ""
        #
        #             if thoughtType == "TextThought":
        #                 thought = Thought.objects.create(thoughtType=thoughtType, text=fake.text(max_nb_chars=random.randint(5, 100)), user=user,
        #                                        privacy="friends", location=location, is_repubble=bool(random.getrandbits(1)))
        #             if thoughtType == "MediaThought":
        #                 media = "{\"wrapperType\":\"track\",\"kind\":\"song\",\"artistId\":258535972,\"collectionId\":258615649,\"trackId\":258618600,\"artistName\":\"Little Dragon\",\"collectionName\":\"Little Dragon\",\"trackName\":\"Test\",\"collectionCensoredName\":\"Little Dragon\",\"trackCensoredName\":\"Test\",\"artistViewUrl\":\"https://music.apple.com/us/artist/little-dragon/258535972?uo=4\",\"collectionViewUrl\":\"https://music.apple.com/us/album/test/258615649?i=258618600&uo=4\",\"trackViewUrl\":\"https://music.apple.com/us/album/test/258615649?i=258618600&uo=4\",\"previewUrl\":\"https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview115/v4/af/83/79/af837916-90f9-d503-bf08-13ffb9957f21/mzaf_16662673119862695322.plus.aac.p.m4a\",\"artworkUrl30\":\"https://is4-ssl.mzstatic.com/image/thumb/Music/v4/73/aa/cd/73aacdee-0259-fda7-3e6f-28433c098b38/source/30x30bb.jpg\",\"artworkUrl60\":\"https://is4-ssl.mzstatic.com/image/thumb/Music/v4/73/aa/cd/73aacdee-0259-fda7-3e6f-28433c098b38/source/60x60bb.jpg\",\"artworkUrl100\":\"https://is4-ssl.mzstatic.com/image/thumb/Music/v4/73/aa/cd/73aacdee-0259-fda7-3e6f-28433c098b38/source/100x100bb.jpg\",\"collectionPrice\":9.99,\"trackPrice\":0.99,\"releaseDate\":\"2007-08-28T12:00:00Z\",\"collectionExplicitness\":\"notExplicit\",\"trackExplicitness\":\"notExplicit\",\"discCount\":1,\"discNumber\":1,\"trackCount\":12,\"trackNumber\":10,\"trackTimeMillis\":268040,\"country\":\"USA\",\"currency\":\"USD\",\"primaryGenreName\":\"Electronic\",\"isStreamable\":true}"
        #                 thought = Thought.objects.create(thoughtType=thoughtType, text=fake.text(max_nb_chars=random.randint(5, 100)), user=user,
        #                                        privacy="friends", location=location, media=media, is_repubble=bool(random.getrandbits(1)))
        #             if thoughtType == "LocationThought":
        #                 lat = fake.latitude()
        #                 lng = fake.longitude()
        #                 locationName = fake.street_address()
        #                 json_location = {
        #                     'lat': str(lat),
        #                     'lng': str(lng),
        #                     'locationName': locationName,
        #                     'selectedLocationImage': "https://maps.googleapis.com/maps/api/staticmap?center=" + str(lat) + "," + str(lng)
        #                                              + "&zoom=14&size=500x300&maptype=roadmap&markers=color:red%7Clabel:Place%7C24.8354896,46.6003797&key=AIzaSyBRmUPUO4Y0209cXL0GTfkqoAtlBeg4NHg"
        #                 }
        #                 location = json.dumps(json_location)
        #                 thought = Thought.objects.create(thoughtType=thoughtType,text=fake.text(max_nb_chars=random.randint(5, 100)), user=user,
        #                                        privacy="friends",  location=location, is_repubble=bool(random.getrandbits(1)))
        #             if thoughtType == "ImageThought":
        #                 image = fake.file_name(category='image')
        #                 thought = Thought.objects.create(thoughtType=thoughtType, text=fake.text(max_nb_chars=random.randint(5, 100)), user=user,
        #                                        privacy="friends",location=location, thought_image=image, is_repubble=bool(random.getrandbits(1)))
        #             if thoughtType == "VideoThought":
        #                 video = fake.file_name(category='image')
        #                 thought = Thought.objects.create(thoughtType=thoughtType, text=fake.text(max_nb_chars=random.randint(5, 100)), user=user,
        #                                        privacy="friends", location=location, thought_video=video, is_repubble=bool(random.getrandbits(1)))
        #             if thoughtType == "StatusThought":
        #                 thought = Thought.objects.create(thoughtType=thoughtType, text=fake.text(max_nb_chars=random.randint(5, 100)), user=user,
        #                                        privacy="friends",
        #                                        location=location, status=fake.thought_status(), is_repubble=bool(random.getrandbits(1)))
        #             for to_be_friend_emotion in random.sample(Friend.objects.friends(user), random.randint(0, len(Friend.objects.friends(user)))):
        #                 Emotion.objects.create(user=to_be_friend_emotion, thought=thought, type=fake.thought_emotions())
        #             for to_be_friend_comment in random.sample(Friend.objects.friends(user), random.randint(0, len(Friend.objects.friends(user)))):
        #                 Comment.objects.create(user=to_be_friend_comment, thought=thought, text=fake.text(max_nb_chars=random.randint(5, 30)))
        self.stdout.write('Done creating data')