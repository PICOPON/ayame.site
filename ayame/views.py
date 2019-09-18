from django.shortcuts import render
from ayame.models import Blog, Schedule, Comment, Mv, Member, Info_donation, Goal
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms.models import model_to_dict
import re, hashlib
import random, datetime
from django.shortcuts import render
from ayame.models import Blog, Schedule, Comment, Mv, Member
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
import re
import random
from PIL import Image
from django.core.files.base import ContentFile
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from binascii import b2a_hex, a2b_hex
import base64


# Create your views here.
hashcode = ''

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
    return render(request, 'ayame/index.html', {"blogs": bs_show, "agenda": agenda_show, "members": member_show})


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
            messages.error(request, "登录失败")
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
        return render(request, "ayame/researchres.html", {"researchres": res})
    except:
        messages.error(request, "检索失败")


# 上传新blog
def news(request):
    try:
        bs = Blog.objects.all()
    except Blog.DoesNotExist:
        raise Http404("No Blogs!")
    return render(request, 'ayame/news.html', {"blogs": bs})


# 新闻详细页
def singlenews(request, news_id):
    try:
        blog = Blog.objects.get(pk=news_id)
    except Blog.DoesNotExist:
        raise Http404("No this Blog")
    return render(request, 'ayame/singlenews.html', {'blog': blog})


def comment(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            cmt_content = request.POST['comment']
            try:
                Comment.objects.create(comment=cmt_content)
                return HttpResponseRedirect("/comment/")
            except:
                messages.success(request, "评论失败")
                return HttpResponseRedirect("/comment/")
        else:
            messages.success(request, "您未登录")
            return HttpResponseRedirect("/comment/")
    else:
        comments = Comment.objects.all()
        comments = reversed(comments)
        return render(request, "ayame/comment.html", {"comments": comments})


def mv(request, pg_id):
    res_mv = []
    res_item = []
    mv_items = Mv.objects.all()
    rev_mvs = []
    for mv_item in reversed(mv_items):
        rev_mvs.append(mv_item)
    for i in range((int(pg_id) - 1) * 15, int(pg_id) * 15):
        if i % 3 == 0 and i >= 3:
            res_mv.append(res_item)
            res_item = []
        res_item.append(rev_mvs[i])
        if i == 14:
            res_mv.append(res_item)
    return render(request, "ayame/mv.html",
                  {"mv1": res_mv[0], "mv2": res_mv[1], "mv3": res_mv[2], "mv4": res_mv[3], "mv5": res_mv[4]})


def donate(request):
    try:
        donations = Info_donation.objects.all()  # 获取所有捐赠人信息
        gls = Goal.objects.all()
        json_list = []
        res = []
        for dona_item in donations:
            json_dict = model_to_dict(dona_item)
            json_list.append(json_dict)
        md5 = hashlib.md5()
        md5.update(str(datetime.datetime.now()).encode())  # MD5加密
        global hashcode
        hashcode = md5.hexdigest()[8:-8]
        for gl_item in gls:
            goal_amount = gl_item.goal
        res.append(hashcode)  # hashcode
        res.append(goal_amount)  # 总捐助额
        res.append(json_list)  # 捐助人信息具体项列表
    except:
        return Http404("failed")
    # return HttpResponse(, content_type="application/json")
    return render(request, "ayame/donate.html", {"res": res})


def join(request):
    if request.method == "POST":
        return HttpResponse(request.body)
    return render(request, "ayame/join.html")


def submit(request, hcode):
    # 验证hashcoded是否为同一个
    # if hcode == **:
    # pass
    # else:
    global hashcode
    print(hashcode)
    print(hcode)
    if hashcode == hcode:
        if request.method == "POST":
            # 获取key和iv
            key = request.POST.get('hashcode')  # 加密key
            iv = request.POST.get('date')  # 偏移时间戳
            mode = AES.MODE_CBC  # CBC模式加密
            DCP = decrypt_AES(key, mode, iv)
            # 解密类的实例
            # 获取multipart/form-data
            name = request.POST.get('name')
            amount = request.POST.get('amount')
            alipay = request.POST.get('alipay')
            qq = request.POST.get('qq')
            pwd = request.POST.get('pwd')
            msg = request.POST.get('msg')
            img = request.FILES.get("image")  # 图片数据获取
            # 存储上传图片
            image = Image.open(ContentFile(img.read()))
            image = image.convert('RGB')
            new_path = "http://www.ynsszs.fun/static/imgs/" + hcode + '.jpg'
            image.save('static/media/' + hcode + '.jpg')  # 按照hashcode存储
            # 解密加密的数据
            de_name = DCP.decrypt(name)
            de_amount = DCP.decrypt(amount)
            de_alipay = DCP.decrypt(alipay)
            de_qq = DCP.decrypt(qq)
            de_pwd = DCP.decrypt(pwd)
            de_msg = DCP.decrypt(msg)
            # 存储解密的数据
            obj = Info_donation.objects.create(name=de_name,donated_amount=de_amount,message=de_msg, alipay_account=de_alipay,qq_account=de_qq,pwd=de_pwd,image=new_path)
            obj.save()
            # 展示解密后的数据
            print(de_name, de_amount, de_alipay, de_qq, de_pwd, de_msg)
            return HttpResponse("Post Successed.")
        else:
            return HttpResponse("No Responce!")
    else:
        return HttpResponse("invalid operation!")
    ###


################################################

class decrypt_AES:  # 解密类
    def __init__(self, key, mode, iv):
        self.key = key.encode('utf-8')  # 16byte key
        self.mode = mode
        self.iv = iv.encode('utf-8')  # 16byte iv

    def decrypt(self, text):  # 解密
        cryptor = AES.new(self.key, self.mode, self.iv)
        base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
        decrypted_text = str(cryptor.decrypt(base64_decrypted), encoding='utf-8')  # 执行解密密并转码返回str
        unpad = lambda s: s[0:-ord(s[-1])]
        return unpad(decrypted_text)
