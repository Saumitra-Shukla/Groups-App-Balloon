from django.conf import settings
from rest_framework import status,generics,mixins
from rest_framework.response import Response
from api.models import Asset, AssetBundle, Item
from api import settings as api_settings
from api.generics import generics
#from base.tasks import resize_and_upload
import json,string,random,os
from PIL import Image
from io import BytesIO
import base64,boto3,PIL
from api.serializers.item import ItemDetailSerializer
from api.auth.serializers import UploadSerializer

class UploadImage(generics.CreateAPIView):

	queryset = Asset.objects.all()
	serializer_class = UploadSerializer

	def post(self,request):
		data = json.dumps(request.data)
		data = json.loads(data)


		if not 'image' in data:
			return Response({'error': 'no image in request.'}, status=status.HTTP_400_BAD_REQUEST)
		if not 'mime' in data:
			return Response({'error': 'no mime in request.'}, status=status.HTTP_400_BAD_REQUEST)

		mime=data['mime']
		if not mime in ['image/jpeg','image/png','image/gif','image/jpg']:
			return Response({'error':'mime not accepted'},status=status.HTTP_400_BAD_REQUEST)
		ext=mime[6:]
		salt=''.join(random.choice(string.ascii_uppercase+ string.digits)
				for _ in range(16))
		#data['image']=data['image']
		image_string=data['image']
		#image_string=image_string.replace('data:%s;base64,'% mime, '')

		# fh = open("public/static/admin/img/imageToSave.%s" % ext, "wb")
		# fh.write(base64.b64decode(image_string))
		# fh.close()

		from firebase import Firebase

		config = {
			'apiKey': "AIzaSyD7yT4lfcGx09w0WebnCMsGoNOW31dQm08",
			'authDomain': "group-proj-c8dd5.firebaseapp.com",
			'databaseURL': "https://group-proj-c8dd5.firebaseio.com",
			'projectId': "group-proj-c8dd5",
			'storageBucket': "group-proj-c8dd5.appspot.com",
			'messagingSenderId': "424365456354",
			'appId': "1:424365456354:web:27821c94665e5233"

		}
		

		firebase = Firebase(config)
		# storage=firebase.storage()
		# storage.child("storage/%s.%s"%(salt,ext)).put('public/static/admin/img/imageToSave.%s' % ext)


		asset_bundle=AssetBundle()
		asset_bundle.salt=salt
		asset_bundle.kind='image'
		#asset_bundle.base_url=storage.child("storage/%s.%s"%(salt,ext)).get_url(None)
		print(asset_bundle.base_url)
		asset_bundle.owner=request.user
		asset_bundle.save()

		


		for k in Asset.KIND_CHOICES:
			kind=k[0]

			asset=Asset()
			asset.asset_bundle=asset_bundle
			asset.kind=kind
			asset.extension=salt
			asset.processing=True
			asset.save()
			img = Image.open(BytesIO(base64.b64decode(image_string)))
			print(img)
			aspect = img.width / img.height

			width = 0
			height = 0
			resized_img = None
			if kind == 'original':
				print ("ORIGINAL")
				width = img.width
				height = img.height
				resized_img = img.resize((width, height), PIL.Image.ANTIALIAS)

			elif kind == 'large':
				print ("LARGE")
				width = 1024
				height = aspect * 1024
				resized_img = img.resize((int(width), int(height)), PIL.Image.ANTIALIAS)

			
			elif kind == 'small':
				print ("SMALL")
				width = 128
				height = aspect * 128
				resized_img = img.resize((int(width),int( height)), PIL.Image.ANTIALIAS)

			else:
				print ("ERROR - size not handled.")

			fh = open("public/static/admin/img/imageToSave.%s" % ext, "wb")
			fh.write(base64.b64decode(image_string))
			fh.close()	
			
			storage=firebase.storage()

			storage.child("storage/%s-%s.%s"%(salt,kind,ext)).put("public/static/admin/img/imageToSave.%s" % ext)
			asset.base_url=storage.child("storage/%s-%s.%s"%(salt,kind,ext)).get_url(None)
			#asset = Asset.objects.get(pk=asset_id)
			asset.width = width
			asset.height = height
			asset.processing = False
			asset.save()




		item = Item()
		item.asset__bundle=asset_bundle
		item.owner=request.user
		item.save()

		serializer=ItemDetailSerializer(item)
		return Response(serializer.data, status=status.HTTP_200_OK)

