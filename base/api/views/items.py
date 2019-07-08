from django.conf import settings
from rest_framework import status,generics,mixins
from rest_framework.response import Response
from api.models import Item
from api.serializers.item import ItemSerializer,ItemDetailSerializer
from api import settings as api_settings



class ItemList(generics.ListCreateAPIView):
	'''
	Item : Create, List
	'''
	queryset=Item.objects.all()
	serializer_class=ItemSerializer
	permission_classes=api_settings.CONSUMER_PERMISSIONS

	def list(self,request):
		self.serializer_class= ItemSerializer
		return super(ItemList,self).list(request)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
	'''
	Location : Read, Write, Delete
	'''

	queryset=Item.objects.all()
	serializer_class=ItemDetailSerializer 

	def retrieve(self,request,pk):
		queryset=self.get_object()
		serializer=ItemDetailSerializer(queryset,many=False)
		return Response(serializer.data)