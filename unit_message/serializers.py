from rest_framework import serializers
from .models import unit_message

class unit_messageSerializer(serializers.ModelSerializer):
    class Meta:
        model = unit_message
        fields = ('id', 'message', 'entity', 'status', 'active', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at',)
        

class unit_messageParameterSerializer(serializers.Serializer):
    parameters = serializers.JSONField()