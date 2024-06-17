
from rest_framework import serializers


class AsinSerializer(serializers.Serializer):
    asin = serializers.ListField(
        child=serializers.CharField(max_length=15),
        allow_empty=False
    )
    pincode = serializers.CharField(max_length=10,required=False)
    city_name = serializers.CharField(max_length=20,required=False)


