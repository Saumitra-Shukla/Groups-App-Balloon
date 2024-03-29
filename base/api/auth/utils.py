from django.core import signing
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User, Group
from django.conf import settings as django_settings

from rest_framework.authtoken.models import Token

from api.models import Profile
from . import settings as auth_settings
import json,os,re



class AuthTools:
	password_salt=auth_settings.AUTH_PASSWORD_SALT
	token_age=auth_settings.AUTH_TOKEN_AGE


	@staticmethod
	def issue_user_token(user, salt):

		if user is not None:
			if salt == 'login':
				token,_=Token.objects.get_or_create(user=user)
			else:
				token=signing.dumps({'pk':user.pk},salt=salt)

			return token
		return None
	@staticmethod
	def get_user_from_token(token,salt):
		'''
		verify token for user
		'''
		try:
			value=signing.loads(token,salt=AuthTools.password_salt,max_age=900)
		except signing.SignatureExpired:
			return None
		except signing.BadSignature:
			return None

		user = User.objects.get(pk=value['pk'])

		if user is not None:
			return user
		return None

	@staticmethod
	def send_forgot_password_email(request,user,view):
		token=AuthTools.issue_user_token(user,AuthTools.password_salt)
		url=request.build_absolute_url(reverse(view,kwargs={'token':token}))

		context={
		'username':user.username,
		'email':user.email,
		'reset_password_url':url,

		}

	@staticmethod
	def authenticate(username,password):

		try:
			user=authenticate(username=username, password=password)
			if user is not None:
				return user
		except:
			pass

		return None

	@staticmethod
	def authenticate_email(email,password):

		if re.match(r'[^@]+@[^@]+\.[^@]+',email):
			user=AuthTools.get_user_by_email(email)
			if user is not None:
				return AuthTools.authenticate(user.username,password)
		else:
			return AuthTools.authenticate(email,password)
		return None

	@staticmethod
	def get_user_by_email(email):
		if email:
			try:
				user=User.objects.filter(email=email,is_active=True)[0]
				return user
			except:
				pass
		return None

	@staticmethod
	def get_user_by_username(username):
		try:
			user=User.objects.filter(username=username,is_active=True)[0]
			return user
		except:
			pass
		return None

	@staticmethod
	def login(request,user):

		if user is not None:
			try:
				login(request,user)
				return True
			except Exception as ex:
				template = "An exception of type {0} occured. Arguments:\n{1!r}"
				message = template.format(type(ex).__name__, ex.args)
		return False

	@staticmethod
	def logout(request):
		if request:
			try:
				Token.objects.filter(user=request.user).delete()
				logout(request)
				return True
			except :
				pass
		return False


	@staticmethod
	def set_password(user,password,new_password):
		if user.has_usable_password():
			if user.check_password(password) and password != new_password:
				user.set_password(new_password)
				user.save()
				return True
			elif new_password:
				user.set_password(new_password)
				user.save()
				return True
		return False

	@staticmethod
	def reset_password(token,new_password):
		user=AuthTools.get_user_from_token(token,AuthTools.password_salt)
		if user is not None:
			user.set_password(new_password)
			user.save()
			return user
		return None

	@staticmethod
	def validate_username(username):
		min_username_length=3
		stats='valid'
		if len(username)< min_username_length:
			stats='invalid'
		elif re.match("^[a-zA-Z0-9_-]+$", username) is None:
			stats = 'invalid'
		else:
			user = AuthTools.get_user_by_username(username)

			if user is not None:
				stats = 'taken'

		return stats

	@staticmethod
	def validate_email(email):
		status='valid'
		try:
			validate_email(email)
			user=AuthTools.get_user_by_email(email)
			if user is not None:
				status='taken'

		except:
			status='invalid'
		return status

	@staticmethod
	def validate_password(password):
		min_pass_len=7
		is_valid=True

		if len(password)<min_pass_len:
			is_valid = False

		return is_valid

	@staticmethod
	def register(user_data, profile_data, group):
		"""
		Register user:
			user_data = {'username', 'email', 'password'}
			profile_data = {'role', 'position'}
		"""

		user_data['email'] = user_data['email']
		user_data['username'] = user_data['username']

		try:
			#Determine if email already exists.
			user_exists = User.objects.filter(email=user_data['email'])
			if user_exists:
				return {
					'user': user_exists[0],
					'is_new': False
				}

			#Determine if username already exists.
			username_exists = User.objects.filter(username=user_data['username'])
			if username_exists:
				return {
					'user': username_exists[0],
					'is_new': False
				}

			user = User.objects.create_user(**user_data)

			profile_data['user'] = user
			profile = Profile(**profile_data)
			profile.save()

			group = Group.objects.get(name=group)
			group.user_set.add(user)

			return {
				'user': user,
				'is_new': True
			}
		except e:
			print (str(e))
			#raise Exception(e.message)

		return None

	
	@staticmethod
	def profile_register(user, profile_data):

		try:
			return profile.objects.get(pk=user.id)
		except ObjectDoesNotExist:
			try:
				profile_data['user']=user
				profile=Profile(**profile_data)
				profile.save()

				group=Group.objects.get(name=profile_data['role']+'_basic')

				group.user_set.add(user)
				return profile
			except:
				pass
		return None
















