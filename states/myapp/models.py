from typing import Any
from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timezone
from django.core.exceptions import ValidationError
from django.conf.global_settings import AUTH_USER_MODEL

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, blank=True, editable=False, default=uuid4)

    class Meta:
        abstract = True

def get_datetime():
    return datetime.now(timezone.utc)

def check_created(dt: datetime) -> None:
    if dt > get_datetime():
        raise ValidationError(
            _('Datetime is bigger than current datetime!'),
            params={'created': dt}
        )
def check_modified(dt: datetime) -> None:
    if dt > get_datetime():
        raise ValidationError(
            _('Datetime is bigger than current datetime!'),
            params={'modified': dt}
        )
    
def check_positive(population):
    if population < 0:
        raise ValueError(_('Population cannot be negative.'))
    
class CreatedMixin(models.Model):
    created = models.DateTimeField(
        _('created'),
        null=True, blank=True,
        default=get_datetime, 
        validators=[
            check_created,
        ]
    )

    class Meta:
        abstract = True

class ModifiedMixin(models.Model):
    modified = models.DateTimeField(
        _('modified'),
        null=True, blank=True,
        default=get_datetime, 
        validators=[
            check_modified,
        ]
    )

    class Meta:
        abstract = True

class CountryManager(models.Manager):
    def create(self, **kwargs: Any) -> Any:
        return super().create(**kwargs)

class Country(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.TextField(_('name'), null=False, blank=False)
    population = models.PositiveIntegerField(_('population'), null=True, blank=True, validators=[check_positive])
    area_country = models.PositiveIntegerField(_('area country'), null=False, blank=False, default=0)
    hymn = models.TextField(_('hymn'), null=True, blank=True)
    objects = CountryManager()

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = '"states"."country"'
        verbose_name = _('country')
        verbose_name_plural = _('countries')


class Feast(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(_('title'), null=False, blank=False)
    date_of_feast = models.DateField(_('date of feast'), null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)

    countries = models.ManyToManyField(Country, through='CountryToFeast', verbose_name=_('countries'))

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        db_table = '"states"."feast"'
        verbose_name = _('feast')
        verbose_name_plural = _('feasts')

class City(UUIDMixin, CreatedMixin, ModifiedMixin):
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE, verbose_name=_('country'))
    name = models.TextField(_('name'), null=False, blank=False)
    population = models.PositiveIntegerField(_('population'), null=True, blank=True)
    coordinates = models.TextField(_('coordinates'), null=True, blank=True)
    area_city = models.PositiveIntegerField(_('area city'), null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name}, {self.population}, {self.coordinates}, {self.area_city} km'
    
    class Meta:
        db_table = '"states"."city"'
        verbose_name = _('city')
        verbose_name_plural = _('cities')

class CountryToFeast(UUIDMixin, CreatedMixin):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('country'))
    feast = models.ForeignKey(Feast, on_delete=models.CASCADE, verbose_name=_('feast'))

    def __str__(self) -> str:
        return f'{self.country}: {self.feast}'

    class Meta:
        db_table = '"states"."country_to_feast"'
        unique_together = (
            ('country', 'feast'),
        )
        verbose_name = _('Relationship country feast')
        verbose_name_plural = _('Relationships country feast')

class Client(CreatedMixin, ModifiedMixin):
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE, primary_key=True,
    )
    countries = models.ManyToManyField(Country, through='CountryClient', verbose_name=_('countries'))
    
    def save(self, *args, **kwargs) -> None:
        check_created(self.created)
        check_modified(self.modified)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.user.username} ({self.user.first_name} {self.user.last_name})'
    
    class Meta:
        db_table = '"states"."client"'
        verbose_name = _('client')
        verbose_name_plural = _('clients')

class CountryClient(UUIDMixin, CreatedMixin):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('country'))
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_('client'))

    class Meta:
        db_table = '"states"."country_client"'
        unique_together = (
            ('country', 'client'),
        )
        verbose_name = _('relationship country client')
        verbose_name_plural = _('relationships country client')

        