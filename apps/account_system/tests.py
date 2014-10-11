# -*- encoding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.contrib.sites.models import Site
from allauth.account.models import EmailAddress, EmailConfirmation
from apps.account_system.models import User
from django.conf import settings
from django.test.utils import override_settings

@override_settings(
SITE_ID = 2
)
class CrearUsuarioTestCase(TestCase):

    def setUp(self):
        if 'allauth.socialaccount' in settings.INSTALLED_APPS:
            # Otherwise ImproperlyConfigured exceptions may occur
            from allauth.socialaccount.models import SocialApp
            sa = SocialApp.objects.create(name='testfb',
                                          provider='facebook')
            sa.sites.add(Site.objects.get_current())


    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        # First check for the default behavior
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        response = c.post('/accounts/login/', {'username': '1', 'password': '1'})

    def test_username_containing_at(self):
        user = User.objects.create(username='@raymond.penners')
        user.set_password('psst')
        user.save()
        EmailAddress.objects.create(user=user,
                                    email='raymond.penners@gmail.com',
                                    primary=True,
                                    verified=True)
        resp = self.client.post(reverse('account_login'),
                                {'login': '@raymond.penners',
                                 'password': 'psst'})
        self.assertEqual(resp['location'],
                         'http://testserver'+settings.LOGIN_REDIRECT_URL)
