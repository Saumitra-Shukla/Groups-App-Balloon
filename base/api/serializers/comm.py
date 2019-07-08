from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField
from api.models import Comment,Like,Item
from api.serializers.user import UserSerializer
from api.serializers.item import ItemDetailSerializer
from django.contrib.auth.models import User

class CommentSerializer(ModelSerializer):

	owner=UserSerializer(many=False,read_only=False)
	item=PrimaryKeyRelatedField(queryset=Item.objects.all())
	class Meta:
		model=Comment
		fields=(
			'id',
			'item',
			'owner',
			'body',
			'created_at',
			'updated_at',
			)
		read_only_fields=['id']


class LikeSerializer(ModelSerializer):

	owner=UserSerializer(many=False,read_only=False)
	item=PrimaryKeyRelatedField(queryset=Item.objects.all())
	class Meta:
		model=Like
		fields=(
			'id',
			'item',
			'owner',
			'created_at',
			'updated_at',
			)
		read_only_fields=['id']