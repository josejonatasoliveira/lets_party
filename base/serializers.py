from rest_framework import serializers
from .models import TopicCategory, TopicType, ResourceBase

class TopicCategorySerializer(serializers.Serializer):
    identifier = serializers.CharField()
    description = serializers.CharField()
    fa_class = serializers.CharField()
    created_at = serializers.DateTimeField()
    update_at = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    
    def create(self, validated_data):
        return TopicCategory(**validated_data)
    

class TopicTypeSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    description = serializers.CharField()
    fa_class = serializers.CharField()
    created_at = serializers.DateTimeField()
    update_at = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    
    def create(self, validated_data):
        return TopicType(**validated_data)
    
class ResourceBaseSerializer(serializers.Serializer):
    category = TopicCategorySerializer()
    type_event = TopicTypeSerializer()