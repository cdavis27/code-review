from rest_framework import generics, permissions, viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.models import *
from api.serializers import *

class ProjectViewSet(viewsets.ModelViewSet):
	queryset = Project.objects.all()
	serializer_class = ProjectSerializer


class FileViewSet(viewsets.ModelViewSet):
	queryset = File.objects.all()
	serializer_class = FileSerializer
