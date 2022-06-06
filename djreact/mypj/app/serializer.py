from rest_framework import serializers
from .models import *

class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchImage
        fields = '__all__'