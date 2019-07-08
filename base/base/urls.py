from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.defaults import permission_denied, page_not_found, server_error
from api import urls as api_urls
from api.auth import urls as auth_urls
admin.autodiscover()

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include(api_urls)),
    re_path(r'^auth/', include(auth_urls)),
]



if settings.DEBUG:
    # Add debug-toolbar
    import debug_toolbar
    urlpatterns.append(re_path(r'^__debug__/', include(debug_toolbar.urls)))

    # Serve media files through Django.
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    # Show error pages during development
    urlpatterns += [
        re_path(r'^403/$', permission_denied),
        re_path(r'^404/$', page_not_found),
        re_path(r'^500/$', server_error)
]