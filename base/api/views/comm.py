from rest_framework import status,generics,mixins
from rest_framework.response import Response
from api.models import Comment,Like
from api.serializers.comm import CommentSerializer,LikeSerializer



class CommentList(generics.ListCreateAPIView):
	queryset=Comment.objects.all()
	serializer_class=CommentSerializer

	def list(self,request):
		self.serializer_class=CommentSerializer
		return super(CommentList,self).list(request)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):

	queryset=Comment.objects.all()
	serializer_class=CommentSerializer 

	def retrieve(self,request,pk):
		queryset=self.get_object()
		serializer=CommentSerializer(queryset,many=False)
		return Response(serializer.data)

class LikeList(generics.ListCreateAPIView):
	queryset=Like.objects.all()
	serializer_class=LikeSerializer

	def list(self,request):
		self.serializer_class=LikeSerializer
		return super(LikeList,self).list(request)

class LikeDetail(generics.RetrieveUpdateDestroyAPIView):

	queryset=Like.objects.all()
	serializer_class=LikeSerializer 

	def retrieve(self,request,pk):
		queryset=self.get_object()
		serializer=LikeSerializer(queryset,many=False)
		return Response(serializer.data)