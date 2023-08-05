from django.test import TestCase

from .models import AppSettings


class TestCase(TestCase):

    def test_001(self):

        object_ = AppSettings.objects.create()
        object_.app_name = 'django_app_settings'
        object_.key = 'active'
        object_.value_int = 1
        object_.value_string = '1'
        object_.save()

        self.assertEqual(object_.value_int, 1)
        self.assertEqual(object_.value_string, '1')
