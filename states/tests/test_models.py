"""Module for models test."""

from datetime import datetime, timezone
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from myapp.models import Country, Feast, City, Client, check_created, check_modified

class CountryModelTests(TestCase):
    """
    A test case for validating the fields of the Country model.
    """
    def test_country_fields(self):
        """
        Verifies the assignment of fields
        in a newly created Country instance.
        """
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
    """
    A test case for validating the fields and
    many-to-many relationships of the Feast model.
    """
    def setUp(self):
        """
        Sets up the test environment by creating a Country instance.
        """
        self.country = Country.objects.create(name='Test Country')

    def test_feast_fields(self):
        """
        Verifies the assignment of fields in a newly created Feast instance.
        """
        feast = Feast.objects.create(
            title='Test Feast',
            date_of_feast='2024-01-01',
            description='A test feast.'
        )
        feast.countries.add(self.country)
        self.assertEqual(feast.title, 'Test Feast')
        self.assertEqual(feast.date_of_feast, '2024-01-01')
        self.assertEqual(feast.description, 'A test feast.')

    def test_feast_many_to_many(self):
        """
        Tests the many-to-many relationship between the Feast and Country models.
        """
        feast = Feast.objects.create(title='Test Feast')
        country = Country.objects.create(name='Another Test Country')
        feast.countries.add(country)
        self.assertIn(country, feast.countries.all())


class CityModelTests(TestCase):
    """
    A test case for testing the functionality of the City model.
    """
    def setUp(self):
        """
        Set up the test environment by creating a Country instance.
        """
        self.country = Country.objects.create(name='Test Country')

    def test_city_fields(self):
        """
        Test that a city object can be created
        with the expected fields and values.
        """
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
        """
        Test that the foreign key relationship between
        City and Country models works correctly.
        """
        city = City.objects.create(
            country=self.country,
            name='Test City',
            population=50000,
            coordinates='40.7128, 74.0060',
            area_city=150
        )
        self.assertEqual(city.country, self.country)


class ClientTest(TestCase):
    """
    A test case for testing the functionality of the Client model.
    """
    def setUp(self):
        """
        Set up the test environment by creating a User instance.
        """
        self.user = User.objects.create(
            username='abc',
            first_name='abc',
            last_name='abc',
            password='abc'
        )

    def test_create_and_str(self):
        """
        Test that a client object can be created
        and its string representation matches the expected format.
        """
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
    """
    Dynamically creates a test method that checks the validity
    of a given value using a provided validator function.
    """
    def test(self):
        """
        Checks if calling the provided validator function
        with the given value raises a ValidationError.
        """
        with self.assertRaises(ValidationError):
            validator(value)
    return lambda _ : validator(value) if valid else test

invalid_methods = {f'test_inval_{args[0].__name__}':
                   create_val_test(*args, valid=False) for args in validators_fail}
valid_methods = {f'test_val_{args[0].__name__}': create_val_test(*args) for args in validators_pass}

ValidatorsTest = type('ValidatorsTest', (TestCase,), invalid_methods | valid_methods)
