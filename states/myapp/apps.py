"""Module for application."""

from django.apps import AppConfig

class MyappConfig(AppConfig):
    """
    Configuration class for the 'myapp' Django application.
    
    This class is used to configure the behavior of the 'myapp' application.
    It specifies the default model field type and the application's name.
    
    Attributes:
        default_auto_field (str): The default model field type for models in this application.
        name (str): The name of the application, corresponding to the module name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
