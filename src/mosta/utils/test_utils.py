import random
import string

from allauth.account.models import EmailAddress
from django.contrib.auth.models import User


def get_random_string(length=10, charset=string.ascii_letters):
    return ''.join(random.choices(charset, k=length))


def create_random_user():
    username = get_random_string()
    email = '{}@test.com'.format(username)
    user = User.objects.create(
        username=username,
        email=email
    )
    EmailAddress.objects.create(
        user=user,
        email=email,
        verified=True,
        primary=True
    )
    return user
