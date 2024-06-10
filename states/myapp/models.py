"""Module for models."""

from typing import Any
from uuid import uuid4
from datetime import datetime, timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf.global_settings import AUTH_USER_MODEL

class UUIDMixin(models.Model):
    """Class which adds id field."""

    id = models.UUIDField(primary_key=True, blank=True, editable=False, default=uuid4)

    class Meta:
        """Inner class metadata for abstract base classes."""

        abstract = True

def get_datetime():
    """Getting the current time."""
    return datetime.now(timezone.utc)

def check_created(dt: datetime) -> None:
    """Check creation time.

    Args:
        dt (datetime): accepted time

    Raises:
        ValidationError: time check error
    """
    if dt > get_datetime():
        raise ValidationError(
            _('Datetime is bigger than current datetime!'),
            params={'created': dt}
        )
def check_modified(dt: datetime) -> None:
    """
    Validates that a given datetime is not greater than the current datetime.
    """
    if dt > get_datetime():
        raise ValidationError(
            _('Datetime is bigger than current datetime!'),
            params={'modified': dt}
        )

def check_positive(population):
    """Check the population is positive.

    Args:
        population (int | float): population

    Raises:
        ValidationError: error for django admin
    """
    if population < 0:
        raise ValueError(_('Population cannot be negative.'))

class CreatedMixin(models.Model):
    """Class that adds a date and time field creation."""
    created = models.DateTimeField(
        _('created'),
        null=True, blank=True,
        default=get_datetime,
        validators=[
            check_created,
        ]
    )

    class Meta:
        """Inner class metadata for abstract base classes."""

        abstract = True

class ModifiedMixin(models.Model):
    """Class that adds a last updated date and time field."""

    modified = models.DateTimeField(
        _('modified'),
        null=True, blank=True,
        default=get_datetime,
        validators=[
            check_modified,
        ]
    )

    class Meta:
        """Inner class metadata for abstract base classes."""

        abstract = True

class CountryManager(models.Manager):
    """Module for country manager."""

    def create(self, **kwargs: Any) -> Any:
        """
        Calls the superclass's create method
        to create a new instance of the model.
        """
        return super().create(**kwargs)

class Country(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Module for country."""

    name = models.TextField(_('name'), null=False, blank=False)
    population = models.PositiveIntegerField(
        _('population'),
        null=True,
        blank=True,
        validators=[check_positive])
    area_country = models.PositiveIntegerField(
        _('area country'),
        null=False,
        blank=False,
        default=0
    )
    hymn = models.TextField(_('hymn'), null=True, blank=True)
    objects = CountryManager()

    def __str__(self):
        """Returns a string representation of the object."""

        return f'{self.name}'

    class Meta:
        """Inner class metadata for abstract base classes."""

        db_table = '"states"."country"'
        verbose_name = _('country')
        verbose_name_plural = _('countries')


class Feast(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Module for feast."""

    title = models.TextField(_('title'), null=False, blank=False)
    date_of_feast = models.DateField(_('date of feast'), null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)

    countries = models.ManyToManyField(
        Country,
        through='CountryToFeast',
        verbose_name=_('countries'))

    def __str__(self):
        """Returns a string representation of the object."""

        return f'{self.title}'

    class Meta:
        """Inner class metadata for abstract base classes."""

        db_table = '"states"."feast"'
        verbose_name = _('feast')
        verbose_name_plural = _('feasts')

class City(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Module for city."""

    country = models.ForeignKey(
        Country,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_('country')
    )
    name = models.TextField(_('name'), null=False, blank=False)
    population = models.PositiveIntegerField(_('population'), null=True, blank=True)
    coordinates = models.TextField(_('coordinates'), null=True, blank=True)
    area_city = models.PositiveIntegerField(_('area city'), null=True, blank=True)

    def __str__(self) -> str:
        """Returns a string representation of the object."""

        return f'{self.name}, {self.population}, {self.coordinates}, {self.area_city} km'

    class Meta:
        """Inner class metadata for abstract base classes."""

        db_table = '"states"."city"'
        verbose_name = _('city')
        verbose_name_plural = _('cities')

class CountryToFeast(UUIDMixin, CreatedMixin):
    """Module for country with feast."""

    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('country'))
    feast = models.ForeignKey(Feast, on_delete=models.CASCADE, verbose_name=_('feast'))

    def __str__(self) -> str:
        """Returns a string representation of the object."""

        return f'{self.country}: {self.feast}'

    class Meta:
        """Inner class metadata for abstract base classes."""

        db_table = '"states"."country_to_feast"'
        unique_together = (
            ('country', 'feast'),
        )
        verbose_name = _('Relationship country feast')
        verbose_name_plural = _('Relationships country feast')

class Client(CreatedMixin, ModifiedMixin):
    """Module for client."""

    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE, primary_key=True,
    )
    countries = models.ManyToManyField(
        Country,
        through='CountryClient',
        verbose_name=_('countries')
    )

    def save(self, *args, **kwargs) -> None:
        """
        Overrides the save method to perform custom checks before saving the object.
    
        This method calls custom functions check_created() and check_modified()
        to validate the object's creation and modification timestamps. If both
        checks pass, it proceeds to call the superclass's save method to persist
        the changes to the database.
        """
        check_created(self.created)
        check_modified(self.modified)
        return super().save(*args, **kwargs)

    class Meta:
        """Inner class metadata for abstract base classes."""

        db_table = '"states"."client"'
        verbose_name = _('client')
        verbose_name_plural = _('clients')

class CountryClient(UUIDMixin, CreatedMixin):
    """Module for country with client."""

    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('country'))
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_('client'))

    class Meta:
        """Inner class metadata for abstract base classes."""

        db_table = '"states"."country_client"'
        unique_together = (
            ('country', 'client'),
        )
        verbose_name = _('relationship country client')
        verbose_name_plural = _('relationships country client')
