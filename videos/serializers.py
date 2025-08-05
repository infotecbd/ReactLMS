from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.url:
            representation['url'] = self.context['request'].build_absolute_uri(instance.url.url)
        return representation