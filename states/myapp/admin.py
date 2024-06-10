"""Module for admin."""

from django.contrib import admin
from .models import Country, Feast, City, Client, CountryToFeast, CountryClient

class CountryFeastInline(admin.TabularInline):
    """Inline for CountryFeast model."""

    model = CountryToFeast
    extra = 1

class CountryClientInline(admin.TabularInline):
    """Inline for CountryClient model."""

    model = CountryClient
    extra = 1

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Admin for Client model."""

    model = Client
    inlines = (CountryClientInline,)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Admin for Country model."""

    model = Country
    inlines = (CountryFeastInline,)

@admin.register(Feast)
class FeastAdmin(admin.ModelAdmin):
    """Admin for Feast model."""

    model = Feast
    inlines = (CountryFeastInline,)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Admin for City model."""

    model = City

@admin.register(CountryToFeast)
class CountryToFeastAdmin(admin.ModelAdmin):
    """Admin for Country with Feast model."""

    model = CountryToFeast
