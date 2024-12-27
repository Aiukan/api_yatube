"""Сериализаторы для API проекта."""

from rest_framework import serializers

from posts.models import Post, Group, Comment


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для класса Post."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Мета-информация сериализатора для класса Post."""

        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')
        read_only_fields = ('id', 'pub_date', 'author')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для класса Group."""

    class Meta:
        """Мета-информация сериализатора для класса Group."""

        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для класса Comment."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Мета-информация сериализатора для класса Comment."""

        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('id', 'created', 'author', 'post')
