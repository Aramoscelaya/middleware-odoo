from rest_framework import serializers
from .models import original_message

class original_messageSerializer(serializers.ModelSerializer):
    class Meta:
        model = original_message
        fields = ('id', 'file', 'entity', 'status', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at',)
        

class original_messageParameterSerializer(serializers.Serializer):
    parameters = serializers.JSONField()