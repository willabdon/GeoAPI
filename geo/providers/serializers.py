from rest_framework import serializers

from .models import Provider


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ('pk', 'name', 'email', 'phone', 'language', 'currency')
