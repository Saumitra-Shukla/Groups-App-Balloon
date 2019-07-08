'''
api.auth.urls
'''
from django.urls import re_path
from api.auth import views

urlpatterns=[
	re_path(r'^me/?$',views.UserView.as_view(),name='views'),
	#re_path(r'^me/profile/?$',views.ProfileView.as_view(),name='profile'),
	re_path(r'^login/?$',views.LogInView.as_view(), name='login'),
	re_path(r'^logout/?$',views.LogoutView.as_view(), name='logout'),
	re_path(r'^register/?$',views.RegisterView.as_view(),name='register'),


]