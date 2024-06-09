from django.contrib import admin
from .models import Country, Feast, City, Client, CountryToFeast, CountryClient


class CountryFeastInline(admin.TabularInline):
    model = CountryToFeast
    extra = 1

class CountryClientInline(admin.TabularInline):
    model = CountryClient
    extra = 1

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    inlines = (CountryClientInline,)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    model = Country
    inlines = (CountryFeastInline,)

@admin.register(Feast)
class FeastAdmin(admin.ModelAdmin):
    model = Feast
    inlines = (CountryFeastInline,)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    model = City

@admin.register(CountryToFeast)
class CountryToFeastAdmin(admin.ModelAdmin):
    model = CountryToFeast