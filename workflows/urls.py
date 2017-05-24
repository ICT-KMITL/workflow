from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'workflows'
urlpatterns = [

    url(r'^chat_room1/$', views.chat_room1, name='chat_room1'),
    url(r'^chat_room2/$', views.chat_room2, name='chat_room2'),
    url(r'^chat_room3/$', views.chat_room3, name='chat_room3'),

    url(r'^$', views.index, name='index'),
    url(r'^track/$', views.track, name='track'),
    url(r'^track_modeler/$', views.track_modeler, name='track_modeler'),
    url(r'^create_job/job/$', views.saveXML, name='saveXML'),
    url(r'^create_funding/funding/$', views.saveXML, name='saveXML'),
    url(r'^create_news/announce/$', views.saveXML, name='saveXML'),
    url(r'^create_XML/modeler/$', views.saveXML, name='saveXML'),
    url(r'^create_job/$', views.create_job, name='create_job'),
    url(r'^create_funding/$', views.create_funding, name='create_funding'),
    url(r'^create_news/$', views.create_news, name='create_news'),
    url(r'^create_XML/$', views.create_XML, name='create_XML'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^create/$', views.create, name='create'),
    url(r'^modeler/$', views.modeler, name='modeler'),
    url(r'^create/modeler/$', views.saveXML, name='saveXML'),
    url(r'^(?P<workflow_id>[0-9]+)/modeler/$', views.saveEditedXML, name='saveEditedXML'),
    url(r'^profileedit/$', views.profileEdit, name = 'profileedit'),
    url(r'^register_user/$', views.register_user, name='register_user'),
    url(r'^view_profile/$', views.view_profile, name='view_profile'),
    url(r'^profileDetail/$', views.profileDetail, name='profileDetail'),
    url(r'^job/$', views.job, name='job'),
    url(r'^announce/$', views.announce, name='announce'),
    url(r'^task_noti/$', views.task_noti, name='task_noti'),
    url(r'^funding/$', views.funding, name='funding'),
    url(r'^(?P<workflow_id>[0-9]+)/$', views.editingWorkflow, name='editWorkflow'),
    url(r'^login_user_google/$', views.login_user_google, name='login_user_google'),
    url(r'^design_form/$', views.design_form, name='design_form'),
    url(r'^openXML/$', views.openXML, name='openXML'),
    url(r'^publish/$', views.publish, name='publish'),
    url(r'^tasks/$', views.tasks, name='tasks'),
    url(r'^(?P<task_id>[0-9]+)/do_task/$', views.do_task, name='do_task'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)