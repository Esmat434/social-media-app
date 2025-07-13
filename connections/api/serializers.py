from rest_framework import serializers

from django.contrib.auth import get_user_model

from connections.models import Connection

User = get_user_model()

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ('from_user', 'to_user')

    def validate(self, attrs):
        from_user = attrs.get('from_user')
        to_user = attrs.get('to_user')

        if not from_user or not to_user:
            raise serializers.ValidationError("Both users must be provided.")

        if Connection.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise serializers.ValidationError("This connection already exists.")

        return attrs

    def create(self, validated_data):
        return Connection.objects.create(**validated_data)
