from django.db.models import Avg
from rest_framework import serializers

from .models import *


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ['movie', ]

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class MovieSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Movie
        exclude = ('author', )

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        author = request.user
        movie = Movie.objects.create(author=author, **validated_data)
        for image in images_data.getlist('images'):
            Image.objects.create(image=image, movie=movie)
        return movie

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        images_data = request.FILES
        instance.images.all().delete()
        for image in images_data.getlist('images'):
            Image.objects.create(image=image, movie=instance)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['images'] = ImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['likes'] = instance.likes.all().count()
        representation['rating'] = instance.rating.aggregate(Avg('rating'))
        return representation


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        comment = Comment.objects.create(author=author, **validated_data)
        return comment


class LikesSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Likes
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        movie = validated_data.get('movie')
        like = Likes.objects.get_or_create(author=author, movie=movie)[0]
        like.likes = True if like.likes is False else False
        like.save()
        return like


class RatingSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        movie = validated_data.get('movie')
        rating = Rating.objects.get_or_create(user=user, movie=movie)[0]
        rating.rating = validated_data['rating']
        rating.save()
        return rating


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['movie'] = instance.movie.title
        return representation


class ParsingSerializer(serializers.Serializer):
    movie_title = serializers.CharField(max_length=255)
    year = serializers.CharField(max_length=255)
    place = serializers.CharField(max_length=255)
    star_cast = serializers.CharField(max_length=1000)
    rating = serializers.CharField(max_length=255)
    vote = serializers.CharField(max_length=255)
    link = serializers.CharField(max_length=255)