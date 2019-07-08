from django.urls import include, re_path
from django.views.decorators.csrf import csrf_exempt

from api.views.items import ItemList,ItemDetail
from api.views.groups import GroupList,GroupDetail
from api.views.assetbundle import AssetBundleList,AssetBundleDetail,AssetList,AssetDetail
from api.views.comm import CommentList,CommentDetail,LikeList,LikeDetail
from api.auth import urls as auth_urls
from api.views.upload import UploadImage



urlpatterns=[

	re_path(r'^auth/',include(auth_urls)),
	re_path(r'^items/?$',ItemList.as_view(),name='item-list'),
	re_path(r'^items/(?P<pk>[0-9]+)/?$',ItemDetail.as_view(),name='item-detail'),
	re_path(r'^Groups/?$',GroupList.as_view(),name='group-list'),
	re_path(r'^Groups/(?P<pk>[0-9]+)/?$',GroupDetail.as_view(),name='group-detail'),
	re_path(r'^assetbundle/?$',AssetBundleList.as_view(),name='assetbundle-list'),
	re_path(r'^assetbundle/(?P<pk>[0-9]+)/?$',AssetBundleDetail.as_view(),name='assetbundle-detail'),
	re_path(r'^assets/?$',AssetList.as_view(),name='asset-list'),
	re_path(r'^assets/(?P<pk>[0-9]+)/?$',AssetDetail.as_view(),name='asset-detail'),
	re_path(r'^comment/?$',CommentList.as_view(),name='comment-list'),
	re_path(r'^comment/(?P<pk>[0-9]+)/?$',CommentDetail.as_view(),name='comment-detail'),
	re_path(r'^like/?$',LikeList.as_view(),name='like-list'),
	re_path(r'^like/(?P<pk>[0-9]+)/?$',LikeDetail.as_view(),name='like-detail'),
	re_path(r'^media/image/?$', csrf_exempt(UploadImage.as_view()), name='upload'),

]