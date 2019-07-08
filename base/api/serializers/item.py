from rest_framework.serializers  import ModelSerializer,PrimaryKeyRelatedField
from api.models import Item
from api.serializers.user import UserSerializer
from django.contrib.auth.models import User



class ItemSerializer(ModelSerializer):
	
	owner=UserSerializer(many=False,read_only=False)
	class Meta:
		model=Item
		fields=(
			'id',
			'asset_bundle',
			'owner',
			'created_at',
			'details',
			)

		read_only_fields=('id',)

	def create(self, validated_data):

		return Item.objects.create(**validated_data)


class ItemDetailSerializer(ModelSerializer):
	'''
	Item Detail Serializer
	'''

	owner=UserSerializer(many=False,read_only=True)
	
	class Meta:
		model=Item
		fields= (
			'id',
			'asset_bundle',
			'owner',
			'created_at',
			'updated_at',
			'name',
			'details',
			)
		read_only_fields=['id',]