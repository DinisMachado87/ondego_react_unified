from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from .views import logout_route

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls')),
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/dj-rest-auth/logout/', logout_route),
    path(
        'api/dj-rest-auth/registration/',
        include('dj_rest_auth.registration.urls')
    ),
    path('api/', include('profiles.urls')),
    path('api/', include('events.urls')),
    path('api/', include('comments.urls')),
    path('api/', include('joinings.urls')),
    path('api/', include('friends.urls')),
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]

handler404 = TemplateView.as_view(template_name='index.html')

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
