from django.contrib.auth import get_user_model

from rest_framework import authentication,permissions,viewsets

from .models import Sprint,Task
from .serializers import SprintSerializer,TaskSerializer,UserSerializer

User = get_user_model()

class DefaultsMixin(object):
	"""视图的验证、权限、过滤、分页的默认设置"""
	authentication_classes = (
		authentication.BasicAuthentication,
		authentication.TokenAuthentication,
	)
	permission_classes = (
		permissions.IsAuthenticated,
	)
	paginate_by = 25
	paginate_by_param = 'page_size'
	max_paginate_by = 100


class SprintViewSet(viewsets.ModelViewSet):
	"""docstring for SprintViewSet"""
	queryset = Sprint.objects.order_by('end')
	serializer_class  = SprintSerializer

class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
	"""列出和创建任务时的API视图"""
	queryset = Task.objects.all()
	serializers_class = TaskSerializer

class UserViewSet(object):
	"""列出用户时的API视图"""

	lookup_field = User.USERNAME_FIELD
	queryset = User.objects.order_by(User.USERNAME_FIELD)
	serializer_class = UserSerializer
		
		