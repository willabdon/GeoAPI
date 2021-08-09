import pdb
import factory

from django.test import TestCase
from django.contrib.gis.geos import Polygon
from collections import OrderedDict

from rest_framework.test import APIRequestFactory
from rest_framework_gis.fields import GeoJsonDict

from providers.tests import ProviderFactory
from .models import ServiceArea
from .serializers import ServiceAreaSerializer


class ServiceAreaFactory(factory.django.DjangoModelFactory):
    price = 1

    class Meta:
        model = ServiceArea


polygon = Polygon([
    [1, 1],
    [1, 2],
    [2, 2],
    [2, 1],
    [1, 1],
])

polygon2 = Polygon([
    [3, 3],
    [3, 7],
    [7, 7],
    [7, 3],
    [3, 3],
])


class TestSerializer(TestCase):

    def test_service_area_serializer(self):
        provider = ProviderFactory()
        service_area = ServiceAreaFactory(
            coordinates=polygon, provider=provider)
        data = ServiceAreaSerializer(instance=service_area).data
        self.assertEqual(data, {
            'type': 'Feature',
            'geometry': GeoJsonDict([
                ('type', 'Polygon'),
                ('coordinates', [[[1.0, 1.0], [1.0, 2.0], [2.0, 2.0], [2.0, 1.0], [1.0, 1.0]]])]),
            'properties': OrderedDict([('pk', service_area.pk), ('name', ''), ('price', '1.00000'), ('provider', '')])})


class TestAPI(TestCase):
    client = APIRequestFactory()

    data = {
        'name': 'name',
        'price': 100,
        'coordinates': polygon
    }

    def test_create_service_area(self):
        r_data = {**self.data}
        r_data['coordinates'] = GeoJsonDict([
            ('type', 'Polygon'),
            ('coordinates', [[[1.0, 1.0], [1.0, 2.0], [2.0, 2.0], [2.0, 1.0], [1.0, 1.0]]])])
        provider = ProviderFactory()
        r_data['provider_id'] = provider.pk

        response = self.client.post(
            '/service_area/', r_data, content_type='application/json')
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertDictContainsSubset({
            'geometry': GeoJsonDict([
                ('type', 'Polygon'),
                ('coordinates', [[[1.0, 1.0], [1.0, 2.0], [2.0, 2.0], [2.0, 1.0], [1.0, 1.0]]])])
        }, data)

    def test_update_service_area(self):
        provider = ProviderFactory()
        service_area = ServiceAreaFactory(**self.data, provider=provider)
        update_data = self.data
        update_data['provider_id'] = provider.pk
        update_data['name'] = 'name_updated'
        update_data['coordinates'] = GeoJsonDict([
            ('type', 'Polygon'),
            ('coordinates', [[[1.0, 1.0], [1.0, 2.0], [2.0, 2.0], [2.0, 1.0], [1.0, 1.0]]])])
        response = self.client.put(
            f'/service_area/{service_area.pk}/', update_data, content_type='application/json')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {
            'type': 'Feature',
            'geometry': GeoJsonDict([
                ('type', 'Polygon'),
                ('coordinates', [[[1.0, 1.0], [1.0, 2.0], [2.0, 2.0], [2.0, 1.0], [1.0, 1.0]]])]),
            'properties': OrderedDict([
                ('pk', service_area.pk),
                ('name', 'name_updated'),
                ('price', '100.00000'),
                ('provider', '')])})

    def test_delete_service_area(self):
        provider = ProviderFactory()
        service_area = ServiceAreaFactory(**self.data, provider=provider)
        response = self.client.delete(f'/service_area/{service_area.pk}/')
        self.assertEqual(response.status_code, 204)

    def test_list_service_area(self):
        response = self.client.get(f'/service_area/')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {
            'count': 0,
            'next': None,
            'previous': None,
            'results': {
                'type': 'FeatureCollection',
                'features': []
            }
        })

    def test_retrieve_service_area(self):
        provider = ProviderFactory()
        service_area = ServiceAreaFactory(**self.data, provider=provider)
        response = self.client.get(f'/service_area/{service_area.pk}/')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {
            'type': 'Feature',
            'geometry': GeoJsonDict([
                ('type', 'Polygon'),
                ('coordinates', [[[1.0, 1.0], [1.0, 2.0], [2.0, 2.0], [2.0, 1.0], [1.0, 1.0]]])]),
            'properties': OrderedDict([
                ('pk', service_area.pk),
                ('name', 'name'),
                ('price', '100.00000'),
                ('provider', '')])})

    def test_list_service_area_with_coordinates_filter(self):
        provider = ProviderFactory()
        service_area1 = ServiceAreaFactory(name='name', price=100, coordinates=polygon, provider=provider)
        service_area2 = ServiceAreaFactory(name='name', price=100, coordinates=polygon, provider=provider)
        ServiceAreaFactory(name='name', price=100, coordinates=polygon2, provider=provider)
        response = self.client.get(f'/service_area/', { 'coordinates': '1.4,1.5'})
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 2)
        sa_pks = [service_area1.pk, service_area2.pk]
        response_sa_pks = [x['properties']['pk'] for x in data['results']['features']]
        self.assertEqual(sa_pks, response_sa_pks)
