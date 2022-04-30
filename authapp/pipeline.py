from datetime import datetime
from urllib.parse import urlencode, urlunparse
import requests
from django.conf import settings
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    pass
    if backend.name != 'vk-oauth2':
        return
    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(dict(fields=','.join(('bdate', 'sex',
                                                          'about', 'photo_200')),
                                         access_token=response['access_token'],
                                         v='5.92')), None))

    resp = requests.get(api_url)
    if not resp.ok:
        return

    data = resp.json()['response'][0]

    photo_link = data.get('photo_200')
    if photo_link:
        photo_get = requests.get(photo_link)
        photo_path = f'{settings.MEDIA_ROOT}/user_images/{user.pk}_{user.username}.jpg'
        with open(photo_path, 'wb') as file:
            file.write(photo_get.content)
        user.avatar = photo_path

    if data.get('sex'):
        user.userprofile.gender = UserProfile.MALE if data['sex'] == 2 else UserProfile.FEMALE

    if data.get('about'):
        user.userprofile.about = data['about']

    if data.get('bdate'):
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        else:
            user.age = age

    if response.get('email'):
        user.email = response['email']

    user.save()


