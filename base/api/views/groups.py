from django.conf import settings
from rest_framework import status,generics,mixins
from rest_framework.response import Response
from api.models import Groupps
from api.serializers.group import Grouppserializer,GroupDetailSerializer
from api import settings as api_settings



class GroupList(generics.ListCreateAPIView):
	'''
	Item : Create, List
	'''
	queryset=Groupps.objects.all()
	serializer_class=Grouppserializer
	permission_classes=api_settings.CONSUMER_PERMISSIONS

	def list(self,request):
		self.serializer_class= Grouppserializer
		return super(GroupList,self).list(request)


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
	'''
	Location : Read, Write, Delete
	'''

	queryset=Groupps.objects.all()
	serializer_class=GroupDetailSerializer 

	def retrieve(self,request,pk):
		queryset=self.get_object()
		serializer=GroupDetailSerializer(queryset,many=False)
		return Response(serializer.data)