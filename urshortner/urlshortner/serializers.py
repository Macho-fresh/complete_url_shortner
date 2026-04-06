from .models import Url
from rest_framework import serializers

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ['longurl']
