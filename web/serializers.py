from rest_framework import serializers
from . import models


class UserProfileSerializer(serializers.Serializer):
    class Meta:
        model = models.Customer
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = models.Customer(
                email=validated_data['email'],
                name=validated_data['name']
            )

            user.set_password(validated_data['password'])
            user.save()
            return user