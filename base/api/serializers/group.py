from rest_framework.serializers  import ModelSerializer,PrimaryKeyRelatedField
from api.models import Groupps
from api.serializers.user import UserSerializer
from django.contrib.auth.models import User



class Grouppserializer(ModelSerializer):
	
	owner=UserSerializer(many=True,read_only=False)
	class Meta:
		model=Groupps
		fields=(
			'id',
			'owner',
			'name',
			)

		read_only_fields=('id',)

	def create(self, validated_data):

		return Item.objects.create(**validated_data)


class GroupDetailSerializer(ModelSerializer):
	'''
	Item Detail Serializer
	'''

	owner=UserSerializer(many=True,read_only=True)
	user=UserSerializer(many=True,read_only=True)
	
	class Meta:
		model=Groupps
		fields= (
			'id',
			'owner',
			'user',
			'name',
			'base_url',
			)
		read_only_fields=['id',]