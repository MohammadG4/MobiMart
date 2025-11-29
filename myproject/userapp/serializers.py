from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

        extra_kwargs = {
            'password': {'write_only': True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
            "last_login": {"read_only": True},
            "date_joined": {"read_only": True},
        }

    def create(self, validated_data):
        # This ENSURES password is hashed
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user