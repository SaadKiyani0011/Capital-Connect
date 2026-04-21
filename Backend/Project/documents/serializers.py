from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ('owner', 'file_size_bytes', 'file_type', 'uploaded_at', 'last_modified')
        
    def create(self, validated_data):
        file = validated_data.get('file')
        if file:
            validated_data['file_size_bytes'] = file.size
            validated_data['file_type'] = file.content_type
            
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
        
    def update(self, instance, validated_data):
        file = validated_data.get('file')
        if file:
            validated_data['file_size_bytes'] = file.size
            validated_data['file_type'] = file.content_type
            instance.version += 1 # Auto-increment version on file update
            
        return super().update(instance, validated_data)
