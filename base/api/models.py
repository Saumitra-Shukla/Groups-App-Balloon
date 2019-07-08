from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Profile(models.Model):


	ROLE=(('consumer','Consumer'),('staff','Staff'))
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	bio=models.TextField(blank=True,null=True)
	role=models.CharField(max_length=100,choices=ROLE,default='consumer')

	def __str__(self):
		return self.user.username

class AssetBundle(models.Model):
	
	#--------
	#collection of images
	#--------

	KIND_CHOICES=(('image','Image'),('video','Video'),)

	salt=models.CharField(max_length=16)
	kind=models.CharField(max_length=8,choices=KIND_CHOICES)
	base_url=models.CharField(max_length=255,default=None,blank=True,null=True)

	owner=models.ForeignKey(User, on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)

	def __str__(self):
		return "AssetBundle : %s" % self.salt


class Asset(models.Model):



	asset_bundle=models.ForeignKey(AssetBundle,on_delete=models.CASCADE)
	KIND_CHOICES=(('original','Original'),('large','Large'),('small','Small'),)
	kind=models.CharField(max_length=8,choices=KIND_CHOICES,default='original')
	width=models.IntegerField(default=0)
	height=models.IntegerField(default=0)
	EXTENSION_CHOICES=(('png','PNG'),('gif','GIF'),('jpg','JPG'),('jpeg','JPEG'),)
	extension=models.CharField(max_length=4,choices=EXTENSION_CHOICES)
	base_url=models.CharField(max_length=255,default=None,blank=True,null=True)
	def __unicode__(self):
		return "Asset: %s : %s" % (self.asset_bundle.salt,self.kind)
	
	
	@property
	def owner(self):
		return self.asset_bundle.owner.username

	@property
	def full_detail(self):
		s=self.asset_bundle.kind+'/'+self.kind+'/'+self.asset_bundle.salt+'.'+self.extension

		return s

	# @property
	# def full_url(self):
	# 	s=self.asset_bundle.base_url+'/'+self.asset_bundle.kind+'/'+self.kind+'/'+self.asset_bundle.salt+'.'+self.extension

	# 	return s




class Item(models.Model):
	'''
	this is model for items
	'''
	# title=models.CharField(max_length=255)
	# subtitle=models.TextField(max_length=600,blank=True,null=True)
	# like_count=models.IntegerField(default=0)

	asset_bundle=models.ForeignKey(AssetBundle, on_delete=models.CASCADE, blank=True,null=True)

	details=models.TextField(max_length=600,blank=True,null=True)
	owner=models.ForeignKey(User, on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "Item : %s : %s" %(self.owner.username, self.asset_bundle)


	@property
	def name(self):
		return self.asset_bundle.salt


class Comment(models.Model):
	
	item=models.ForeignKey(Item, on_delete=models.CASCADE)
	body=models.TextField()
	owner=models.ForeignKey(User, on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)



class Like(models.Model):
	
	item=models.ForeignKey(Item, on_delete=models.CASCADE)
	owner=models.ForeignKey(User, on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)

class Groupps(models.Model):
	owner=models.ManyToManyField(User,related_name='ownergroup')
	users=models.ManyToManyField(User,related_name='usergroup')
	name=models.CharField(max_length=255,default=None,blank=True,null=True)
	base_url=models.CharField(max_length=255,default=None,blank=True,null=True)