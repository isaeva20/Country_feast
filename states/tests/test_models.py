from django.test import TestCase
from typing import Iterable
from django.core.exceptions import ValidationError
from datetime import date, datetime, timezone, timedelta
from django.contrib.auth.models import User

from myapp.models import Country, Feast, City, Client, check_created, check_modified

class CountryModelTests(TestCase):
    def test_country_fields(self):
        country = Country.objects.create(
            name='Test Country',
            population=100000,
            area_country=50000,
            hymn='National Anthem'
        )
        self.assertEqual(country.name, 'Test Country')
        self.assertEqual(country.population, 100000)
        self.assertEqual(country.area_country, 50000)
        self.assertEqual(country.hymn, 'National Anthem')


class FeastModelTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name='Test Country')

    def test_feast_fields(self):
        feast = Feast.objects.create(title='Test Feast', date_of_feast='2024-01-01', description='A test feast.')
        feast.countries.add(self.country)
        self.assertEqual(feast.title, 'Test Feast')
        self.assertEqual(feast.date_of_feast, '2024-01-01')
        self.assertEqual(feast.description, 'A test feast.')

    def test_feast_many_to_many(self):
        feast = Feast.objects.create(title='Test Feast')
        country = Country.objects.create(name='Another Test Country')
        feast.countries.add(country)
        self.assertIn(country, feast.countries.all())


class CityModelTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name='Test Country')

    def test_city_fields(self):
        city = City.objects.create(
            country=self.country,
            name='Test City',
            population=50000,
            coordinates='40.7128, 74.0060',
            area_city=150
        )
        self.assertEqual(city.name, 'Test City')
        self.assertEqual(city.population, 50000)
        self.assertEqual(city.coordinates, '40.7128, 74.0060')
        self.assertEqual(city.area_city, 150)

    def test_city_foreign_key(self):
        city = City.objects.create(
            country=self.country,
            name='Test City',
            population=50000,
            coordinates='40.7128° N, 74.0060° W',
            area_city=150
        )
        self.assertEqual(city.country, self.country)


class ClientTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc', first_name='abc', last_name='abc', password='abc')

    def test_create_and_str(self):
        self.assertEqual(str(Client.objects.create(user=self.user)), 'abc (abc abc)')

PAST = datetime(datetime.today().year-1, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)
FUTURE = datetime(datetime.today().year+1, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)

validators_pass = (
    (check_created, PAST),
    (check_modified, PAST),
)

validators_fail = (
    (check_created, FUTURE),
    (check_modified, FUTURE),
)

def create_val_test(validator, value, valid=True):
    def test(self):
        with self.assertRaises(ValidationError):
            validator(value)
    return lambda _ : validator(value) if valid else test

invalid_methods = {f'test_inval_{args[0].__name__}': create_val_test(*args, valid=False) for args in validators_fail}
valid_methods = {f'test_val_{args[0].__name__}': create_val_test(*args) for args in validators_pass}

ValidatorsTest = type('ValidatorsTest', (TestCase,), invalid_methods | valid_methods)
