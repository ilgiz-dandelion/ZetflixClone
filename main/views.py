from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from main.serializers import *


class PermissionMixin:
    def get_permissions(self):
        if self.action in ['create','update', 'partial_update', 'destroy', 'favorites', 'favorite', ]:
            permissions = [IsAdminUser, ]
        elif self.action == ['filter','search', ] :
            permissions = [AllowAny, ]
        else:
            permissions = []
        return [permission() for permission in permissions]


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    queryset_any = Favorite.objects.all()

    @action(detail=False, methods=['get'])
    def filter(self, request, pk=None):
        queryset = self.get_queryset()
        start_date = timezone.now() - timedelta(days=1)
        queryset = queryset.filter(created_at__gte=start_date)
        serializer = MovieSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(description__icontains=q))
        serializer = MovieSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def favorites(self, request):
        queryset = Favorite.objects.all()
        queryset = queryset.filter(user=request.user)
        serializer = FavoriteSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        post = self.get_object()
        obj, created = Favorite.objects.get_or_create(user=request.user, post=post, )
        if not created:
            obj.favorite = not obj.favorite
            obj.save()
        favorites = 'added to favorites' if obj.favorite else 'removed to favorites'

        return Response('Successfully {} !'.format(favorites), status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class MovieImagesViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class CommentViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikesViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer


class RatingViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer



