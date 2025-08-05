from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Category, Course
from .serializers import CategorySerializer, CourseSerializer
from rest_framework import viewsets, permissions


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response({"success": "Logged in"})
    return Response({"error": "Invalid credentials"}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"success": "Logged out"})

@api_view(['GET'])
def check_auth(request):
    if request.user.is_authenticated:
        return Response({"username": request.user.username})
    return Response({"error": "Not authenticated"}, status=401)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def enrolled_courses(request):
    courses = Course.objects.filter(instructors=request.user)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def enrolled_courses(request):
    user = request.user
    print("Logged-in user:", user)

    # This works only if 'enrolled_users' exists on Course model
    courses = Course.objects.filter(enrolled_users=user)

    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)
