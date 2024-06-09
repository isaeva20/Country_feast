from django.test import TestCase
from myapp.forms import RegistrationForm
from django.contrib.auth.models import User

valid_data = {
    'username': 'abc',
    'first_name': 'abc',
    'last_name': 'abc',
    'email': 'email@email.com',
    'password1': 'jdjjYYj223',
    'password2': 'jdjjYYj223',
}

not_matching_password = valid_data.copy()
not_matching_password['password2'] = 'abc'

invalid_email = valid_data.copy()
invalid_email['email'] = 'abc'

short_password = valid_data.copy()
short_password['password1'] = 'abc'
short_password['password2'] = 'abc'

common_password = valid_data.copy()
common_password['password1'] = 'abcdef123'
common_password['password2'] = 'abcdef123'

class TestRegistrationForm(TestCase):
    def test_valid(self):
        self.assertTrue(RegistrationForm(data=valid_data).is_valid())

    def test_not_matching_passwords(self):
        self.assertFalse(RegistrationForm(data=not_matching_password).is_valid())
        
    def test_short_password(self):
        self.assertFalse(RegistrationForm(data=short_password).is_valid())

    def test_invalid_email(self):
        self.assertFalse(RegistrationForm(data=invalid_email).is_valid())

    def test_common_password(self):
        self.assertFalse(RegistrationForm(data=common_password).is_valid())

    def test_existing_user(self):
        User.objects.create(username=valid_data['username'], password='abc')
        self.assertFalse(RegistrationForm(data=valid_data).is_valid())