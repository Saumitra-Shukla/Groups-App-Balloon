from django.conf import settings
from rest_framework import status,generics,mixins
from rest_framework.response import Response
from api.models import AssetBundle,Asset
from api.serializers.assetbundle import AssetBundleSerializer,AssetSerializer
from api import settings as api_settings


class AssetBundleList(generics.ListCreateAPIView):
	queryset=AssetBundle.objects.all()
	serializer_class=AssetBundleSerializer
	permission_classes=api_settings.CONSUMER_PERMISSIONS
	def list(self,request):
		self.serializer_class=AssetBundleSerializer
		return super(AssetBundleList,self).list(request)

class AssetBundleDetail(generics.RetrieveUpdateDestroyAPIView):

	queryset=AssetBundle.objects.all()
	serializer_class=AssetBundleSerializer 
	permission_classes=api_settings.CONSUMER_PERMISSIONS
	def retrieve(self,request,pk):
		queryset=self.get_object()
		serializer=AssetBundleSerializer(queryset,many=False)
		return Response(serializer.data)

class AssetList(generics.ListCreateAPIView):
	queryset=Asset.objects.all()
	serializer_class=AssetSerializer

	def list(self,request):
		self.serializer_class=AssetSerializer
		return super(AssetList,self).list(request)

class AssetDetail(generics.RetrieveUpdateDestroyAPIView):

	queryset=Asset.objects.all()
	serializer_class=AssetSerializer 

	def retrieve(self,request,pk):
		queryset=self.get_object()
		serializer=AssetSerializer(queryset,many=False)
		return Response(serializer.data)