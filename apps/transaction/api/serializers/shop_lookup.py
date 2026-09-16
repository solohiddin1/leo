from rest_framework import serializers


class ShopLookupSerializer(serializers.Serializer):
    shop_id = serializers.IntegerField()


class ShopLookupResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    is_priority = serializers.BooleanField()
    bonus_boost_percentage = serializers.IntegerField()
