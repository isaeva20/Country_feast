"""Module for testing forms."""

from django.test import TestCase
from django.contrib.auth.models import User
from myapp.forms import RegistrationForm

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
    """
    A test case for validating the RegistrationForm.
    """
    def test_valid(self):
        """
        Verifies that the RegistrationForm validates correctly with valid data.
        """
        self.assertTrue(RegistrationForm(data=valid_data).is_valid())

    def test_not_matching_passwords(self):
        """
        Checks that the RegistrationForm rejects
        submissions with non-matching passwords.
        """
        self.assertFalse(RegistrationForm(data=not_matching_password).is_valid())

    def test_short_password(self):
        """
        Ensures the RegistrationForm rejects submissions with short passwords.
        """
        self.assertFalse(RegistrationForm(data=short_password).is_valid())

    def test_invalid_email(self):
        """
        Verifies that the RegistrationForm rejects
        submissions with invalid email addresses.
        """
        self.assertFalse(RegistrationForm(data=invalid_email).is_valid())

    def test_common_password(self):
        """
        Confirms that the RegistrationForm rejects submissions with common passwords.
        """
        self.assertFalse(RegistrationForm(data=common_password).is_valid())

    def test_existing_user(self):
        """
        Ensures the RegistrationForm rejects submissions
        for usernames that already exist.
        """
        User.objects.create(username=valid_data['username'], password='abc')
        self.assertFalse(RegistrationForm(data=valid_data).is_valid())
