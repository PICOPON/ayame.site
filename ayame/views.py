from django.shortcuts import render
from ayame.models import Blog, Schedule, Comment, Mv, Member,Info_donation,Goal
from django.http import Http404, HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms.models import model_to_dict
import re,hashlib
import random,datetime
from django.utils.datastructures import MultiValueDictKeyError
import json
from django.core import serializers
# Create your views here.


def index(request):
    try:
        bs_show = []
        agenda_show = []
        member_show = []
        array_rand_key = []
        blogs = Blog.objects.all()
        agenda = Schedule.objects.all()
        while len(member_show) <= 2:
            rand_key = random.randint(1, 12)
            if rand_key in array_rand_key:
                continue
            else:
                array_rand_key.append(rand_key)
                member_show.append(Member.objects.get(pk=rand_key))
        for i, bs_item in enumerate(reversed(blogs)):
            if i <= 7:
                bs_show.append(bs_item)
            else:
                break
        for i, ag_item in enumerate(reversed(agenda)):
            if i <= 6:
                agenda_show.append(ag_item)
            else:
                break
    except Blog.DoesNotExist:
        raise Http404("No Blogs or No Agenda!")
    return render(request, 'ayame/index.html', {"blogs": bs_show, "agenda":agenda_show,"members":member_show})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            messages.success(request, "登录成功")
            return HttpResponseRedirect("/news/")
        else:
            messages.error(request,"登录失败")
            return render(request, "ayame/login.html")
    else:

        return render(request, "ayame/login.html")


def logout(request):
    auth.logout(request)
    messages.success(request, "已退出登录")
    return HttpResponseRedirect("/")


def register(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            User.objects.create_user(username=username, password=password)
            messages.success(request, "注册成功")
            return HttpResponseRedirect("/news/")
        except:
            messages.error(request, "注册失败")
            return render(request, "ayame/register.html")
    else:
        return render(request, "ayame/register.html")


def search(request):
    search_content = request.POST['search']
    pa = re.compile(search_content)
    bs = Blog.objects.all()
    res = []
    try:
        for bg_item in bs:
            key1 = pa.search(bg_item.title)
            key2 = pa.search(bg_item.summary)
            key3 = pa.search(bg_item.body)
            if (key1 is not None) or (key2 is not None) or (key3 is not None):
                res.append(bg_item)
        if len(res) == 0:
            messages.success(request, "未检索到内容")
        return render(request,"ayame/researchres.html", {"researchres":res})
    except:
        messages.error(request,"检索失败")


#上传新blog
def news(request):
    try:
        bs = Blog.objects.all()
    except Blog.DoesNotExist:
        raise Http404("No Blogs!")
    return render(request, 'ayame/news.html',{"blogs":bs})


#新闻详细页
def singlenews(request, news_id):
    try:
        blog = Blog.objects.get(pk=news_id)
    except Blog.DoesNotExist:
        raise Http404("No this Blog")
    return render(request, 'ayame/singlenews.html', {'blog':blog})


def comment(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            cmt_content = request.POST['comment']
            try:
                Comment.objects.create(comment=cmt_content)
                return HttpResponseRedirect("/comment/")
            except:
                messages.success(request,"评论失败")
                return HttpResponseRedirect("/comment/")
        else:
            messages.success(request,"您未登录")
            return HttpResponseRedirect("/comment/")
    else:
        comments = Comment.objects.all()
        comments = reversed(comments)
        return render(request, "ayame/comment.html", {"comments":comments})


def mv(request, pg_id):
    res_mv = []
    res_item = []
    mv_items = Mv.objects.all()
    rev_mvs = []
    for mv_item in reversed(mv_items):
        rev_mvs.append(mv_item)
    for i in range((int(pg_id)-1)*15, int(pg_id)*15):
        if i % 3 ==0 and i>=3:
            res_mv.append(res_item)
            res_item = []
        res_item.append(rev_mvs[i])
        if i == 14:
            res_mv.append(res_item)
    return render(request, "ayame/mv.html", {"mv1": res_mv[0],"mv2":res_mv[1],"mv3":res_mv[2],"mv4":res_mv[3],"mv5":res_mv[4]})


def pay(request):
    try:
        donations = Info_donation.objects.all()
        gls = Goal.objects.all()
        json_list = []
        res = []
        for dona_item in donations:
            json_dict = model_to_dict(dona_item)
            json_list.append(json_dict)
        md5 = hashlib.md5()
        md5.update(str(datetime.datetime.now()).encode())
        hashcode= md5.hexdigest()[8:-8]
        for gl_item in gls:
            goal_amount = gl_item.goal
        res.append(hashcode)
        res.append(goal_amount)
        res.append(json_list)
    except:
        return Http404("failed")
    # return HttpResponse(, content_type="application/json")
    return render(request, "ayame/pay.html", {"res":res})


def join(request):
    if request.method == "POST":

        return HttpResponse(request.POST['hhcd'])
    else:
        return render(request,"ayame/join.html")