from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

#博客上传


class Blog(models.Model):
    title = models.CharField(u'推文标题', blank=False, max_length=30, null=False, unique=True, help_text='请输入标题不超过30个字')
    summary = models.CharField(u'推文简要概括', blank=True, max_length=200, null=True, help_text='请输入简要概括，不超过200个字')
    created_time = models.DateField(auto_now=True)
    # 博客的内容为 RichTextField 对象
    body = RichTextField(u'推文', config_name='my_config', help_text='上传的图片宽不要超过777px')

    def __str__(self):
        return self.title

#日程计划上传


class Schedule(models.Model):
    date = models.DateField(u'预计日期', blank=False, null=False, help_text='请选择预计日期')
    agenda = models.CharField(u'预计事项', blank=False, max_length=100, null=False, help_text='请输入预计事项,不超过100字')

    def __str__(self):
        return self.agenda

#评论上传


class Comment(models.Model):
    comment_time = models.DateTimeField(auto_now=True)
    comment = models.CharField(u'评论', blank=False, max_length=300, null=False, help_text='请输入评论,不超过300字')

    def __str__(self):
        return self.comment

#mv上传


class Mv(models.Model):
    mv_title = models.CharField(u'mv标题', blank=False, max_length=300, null=False, help_text='请输入标题,不超过300字')
    mv_pic_url = models.URLField(u'封面链接', blank=False, null=False, help_text='请添加视频封面链接')
    mv_url = models.URLField(u'视频链接', blank=False, null=False, help_text='请添加视频链接')
    mv_uptime = models.DateField(auto_now=True)

    def __str__(self):
        return self.mv_title


#成员

class Member(models.Model):
    member_profile = models.CharField(u'成员简介',blank=False,max_length=200, null=False, help_text='请添加成员简介')
    member_picurl = models.URLField(u'成员头像',blank=False, null=False, help_text='请添加成员头像链接')

    def __str__(self):
        return self.member_profile

