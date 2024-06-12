"""Module for views."""

from typing import Any
from rest_framework import viewsets, permissions, authentication
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core import paginator as django_paginator, exceptions
from django.contrib.auth import decorators, mixins
from .models import Country, Feast, City, Client
from .serializers import CountrySerializer, FeastSerializer, CitySerializer
from .forms import RegistrationForm


def home_page(request):
    """Home page."""

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
    """
    Creates a custom ListView for Django with pagination and login requirement.

    Args:
        model_class (type): The model class to be displayed in the view.
        plural_name (str): The plural name used in the template context.
        template (str): The template name to render the view.
        
    Returns:
        CustomListView: A subclass of Django's ListView with customizations.
    """
    class CustomListView(mixins.LoginRequiredMixin, ListView):
        """A custom Django ListView with login requirement, pagination, and dynamic context data."""

        model = model_class
        template_name = template
        paginate_by = 10
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            """
            Overrides the get_context_data method to include paginated
            model instances in the context.
            """
            context = super().get_context_data(**kwargs)
            instances = model_class.objects.all()
            paginator = django_paginator.Paginator(instances, 10)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{plural_name}_list'] = page_obj
            return context
    return CustomListView

def create_view(model, model_name, template, redirect_page):
    """
    Creates a view function for displaying a single instance of a model.
    
    This decorator-based view function retrieves a single instance of the specified model
    based on its ID from the GET parameters.
      If the ID is not provided or the instance does
    not exist, it redirects to the specified redirect page.
    
    Parameters:
        model (type): The Django model class for which to create the view.
        model_name (type): The name of the model class,
        used as the context variable name.
        template (type): The path to the HTML template to use for rendering the view.
        redirect_page (type): The URL pattern name or callable to redirect
        to if the ID is not provided or the instance does not exist.
    
    Returns:
        view: A view function that handles GET requests
        for a single instance of the specified model.
    """
    @decorators.login_required
    def view(request):
        """Renders a detail view for a specific model instance identified by an ID."""
        id_ = request.GET.get('id', None)
        if not id_:
            return redirect(redirect_page)
        try:
            target = model.objects.get(id=id_) if id_ else None
        except exceptions.ValidationError:
            return redirect(redirect_page)
        if not target:
            return redirect_page(redirect_page)
        if model_name == 'country':
            cities = City.objects.filter(country=target)
            feasts = Feast.objects.filter(countries=target)
            context = {model_name: target, 'cities': cities, 'feasts': feasts}
            return render(
                request,
                template,
                context,
            )
        if model_name == 'feast':
            countries = Country.objects.filter(feast=target)
            context = {model_name: target, 'countries': countries}
            return render(
                request,
                template,
                context,
            )
        else:
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
    """
    Handles user registration.
    
    This view displays a registration form if the request method is not POST.
    Upon receiving a POST request, it validates the submitted form data,
    creates a new User instance, associates it with a Client instance, and then
    redirects the user to the homepage.
    
    Parameters:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: An HTTP response object, 
        either redirecting to the homepage upon successful registration
                    or rendering the registration form.
    """
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
    """
    Custom permission class for checking user permissions.
    
    This class checks if the authenticated user is allowed to perform certain actions
    based on the HTTP method of the request. 
    Users must be authenticated for GET, OPTIONS, and HEAD methods,
    and must also be superusers for POST, DELETE, and PUT methods.
    
    Methods:
        has_permission(self, request, _): Checks if the current user has permission 
        to access the requested resource.
    """
    def has_permission(self, request, _):
        """ 
        Checks if the request should be granted permission
        based on the request method and user roles.
        """
        if request.method in ('GET', 'OPTIONS', 'HEAD'):
            return bool(request.user and request.user.is_authenticated)
        elif request.method in ('POST', 'DELETE', 'PUT'):
            return bool(request.user and request.user.is_superuser)
        return False

@decorators.login_required
def profile(request):
    """
    Displays the user's profile.
    
    This view checks if the current user is a superuser. 
    If not, it fetches the associated Client
    instance and prepares data for display. 
    If the user is a superuser, a special message is prepared instead.
    
    Parameters:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: An HTTP response object, rendering the user's profile page.
    """
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
    """A ViewSet for managing country resources."""

    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [MyPermission]


class FeastViewSet(viewsets.ModelViewSet):
    """A ViewSet for managing country resources."""

    serializer_class = FeastSerializer
    queryset = Feast.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [MyPermission]

class CityViewSet(viewsets.ModelViewSet):
    """A ViewSet for managing country resources."""

    serializer_class = CitySerializer
    queryset = City.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [MyPermission]
