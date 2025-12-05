from rest_framework import serializers
from .models import DjangoAppUserdetails


class UserDetails_Serializers(serializers.ModelSerializer):
    class Meta:
        model=DjangoAppUserdetails
        fields="__all__"
