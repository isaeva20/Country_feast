from typing import Any
from rest_framework import viewsets, permissions, authentication
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core import paginator as django_paginator, exceptions
from rest_framework import viewsets, permissions, authentication
from django.contrib.auth import decorators, mixins
from .models import Country, Feast, City, Client
from .serializers import CountrySerializer, FeastSerializer, CitySerializer
from .forms import RegistrationForm


def home_page(request):
    return render(
        request,
        'index.html',
        {
            'countries': Country.objects.count(),
            'feasts': Feast.objects.count(),
            'cities': City.objects.count(),
        }
    )

def create_listview(model_class, plural_name, template):
    class CustomListView(mixins.LoginRequiredMixin, ListView):
        model = model_class
        template_name = template
        paginate_by = 10
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            instances = model_class.objects.all()
            paginator = django_paginator.Paginator(instances, 10)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{plural_name}_list'] = page_obj
            return context
    return CustomListView

def create_view(model, model_name, template, redirect_page):
    @decorators.login_required
    def view(request):
        id_ = request.GET.get('id', None)
        if not id_:
            return redirect(redirect_page)
        try:
            target = model.objects.get(id=id_) if id_ else None
        except exceptions.ValidationError:
            return redirect(redirect_page)
        if not target:
            return redirect_page(redirect_page)
        context = {model_name: target}
        return render(
            request,
            template,
            context,
        )
    return view

view_country = create_view(Country, 'country', 'entities/country.html', 'countries')
view_feast = create_view(Feast, 'feast', 'entities/feast.html', 'feasts')
view_city = create_view(City, 'city', 'entities/city.html', 'cities')

CountryListView = create_listview(Country, 'countries', 'catalog/countries.html')
FeastListView = create_listview(Feast, 'feasts', 'catalog/feasts.html')
CityListView = create_listview(City, 'cities', 'catalog/cities.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
            return redirect('homepage')
    else:
        form = RegistrationForm()
    return render(
        request,
        'registration/register.html',
        {'form': form},
    )

class MyPermission(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in ('GET', 'OPTIONS', 'HEAD'):
            return bool(request.user and request.user.is_authenticated)
        elif request.method in ('POST', 'DELETE', 'PUT'):
            return bool(request.user and request.user.is_superuser)
        return False
    

@decorators.login_required
def profile(request):
    if not request.user.is_superuser:
        client = Client.objects.get(user=request.user)
        attrs = 'user'
        client_data = {getattr(client, attrs)}
    else:
        client_data = {'You is superuser'}
    return render(
        request,
        'pages/profile.html',
        {
            'client_data': client_data,
        }
    )

class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [MyPermission]


class FeastViewSet(viewsets.ModelViewSet):
    serializer_class = FeastSerializer
    queryset = Feast.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [MyPermission]

class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [MyPermission]



