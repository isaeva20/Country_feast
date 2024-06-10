"""Modeule for views test."""

from django.test import TestCase
from django.test.client import Client as TestClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from myapp.models import Country, Feast, City, Client

def create_method_with_auth(url, page_name, template, login=False):
    """
    Creates a test method that makes authenticated GET 
    requests to specified URLs and verifies the response.
    """
    def method(self):
        """
        Performs authenticated GET requests
        to specified URLs and verifies the response.
        """
        self.client = TestClient()
        if login:
            user = User.objects.create(username='user', password='user')
            Client.objects.create(user=user)
            self.client.force_login(user=user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, template)

        response = self.client.get(reverse(page_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    return method

def create_method_no_auth(url):
    """
    Creates a test method that sends an unauthenticated GET
    request to a specified URL and verifies the response.
    """
    def method(self):
        """
        Sends an unauthenticated GET request
        to a specified URL and verifies the response.
        """
        self.client = TestClient()
        self.assertEqual(self.client.get(url).status_code, status.HTTP_302_FOUND)
    return method

def create_method_instance(url, page_name, template, model, creation_attrs):
    """
    Generates a test method that sets up a TestClient,
    creates a user and client, and interacts with a specified model.
    """
    def method(self):
        """
        Initializes a TestClient, creates a user,
        and associates a client with that user.
        """
        self.client = TestClient()
        user = User.objects.create(username='user', password='user')
        Client.objects.create(user=user)

        self.assertEqual(self.client.get(url).status_code, status.HTTP_302_FOUND)
        self.client.force_login(user=user)
        self.assertEqual(self.client.get(url).status_code, status.HTTP_302_FOUND)
        self.assertEqual(self.client.get(f'{url}?id=123').status_code, status.HTTP_302_FOUND)
        created_id = model.objects.create(**creation_attrs).id
        created_url = f'{url}?id={created_id}'
        created_reversed_url = f'{reverse(page_name)}?id={created_id}'
        response = self.client.get(created_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, template)
        self.assertEqual(self.client.get(created_reversed_url).status_code, status.HTTP_200_OK)

    return method

instance_pages = (
    (
        '/country/',
        'country',
        'entities/country.html',
        Country, {'name': 'adaaw', 'area_country': 1013022}
    ),
    ('/feast/', 'feast', 'entities/feast.html', Feast, {'title': 'dadqwd'}),
    ('/city/', 'city', 'entities/city.html', City, {'name': 'fsfsf'}),
)

pages = (
    ('/countries/', 'countries', 'catalog/countries.html'),
    ('/feasts/', 'feasts', 'catalog/feasts.html'),
    ('/cities/', 'cities', 'catalog/cities.html'),
    ('/profile/', 'profile', 'pages/profile.html'),
)

casual_pages = (
    ('', 'homepage', 'index.html'),
    ('/register/', 'register', 'registration/register.html'),
    ('/accounts/login/', 'login', 'registration/login.html'),
)

methods_with_auth = {f'test_{page[1]}':
                    create_method_with_auth(*page, login=True) for page in pages}
TestWithAuth = type('TestWithAuth', (TestCase,), methods_with_auth)

casual_methods = {f'test_with_auth_{page[1]}':
                create_method_with_auth(*page, login=True) for page in casual_pages}
casual_methods.update({f'test_no_auth_{page[1]}':
                    create_method_with_auth(*page, login=False) for page in casual_pages})
TestCasualPage = type('TestCasualPages', (TestCase,), casual_methods)

methods_no_auth = {f'test_{url}': create_method_no_auth(url) for url, _, _ in pages}
TestNoAuth = type('TestNoAuth', (TestCase,), methods_no_auth)

methods_intance = {f'test_{page[1]}':
                   create_method_instance(*page) for page in instance_pages}
TestInstancePages = type('TestInstancePages', (TestCase,), methods_intance)
