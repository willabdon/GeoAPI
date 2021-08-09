import factory

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .models import Provider
from .serializers import ProviderSerializer


class ProviderFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Provider


class TestSerializer(TestCase):
    def test_provider_serializer(self):
        provider = ProviderFactory()
        data = ProviderSerializer(instance=provider).data
        self.assertEqual(provider.name, data['name'])
        self.assertEqual(provider.email, data['email'])
        self.assertEqual(provider.phone, data['phone'])
        self.assertEqual(provider.language, data['language'])
        self.assertEqual(provider.currency, data['currency'])


class TestAPI(TestCase):
    client = APIRequestFactory()

    data = {
        'name': 'name',
        'email': 'email@gmail.com',
        'phone': '+5583996335122',
        'language': 'BR',
        'currency': 'BRL',
    }

    def test_create_provider(self):
        response = self.client.post('/provider/', self.data)
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertDictContainsSubset(self.data, data)

    def test_update_provider(self):
        provider = ProviderFactory(**self.data)
        update_data = self.data
        update_data['name'] = 'name_updated'
        response = self.client.put(
            f'/provider/{provider.pk}/', update_data, content_type='application/json')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset(update_data, data)

    def test_delete_provider(self):
        provider = ProviderFactory(**self.data)
        response = self.client.delete(f'/provider/{provider.pk}/')
        self.assertEqual(response.status_code, 204)

    def test_list_provider(self):
        response = self.client.get(f'/provider/')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        })

    def test_retrieve_provider(self):
        provider = ProviderFactory(**self.data)
        response = self.client.get(f'/provider/{provider.pk}/')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset(self.data, data)
