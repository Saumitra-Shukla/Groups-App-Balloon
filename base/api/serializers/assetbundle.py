from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField
from api.models import AssetBundle, Asset
from api.serializers.user import UserSerializer
from django.contrib.auth.models import User

class AssetBundleSerializer(ModelSerializer):

	owner=UserSerializer(many=False,read_only=False)

	class Meta:
		model=AssetBundle
		fields=(
			'id',
			'salt',
			'kind',
			'base_url',
			'owner',
			'created_at',
			'updated_at',
			)
		read_only_fields=['id']
		def create(self, validated_data):

			return Item.objects.create(**validated_data)


class AssetSerializer(ModelSerializer):

	asset_bundle=AssetBundleSerializer(many=False, read_only=True)

	class Meta:
		model=Asset
		fields=(
			'id',
			'kind',
			'width',
			'height',
			'extension',
			'asset_bundle',
			)
		read_only_fields=['id']