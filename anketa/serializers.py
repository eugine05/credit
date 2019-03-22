from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Organization,Partner,Offer,Anketa,Bid


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""
    class Meta:
        model = User
        fields = ("url", "username")

class PartnerSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализация партнера"""
    class Meta:
        model = Partner
        fields = ("url", "name")

class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализация кредитной организации"""
    class Meta:
        model = Organization
        fields = ("url", "name")

class AnketaSerializers(serializers.HyperlinkedModelSerializer):
    """Сериализация анкеты"""
    class Meta:
        model = Anketa
        fields = ("url", "name", "surname", "first_name", "Birthdate", "telefon", "pasport", "ball", "partner")

class AnketaPostSerializers(serializers.HyperlinkedModelSerializer):
    """Сериализация создания анкеты"""
    class Meta:
        model = Anketa
        fields = ("url", "name", "surname", "first_name", "Birthdate", "telefon", "pasport", "ball", "partner")

class AnketaUpdateSerializers(serializers.HyperlinkedModelSerializer):
    """Сериализация обновления анкеты"""
    class Meta:
        model = Anketa
        fields = ("url", "name", "surname", "first_name", "Birthdate", "telefon", "pasport", "ball", "partner")

class BidSerializers(serializers.HyperlinkedModelSerializer):
    """Сериализация заявок"""
    class Meta:
        model = Bid
        fields = ("url", "create", "sent", "status", "anketa", "offer")

class BidPostSerializers(serializers.HyperlinkedModelSerializer):
    """Сериализация создания заявки"""
    class Meta:
        model = Bid
        fields = ("url", "create", "sent", "status", "anketa", "offer")

    def create(self, validated_data):
        print(self.context['request'].user)
        print(validated_data['anketa'].id)
        if self.context['request'].user.is_staff==False:
            try:
                user = Anketa.objects.get(Q(partner__customer=self.context['request'].user) & Q(id=validated_data['anketa'].id))               
            except Anketa.DoesNotExist:
                raise serializers.ValidationError("У Вас нет такой анкеты")
        return Bid.objects.create(**validated_data)

class BidPostStatusSerializers(serializers.ModelSerializer):
    """Сериализация обновления статуса заявки"""
    class Meta:
        model = Bid
        fields = ("status",)

class OfferSerializers(serializers.HyperlinkedModelSerializer):
    """Сериализация предложений"""
    class Meta:
        model = Offer
        fields = ("url", "name", "create", "update", "start_rotation", "stop_rotation", "min_ball", "max_ball", "credit", 'status')