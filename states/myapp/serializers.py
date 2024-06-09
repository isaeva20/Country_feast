from rest_framework.serializers import HyperlinkedModelSerializer
from .models import Country, Feast, City


class CountrySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class FeastSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Feast
        fields = '__all__'

class CitySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = City
        fields = '__all__'

