
from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator
from posts.models import Post, PostImage

# code reference:
# JPG; https://stackoverflow.com/questions/48756249/django-rest-uploading-and-serializing-multiple-images
class PostImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostImage
        fields = ('post', 'image',)

class PostSerializer(serializers.HyperlinkedModelSerializer):
    # associate Post with user
    # see more: https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#updating-our-serializer
    author = serializers.ReadOnlyField(source='author.username')
    # associate Post with PostImage
    images = PostImageSerializer(source='postimage_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'images', 'origin_post', 'text_type', 'add_time', 'mod_time', 'visibility', 'unlist')

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        post = Post.objects.create(**validated_data)
        for image_data in images_data.values():
            PostImage.objects.create(post=post, image=image_data)
        return post

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.content = validated_data.get('content', instance.content)
        instance.origin_post = validated_data.get('origin_post', instance.origin_post)
        instance.text_type = validated_data.get('text_type', instance.text_type)
        instance.add_time = validated_data.get('add_time', instance.add_time)
        instance.mod_time = validated_data.get('mod_time', instance.mod_time)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.unlist = validated_data.get('unlist', instance.unlist)
        instance.save()

        return instance

class PostReadOnlySerializer(serializers.HyperlinkedModelSerializer):
    # associate Post with user
    # see more: https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#updating-our-serializer
    author = serializers.ReadOnlyField(source='author.username')
    # associate Post with PostImage
    images = PostImageSerializer(source='postimage_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'images', 'origin_post', 'text_type', 'add_time', 'mod_time', 'visibility', 'unlist')
        read_only_fields = ('author', 'content', 'images', 'origin_post', 'text_type', 'visibility', 'unlist')

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        post = Post.objects.create(**validated_data)
        for image_data in images_data.values():
            PostImage.objects.create(post=post, image=image_data)
        return post

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.content = validated_data.get('content', instance.content)
        instance.origin_post = validated_data.get('origin_post', instance.origin_post)
        instance.text_type = validated_data.get('text_type', instance.text_type)
        instance.add_time = validated_data.get('add_time', instance.add_time)
        instance.mod_time = validated_data.get('mod_time', instance.mod_time)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.unlist = validated_data.get('unlist', instance.unlist)
        instance.save()

        return instance