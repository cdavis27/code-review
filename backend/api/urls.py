from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter(trailing_slash=True)
router.register(r'projects', views.ProjectViewSet)
router.register(r'files', views.FileViewSet)

urlpatterns = patterns('',
	url(r'^', include(router.urls)),
    # url(r'projects^$', views.ProjectList.as_view(), name='projects'),
    
)
