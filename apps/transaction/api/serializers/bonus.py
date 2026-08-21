from rest_framework import serializers


class BonusCheckQuerySerializer(serializers.Serializer):
    code = serializers.CharField(help_text="Printed bonus code, e.g. LEOB0001")


class BonusCheckResponseSerializer(serializers.Serializer):
    summa = serializers.IntegerField(help_text="Balance amount that will be credited")


class BonusRedeemSerializer(serializers.Serializer):
    code = serializers.CharField(help_text="Printed bonus code, e.g. LEOB0001")
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        help_text="Proof-of-purchase photos (upload multiple)",
    )


class BonusRedeemResponseSerializer(serializers.Serializer):
    balance = serializers.IntegerField(help_text="User's new total balance")
    awarded = serializers.IntegerField(help_text="Amount credited from this code")