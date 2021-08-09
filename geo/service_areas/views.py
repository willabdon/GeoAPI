from django.db.models import query
from django.utils.decorators import method_decorator
from rest_framework import viewsets

from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError

from .serializers import ServiceAreaSerializer, ServiceAreaSerializerRepresentation
from .models import ServiceArea


@method_decorator(name='list', decorator=swagger_auto_schema(
    responses={200: ServiceAreaSerializerRepresentation(many=True)}
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    responses={200: ServiceAreaSerializerRepresentation()}
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    responses={200: ServiceAreaSerializerRepresentation()}
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    responses={200: ServiceAreaSerializerRepresentation()}
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    responses={200: ServiceAreaSerializerRepresentation()}
))
class ServiceAreaViewSet(viewsets.ModelViewSet):

    serializer_class = ServiceAreaSerializer
    queryset = ServiceArea.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        coordinates = self.request.query_params.get('coordinates', None)

        if coordinates is not None:
            split = coordinates.split(',')
            data = [float(coord) for coord in split]

            if len(data) != 2:
                raise ValidationError(
                    'Coordinates must have latitude and longitude.')

            point = f"POINT({' '.join(map(str, data))})"

            queryset = queryset.filter(coordinates__contains=point)

        return queryset
