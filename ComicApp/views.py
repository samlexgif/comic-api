from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, Comic, ComicPage, Comment, Like
from .serializers import (
    CommentSerializer,
    ComicPageSerializer,
    ComicSerializer,
    LikeSerializer,
    RegisterSerializer,
    UserSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_health(request):
    return Response({
        'status': 'ok',
        'message': 'ComicVerse API is working',
        'app': 'ComicApp',
    }, status=200)


def home(request):
    return HttpResponse(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>ComicVerse API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; background: #0f172a; color: #f8fafc; }
                .container { max-width: 900px; margin: 0 auto; padding: 80px 24px; }
                .card { background: #111827; border-radius: 18px; padding: 32px; box-shadow: 0 12px 30px rgba(0,0,0,0.25); }
                h1 { font-size: 2.7rem; margin-bottom: 10px; }
                p { color: #dbeafe; line-height: 1.7; }
                .tags { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 24px; }
                .tag { background: #1d4ed8; border-radius: 999px; padding: 10px 16px; }
                a { color: #93c5fd; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="card">
                    <h1>ComicVerse API</h1>
                    <p>API is working.</p>
                    <p>Discover comics, support creators, and upload original stories to the community.</p>
                    <div class="tags">
                        <span class="tag">Creators</span>
                        <span class="tag">Audience</span>
                        <span class="tag">Comic Pages</span>
                        <span class="tag">API</span>
                    </div>
                    <p>Browse the API at <a href="/api/">/api/</a> and use the upload feature for creator accounts.</p>
                </div>
            </div>
        </body>
        </html>
        """,
        content_type='text/html',
    )

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ComicViewSet(viewsets.ModelViewSet):
    queryset = Comic.objects.all().order_by('-created_at')
    serializer_class = ComicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['post'], url_path='upload', permission_classes=[permissions.IsAuthenticated])
    def upload(self, request):
        if request.user.role != 'creator':
            return Response(
                {'detail': 'Only creators can upload comics.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        title = request.data.get('title')
        description = request.data.get('description', '')
        genre = request.data.get('genre')
        cover_image = request.FILES.get('cover_image')
        pages = request.FILES.getlist('pages')

        if not title or not genre:
            return Response(
                {'detail': 'title and genre are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comic = Comic.objects.create(
            title=title,
            description=description,
            author=request.user,
            genre=genre,
            cover_image=cover_image,
        )

        for page_number, page_file in enumerate(pages, start=1):
            ComicPage.objects.create(
                comic=comic,
                image=page_file,
                page_number=page_number,
            )

        serializer = self.get_serializer(comic)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        comic = self.get_object()
        Like.objects.get_or_create(comic=comic, user=request.user)
        return Response({'status': 'comic liked'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        comic = self.get_object()
        Like.objects.filter(comic=comic, user=request.user).delete()
        return Response({'status': 'comic unliked'})

# -------------------------------
# 📄 ComicPage ViewSet (Optional)
# -------------------------------
class ComicPageViewSet(viewsets.ModelViewSet):
    queryset = ComicPage.objects.all()
    serializer_class = ComicPageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# -------------------------------
# 💬 Comment ViewSet
# -------------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# -------------------------------
# ❤️ Like ViewSet (Read-only)
# -------------------------------
class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    
   
