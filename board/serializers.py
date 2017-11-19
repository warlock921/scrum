#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-18 23:12:07
# @Author  : warlock921
# @readme  : 这是一个用于生成序列化的程序
# @Version : $Id$
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Sprint,Task

User = get_user_model()

class SprintSerializer(serializers.ModelSerializer):
	"""docstring for SprintSerializer"""

	#每个序列化器都有一个只读字段links提供给响应主体
	links = serializers.SerializerMethodField()
	class Meta:
		model = Sprint
		fields = ('id','name','description','end','links',)

	#为了赋予links的值，每个序列化器都有一个get_links方法生成相关链接
	def get_links(self,obj):
		request = self.context['request']
		return{
			'self' : reverse('sprint-detail', kwargs={'pk':obj.pk}, request=request)
		}

class TaskSerializer(serializers.ModelSerializer):
	"""docstring for TaskSerializer"""
	assigned = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD,required=False,queryset=User.objects.all())
	status_display = serializers.SerializerMethodField()

	#每个序列化器都有一个只读字段links提供给响应主体
	links = serializers.SerializerMethodField()

	class Meta:
		model = Task
		fields = ('id','name','description','sprint','status','status_display','order','assigned','started','due','completed','links',)

	def get_status_display(self,obj):
		return obj.get_status_display()

	#为了赋予links的值，每个序列化器都有一个get_links方法生成相关链接
	def get_links(self,obj):
		request = self.context['request']
		links = {
			'self' : reverse('task-detail', 
				kwargs={'pk':obj.pk}, request=request),
			'sprint':None,
			'assigned':None
		}
		if obj.sprint_id:
			links['sprint'] = reverse('sprint-detail',
				kwargs={'pk':obj.sprint_id}, request=request)
		if obj.assigned:
			links['assigned'] = reverse('user-detail',
				kwargs={User.USERNAME_FIELD:obj.assigned}, request=request)
		return links

class UserSerializer(serializers.ModelSerializer):
	"""docstring for UserSerializer"""
	full_name = serializers.CharField(source='get_full_name',read_only=True)

	#每个序列化器都有一个只读字段links提供给响应主体
	links = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ('id',User.USERNAME_FIELD,'full_name','is_active','links',)

	#为了赋予links的值，每个序列化器都有一个get_links方法生成相关链接
	def get_links(self,obj):
		request = self.context['request']
		username = obj.get_username()
		return{
			'self' : reverse('user-detail', kwargs={User.USERNAME_FIELD:username}, request=request)
		}
			
			
		