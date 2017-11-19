from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

# 创建sprint模型供后面使用

class Sprint(models.Model):
	"""分解任务用的sprint"""
	name = models.CharField(max_length=100, blank=True, default='')
	description = models.TextField(blank=True, default='')
	end = models.DateField(unique=True)

	def __str__(self):
		return self.name or _('Sprint ending %s') % self.end
		
class Task(models.Model):
	"""为sprint创建的工作单元"""
	STATUS_TODO = 1
	STATUS_IN_PROGRESS = 2
	STATUS_TESTING = 3
	STATUS_DONE = 4

	STATUS_CHOICES = (
		(STATUS_TODO, _('任务还没有开始！')),
		(STATUS_IN_PROGRESS, _('任务处理中...')),
		(STATUS_TESTING, _('任务测试中...')),
		(STATUS_DONE, _('任务已经完成！')),
	)

	name = models.CharField(max_length=100)
	description = models.TextField(blank=True, default='')
	sprint = models.ForeignKey(Sprint, blank=True, null=True)
	status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_TODO)
	order = models.SmallIntegerField(default=0)
	assigned = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	started = models.DateField(blank=True, null=True)
	due = models.DateField(blank=True, null=True)
	completed = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.name

		