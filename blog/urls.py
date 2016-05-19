from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^(?P<id>\d+)/$', views.project_detail, name='project_detail'),
	url(r'^(?P<id>\d+)/edit/$', views.project_update, name='project_update'),
	url(r'^(?P<id>\d+)/delete/$', views.project_delete, name='project_delete'),

	url(r'^newPimage/$', views.newPimage, name='newPimage'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.loginView, name='loginView'),
	url(r'^auth/$', views.auth_view, name='auth_view'),
	url(r'^newproject/$', views.newProjectView, name='newProjectView'),
	url(r'^logout/$', views.logout_view, name='logout_view'),

	url(r'^projects/$', views.projects, name='projects'),

	url(r'^projectlist/$', views.ProjectList.as_view(), name='ProjectList'),	
	url(r'^projectlist/(?P<pk>[0-9]+)$', views.ProjectDetail.as_view(), name="ProjectDetail"),
	
	url(r'^users/$', views.AccountList.as_view()),
	url(r'^users/(?P<pk>[0-9]+)/$', views.AccountDetail.as_view()),

	url(r'^imagelist/$', views.PimageList.as_view(), name='PimageList'),
	url(r'^imagelist/(?P<username>.+)/$', views.PimageList.as_view()),

	url(r'^reviewlist/$', views.ReviewList.as_view(), name='BidList'),
	url(r'^reviewlist/(?P<username>.+)/$', views.ReviewList.as_view()),
	url(r'^reviewlist/(?P<pk>[0-9]+)$', views.ReviewDetail.as_view(), name="ReviewDetail"),

	url(r'^bidlist/$', views.BidList.as_view(), name='ReviewList'),
	url(r'^bidlist/(?P<pk>[0-9]+)$', views.BidList.as_view()),
	url(r'^biddetail/(?P<pk>[0-9]+)$', views.BidDetail.as_view(), name="ReviewDetail"),

	url(r'^(?P<username>[-\w.]+)/$', views.profile, name ='profile'),
	
]




if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)