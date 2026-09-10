from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ComicViewSet, ComicPageViewSet,
    CommentViewSet, LikeViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'comics', ComicViewSet)
router.register(r'pages', ComicPageViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
