"""Представления для API проекта."""

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Переопределение метода perform_create для PostViewSet.

        Автоматическое добавление автора поста.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Переопределение метода perform_update для PostViewSet.

        Накладывает ограничения на редактирование
        значений сторонними пользователями.
        """
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Переопределение метода perform_destroy для PostViewSet.

        Накладывает ограничения на удаление значений сторонними пользователями.
        """
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Comment."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Переопределение метода get_queryset для CommentViewSet.

        Извлекает информацию о посте из аргументов
        и возвращает связанные комментарии.
        """
        post = Post.objects.get(pk=self.kwargs['post_id'])
        return self.queryset.filter(post=post)

    def perform_create(self, serializer):
        """Переопределение метода perform_create для PostViewSet.

        Автоматическое добавление номера поста и автора поста к комментарию.
        """
        post = Post.objects.get(pk=self.kwargs['post_id'])
        serializer.save(
            author=self.request.user,
            post=post
        )

    def perform_update(self, serializer):
        """Переопределение метода perform_update для CommentViewSet.

        Накладывает ограничения на редактирование
        значений сторонними пользователями.
        """
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Переопределение метода perform_destroy для CommentViewSet.

        Накладывает ограничения на удаление значений сторонними пользователями.
        """
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super().perform_destroy(instance)
