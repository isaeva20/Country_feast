"""Module for urls."""

from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'countries', views.CountryViewSet)
router.register(r'feasts', views.FeastViewSet)
router.register(r'cities', views.CityViewSet)

urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('countries/', views.CountryListView.as_view(), name='countries'),
    path('country/', views.view_country, name='country'),
    path('feasts/', views.FeastListView.as_view(), name='feasts'),
    path('feast/', views.view_feast, name='feast'),
    path('cities/', views.CityListView.as_view(), name='cities'),
    path('city/', views.view_city, name='city'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('api/', include(router.urls), name='api'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('profile/', views.profile, name='profile'),
]
