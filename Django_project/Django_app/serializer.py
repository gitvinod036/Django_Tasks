from rest_framework import serializers
from .models import UserDetails


class UserDetails_Serializers(serializers.ModelSerializer):
    class Meta:
        model=UserDetails
        fields="__all__"
