from rest_framework import serializers
from .models import CustomUser, Comic, ComicPage, Comment, Like


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role']
        read_only_fields = ['id']

    def validate_role(self, value):
        if value not in {'creator', 'audience'}:
            raise serializers.ValidationError('Role must be either creator or audience.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        return CustomUser.objects.create_user(password=password, **validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'avatar', 'role']


class ComicPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicPage
        fields = ['id', 'comic', 'image', 'page_number']

class ComicSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    pages = ComicPageSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Comic
        fields = [
            'id', 'title', 'description', 'author', 'genre',
            'cover_image', 'created_at', 'pages',
            'likes_count', 'comments_count'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comic', 'user', 'text', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'comic', 'user', 'created_at']
