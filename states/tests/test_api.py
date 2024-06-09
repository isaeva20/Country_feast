from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status

from myapp.models import Country, Feast, City


def create_viewset_test(model_class, url, creation_attrs):
    class ViewSetTest(TestCase):
        def setUp(self):
            self.client = APIClient()
            self.user = User.objects.create_user(username='user', password='user')
            self.superuser = User.objects.create_user(
                username='superuser', password='superuser', is_superuser=True,
            )
            self.user_token = Token.objects.create(user=self.user)
            self.superuser_token = Token.objects.create(user=self.superuser)

        def get(self, user: User, token: Token):
            self.client.force_authenticate(user=user, token=token)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_get_by_user(self):
            self.get(self.user, self.user_token)

        def test_get_by_superuser(self):
            self.get(self.superuser, self.superuser_token)

        def manage(self, user: User, token: Token, post_status: int, put_status: int, delete_status: int):
            self.client.force_authenticate(user=user, token=token)

            response = self.client.post(url, creation_attrs)
            self.assertEqual(response.status_code, post_status)

            created_id = model_class.objects.create(**creation_attrs).id

            response = self.client.put(f'{url}{created_id}/', creation_attrs)
            self.assertEqual(response.status_code, put_status)

            response = self.client.delete(f'{url}{created_id}/')
            self.assertEqual(response.status_code, delete_status)

        def test_manage_user(self):
            self.manage(
                self.user, self.user_token,
                post_status=status.HTTP_403_FORBIDDEN,
                put_status=status.HTTP_403_FORBIDDEN,
                delete_status=status.HTTP_403_FORBIDDEN,
            )

        def test_manage_superuser(self):
            self.manage(
                self.superuser, self.superuser_token,
                post_status=status.HTTP_201_CREATED,
                put_status=status.HTTP_200_OK,
                delete_status=status.HTTP_204_NO_CONTENT,
            )

    return ViewSetTest

CountryViewSetTest = create_viewset_test(Country, '/api/countries/', {'name': 'A', 'area_country': 100453})
FeastViewSetTest = create_viewset_test(Feast, '/api/feasts/', {'title': 'nfrnrfr'})
CityViewSetTest = create_viewset_test(City, '/api/cities/', {'name': 'fkfff'})

