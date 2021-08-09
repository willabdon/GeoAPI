from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from providers.models import Provider
from .models import ServiceArea


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    provider = serializers.CharField(source='provider.name', read_only=True)
    provider_id = PrimaryKeyRelatedField(queryset=Provider.objects.all(
    ), required=True, write_only=True, source='provider')

    class Meta:
        model = ServiceArea
        fields = ('pk', 'name', 'price', 'provider', 'provider_id')
        geo_field = 'coordinates'


class ServiceAreaSerializerRepresentation(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True)
    coordinates = serializers.ListField(
        child=serializers.ListField(child=serializers.FloatField()))
    properties = ServiceAreaSerializer()

    class Meta:
        model = ServiceArea
        fields = ('type', 'coordinates', 'properties')

    def get_type(self):
        return 'Polygon'
