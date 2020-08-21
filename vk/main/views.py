from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialToken
import requests
from random import randint


def index(request):
    return render(request, 'main/index.html')


def profile(request):
    if request.user.is_authenticated:
        try:

            first_name = SocialAccount.objects.filter(user=request.user, provider='vk')[0].extra_data['first_name']
            user_id = SocialAccount.objects.filter(user=request.user, provider='vk')[0].extra_data['id']
            last_name = SocialAccount.objects.filter(user=request.user, provider='vk')[0].extra_data['last_name']
            TOKEN = SocialToken.objects.filter(account__user=request.user, account__provider='vk')

            def get_friend():
                offset = randint(0, 9)
                r = requests.get("https://api.vk.com/method/friends.get",
                                 params={'user_id': user_id, "v": 5.122, 'count': 5, "offset": offset,
                                         "access_token": TOKEN, 'fields': "photo_200_orig,domain"})
                response = r.json()

                friends_resp = response['response']['items']
                return friends_resp

            friends = get_friend()

            context = {
                'first_name': first_name,
                'last_name': last_name,
                'friends': friends,

            }

            return render(request, 'main/profile.html', context)
        except:
            pass
    else:
        return render(request, 'main/redirect.html')
