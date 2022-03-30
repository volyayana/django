from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, AdvertisementStatusChoices, AdvertisementFavourite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        method = self.context['request'].stream.method
        status = data.get('status')
        if ((status is None or status == AdvertisementStatusChoices.OPEN) and method == 'POST') \
                or (status == AdvertisementStatusChoices.OPEN and method == 'PATCH'):
            adv_count = Advertisement.objects.filter(creator=self.context['request'].user,
                                                     status=AdvertisementStatusChoices.OPEN).count()
            if adv_count == 10:
                raise ValidationError('Пользователь может иметь не более 10 открытых объявлений')
        return data


class AdvertisementFavouriteSerializer(serializers.ModelSerializer):
    """Serializer для избранных объявлений."""

    user = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = AdvertisementFavourite
        fields = ('id', 'advertisement', 'user')

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является тем, кто добавляет объявления в избранное,
        # изменить или переопределить его через API нельзя.
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        if data.get('advertisement').creator == self.context["request"].user:
            raise ValidationError('Пользователь не может добавлять в избранное свои объявления')
        return data