from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer

from courses.serializers import CourseSerializer
from .models import Course





@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # or AllowAny if public
def video_list(request):
    if request.method == 'GET':
        videos = Video.objects.all().order_by('-created_at')
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def enrolled_courses(request):
    user = request.user
    print('Logged in as:', user)

    # Make sure this matches your actual field name
    courses = Course.objects.filter(enrolled_users=user)

    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)
