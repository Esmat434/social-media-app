from rest_framework import serializers

from django.contrib.auth import get_user_model

from connections.models import Connection

User = get_user_model()

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ('to_user',)
        extra_kwargs = {
            'to_user':{'write_only': True}
        }

    def validate(self, attrs):
        from_user = self.context['request'].user
        to_user = attrs.get('to_user')

        if from_user == to_user:
            raise serializers.ValidationError("You cannot follow yourself.")

        if Connection.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise serializers.ValidationError("This connection already exists.")

        return attrs
