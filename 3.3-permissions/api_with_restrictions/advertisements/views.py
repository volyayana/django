from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, AdvertisementFavourite
from advertisements.permissions import IsObjectOwner
from advertisements.serializers import AdvertisementSerializer, AdvertisementFavouriteSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated(), IsObjectOwner()]
        return []

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Advertisement.objects.filter(~Q(status='DRAFT'))
        return Advertisement.objects.all().exclude(~Q(creator=self.request.user) & Q(status='DRAFT'))


class AdvertisementFavouriteViewSet(ModelViewSet):
    """ViewSet для избранных объявлений."""
    queryset = AdvertisementFavourite.objects.all()
    serializer_class = AdvertisementFavouriteSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return AdvertisementFavourite.objects.none()
        return AdvertisementFavourite.objects.filter(Q(user=self.request.user))

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated(), IsObjectOwner()]
        return []