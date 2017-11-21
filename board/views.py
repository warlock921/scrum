from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import get_user_model

#导入rest_framework的相关模块，有验证、权限、视图、过滤器等
from rest_framework import authentication,permissions,viewsets,filters

from .forms import TaskFilter,SprintFilter
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
	filter_backends = (
		DjangoFilterBackend,
		filters.SearchFilter,
		filters.OrderingFilter,
	)


class SprintViewSet(viewsets.ModelViewSet):
	"""所有API的端点"""
	queryset = Sprint.objects.order_by('end')
	serializer_class  = SprintSerializer
	filter_class = SprintFilter
	search_fields = ('name',)
	ordering_fields = ('end','name',)

class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
	"""创建任务的API端点"""
	queryset = Task.objects.all()
	serializer_class = TaskSerializer
	filter_class = TaskFilter
	search_fields = ('name','description',)
	ordering_fields = ('name','order','started','due','completed',)

class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
	"""用户列表的API端点"""

	lookup_field = User.USERNAME_FIELD
	lookup_url_kwarg = User.USERNAME_FIELD
	queryset = User.objects.order_by(User.USERNAME_FIELD)
	serializer_class = UserSerializer
	search_fields = (User.USERNAME_FIELD,)
		
		