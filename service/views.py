from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from service.models import Post, Comments, User
from service.serializer import PostSerializers, CommentsSerializers, UserSerializers
from service.permissions import PermissionPolicyMixin


class UserViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes_per_method = {
        'list': [IsAdminUser, IsAuthenticated],
        'create': [AllowAny],
        'update': [IsAdminUser, IsAuthenticated],
        'destroy': [IsAdminUser],
        'retrieve': [IsAdminUser]
    }


class CommentsViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializers
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser, IsAuthenticated],
        'retrieve': [IsAdminUser, IsAuthenticated]
    }


class PostViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAdminUser, IsAuthenticated],
        'destroy': [IsAdminUser, IsAuthenticated],
        'retrieve': [IsAdminUser]
    }

