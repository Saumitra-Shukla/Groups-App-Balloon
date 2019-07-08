from django.contrib import admin
from api.models import Item,Asset,AssetBundle,Profile,Like,Comment,Groupps
from django.utils.safestring import mark_safe
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
	# list_display=['title','subtitle','full_title','owner','owner_details','like_count','created_at','updated_at']
	# search_fields=['title']
	pass

class AssetAdmin(admin.ModelAdmin):

	@mark_safe
	def preview(self,obj):
		return '<img src="%s" width="100"/>' % obj.base_url
	
	preview.allow_tags = True

	list_display=['preview','owner','full_detail','base_url']



class AssetBundleAdmin(admin.ModelAdmin):
	
	@mark_safe
	def preview(self, obj):
		html = '<ul>'
		for key, url in obj.asset_urls.iteritems():
			#print key
			html += '<li><a href="%s" target="_blank"><img src="%s" width="128" /></a></li>' % (url, url)

		html += '</ul>'
		return html
	preview.allow_tags = True

	list_display = ['salt', 'kind']
	readonly_fields = ('preview',)

class ProfileAdmin(admin.ModelAdmin):
	
	list_display = ['user']


class LikeAdmin(admin.ModelAdmin):
	
	pass

class CommentAdmin(admin.ModelAdmin):
	
	pass
class GroupAdmin(admin.ModelAdmin):
	
	pass



admin.site.register(Item, ItemAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetBundle, AssetBundleAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Groupps, GroupAdmin)