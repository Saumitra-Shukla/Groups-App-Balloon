from django.contrib.auth import get_user_model
from django.conf import settings as dj_settings
from rest_framework import generics, status
from rest_framework.response import Response
from api.auth.utils import AuthTools
from api import settings as api_settings
from api import generics
from api.auth import serializers
from api.serializers.user import UserSerializer
from api.serializers.profile import ProfileSerializer
from api.auth.serializers import LoginSerializer,LogoutSerializer,LoginCompleteSerializer
from api.models import Profile
import re



User= get_user_model()

class UserView(generics.RetrieveUpdateAPIView):
	'''
	User View
	'''

	model=User
	serializer_class=UserSerializer
	permission_classes=api_settings.CONSUMER_PERMISSIONS

	def get_object(self,*args, **kwargs):
		return self.request.user

class ProfileView(generics.RetrieveUpdateAPIView):
	'''
	Profile View
	'''


	model=Profile
	serializer_class=ProfileSerializer
	permission_classes=api_settings.CONSUMER_PERMISSIONS

	def get_object(self,*args, **kwargs):
		return self.request.user.profile

class LogInView(generics.GenericAPIView):
    """
    Login View
    """

    permission_classes = api_settings.UNPROTECTED
    serializer_class = LoginSerializer

    def post(self, request):
        if 'email' in request.data and 'password' in request.data:

            email = request.data['email'].lower()
            password = request.data['password']

            user = AuthTools.authenticate_email(email, password)

            if user is not None and AuthTools.login(request, user):
                token = AuthTools.issue_user_token(user, 'login')
                serializer = serializers.LoginCompleteSerializer(token)
                return Response(serializer.data)

        print(request.data)
        message = {'message': 'Unable to login with the credentials provided.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.GenericAPIView):
	permission_classes=api_settings.CONSUMER_PERMISSIONS
	serializer_class=LogoutSerializer

	def post(self,request):
		if AuthTools.logout(request):
			return Response(status.HTTP_200_OK)
		return Response(status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
	serializer_class=serializers.UserRegisterSerializer
	permission_classes=api_settings.UNPROTECTED

	def perform_create(self, serializer):
		instance=serializer.save()




