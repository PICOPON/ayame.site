from django.contrib import admin
from .models import Blog,Schedule,Comment,Mv,Member
# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # 列表页面显示字段
    list_display = ['title', 'summary', 'body']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['date', 'agenda']


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ['comment_time', 'comment']


@admin.register(Mv)
class Comment(admin.ModelAdmin):
    list_display = ['mv_title', 'mv_pic_url', 'mv_url']


@admin.register(Member)
class Comment(admin.ModelAdmin):
    list_display = ['member_profile', 'member_picurl']
