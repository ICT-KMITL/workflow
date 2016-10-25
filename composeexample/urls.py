
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^draw/', include('draw.urls')),
    url(r'^workflows/', include('workflows.urls')),
    url(r'^admin/', admin.site.urls),

]
