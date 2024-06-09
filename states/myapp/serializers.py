from rest_framework.serializers import HyperlinkedModelSerializer
from .models import Country, Feast, City


class CountrySerializer(HyperlinkedModelSerializer):
    """Serializer for the Country model."""

    class Meta:
        """Settings for country serializer."""

        model = Country
        fields = '__all__'

class FeastSerializer(HyperlinkedModelSerializer):
    """Serializer for the Feast model."""

    class Meta:
        """Settings for feast serializer."""

        model = Feast
        fields = '__all__'

class CitySerializer(HyperlinkedModelSerializer):
    """Serializer for the City model."""

    class Meta:
        """Settings for city serializer."""

        model = City
        fields = '__all__'

