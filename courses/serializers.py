from rest_framework import serializers
from .models import Category, Course
from django.contrib.auth.models import User
from videos.serializers import VideoSerializer



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    instructors = InstructorSerializer(many=True, read_only=True)
    instructor_ids = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, write_only=True, source='instructors')
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'