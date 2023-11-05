from rest_framework import serializers
from apps.account.models import Account

class LoginEUSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'



class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)


