from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField
from api.models import Profile
from django.contrib.auth.models import User

class ProfileSerializer(ModelSerializer):

	
	username=PrimaryKeyRelatedField(queryset=User.objects.all())
	class Meta:
		model=Profile
		fields=(
			'id',
			'username',
			'bio',
			)
		read_only_fields=['id']