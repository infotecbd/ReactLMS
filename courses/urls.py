from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    CourseViewSet,
    enrolled_courses,
    login_view,
    logout_view,
    check_auth
)

# Set up router
router = DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('courses', CourseViewSet)

# Combine path-based and router-based URLs
urlpatterns = [
    # Auth endpoints
    path('auth/login/', login_view),
    path('auth/logout/', logout_view),
    path('auth/check/', check_auth),

    # Enrolled courses
    path('courses/enrolled/', enrolled_courses),

    # Router endpoints
    path('', include(router.urls)),
]
