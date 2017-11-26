#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-18 23:12:07
# @Author  : warlock921
# @readme  : 这是一个用于生成序列化的程序
# @Version : $Id$
from datetime import date

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

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
			'self' : reverse('sprint-detail', kwargs={'pk':obj.pk}, request=request),
			'tasks' : reverse('task-list', request=request) +'?sprint={}'.format(obj.pk),
		}

	def validate_date(self,value):
		new = self.instance is None
		changed = self.instance and self.instance.end != value 
		if(new or changed) and (value.end < date.today()):
			msg = _('已结束的项目不能使用结束时间.')
			raise serializers.ValidationError(msg)
		return value


class TaskSerializer(serializers.ModelSerializer):
	"""docstring for TaskSerializer"""
	assigned = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD,required=False,queryset=User.objects.all())
	status_display = serializers.SerializerMethodField()

	#每个序列化器都有一个只读字段links提供给响应主体
	links = serializers.SerializerMethodField()

	def validate_sprint(self,value):
		if self.instance and self.instance.pk:
			if value != self.instance.sprint:
				if self.instance.status == Task.STATUS_DONE:
					msg = _('Cannot change the sprint of a completed task.')
					raise serializers.ValidationError(msg)
				if value and value.end < date.today():
					msg = _('Cannot assign tasks to past sprints')
					raise serializers.ValidationError(msg)

		else:
			if value and value.end < date.today():
				msg = _('Cannot add tasks to past sprints.')
				raise serializers.ValidationError(msg)

		return value

	def validate(self,attrs):
		sprint = attrs.get('sprint')
		status = attrs.get('status',Task.STATUS_TODO)
		started = attrs.get('started')
		completed = attrs.get('completed')
		if not sprint and status != Task.STATUS_TODO:
			msg = _('Backlog tasks must have "Not Started" status.')
			raise serializers.ValidationError(msg)
		if started and status == Task.STATUS_TODO:
			msg = _('Started date cannot be set for not started tasks.')
			raise serializers.ValidationError(msg)
		if completed and status != Task.STATUS_DONE:
			msg = _('Completed date cannnot be set for uncompleted tasks.')
			raise serializers.ValidationError(msg)
		return attrs

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
			'self' : reverse('user-detail', kwargs={User.USERNAME_FIELD:username}, request=request),
			'tasks' : '{}?assigned={}'.format(reverse('task-list', request=request), username)
		}
			
			
		