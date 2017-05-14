from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^workflows/', include('workflows.urls')),
    url(r'^', include('workflows.urls')),
    #url('', include('social.apps.django_app.urls', namespace='social')),
    #url('', include('social.apps.django_app.urls', namespace='social')),
    #url('', include('django.contrib.auth.urls', namespace='auth')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)