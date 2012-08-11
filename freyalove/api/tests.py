from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, AnonymousUser

from freyalove.users.models import Profile, Friendship

class SignInTest(TestCase):
    def setUp(self):
    	pass
    	