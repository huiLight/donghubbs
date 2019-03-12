from django.shortcuts import render
from django.http import HttpResponse
from donghu.forms import UserForm
from donghu.utils import sendyzm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

import json

# Create your views here.
def index(request):
    return render(request, 'donghu/index.html', {})

def register(request):
    registered = False
    if request.method == 'POST':
        error_code = {'name':1, 'email': 2, 'yzm': 4}
        context_dict = {'success': False, 'state': 0}

        # 判断验证码是否正确
        if request.session['securityCode'] != request.POST.get("yzm"):
        # if '123' != request.POST.get('yzm'): # 测试时使用
            context_dict['state'] += error_code['yzm']
            return HttpResponse(json.dumps(context_dict))

        # 尝试从数据库中获取邮箱
        try:
            User.objects.get(email=request.POST.get('email'))
        except:
            # 有异常证明该地址不存在
            print(request.POST.get('email'))
        else:
            # 该邮箱已被注册
            context_dict['state'] += error_code['email']
            return HttpResponse(json.dumps(context_dict))

        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            print('---valid')
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # 注册成功，自动登录跳转到首页
            user = authenticate(username=user.username, password=request.POST.get("password"))
            login(request, user)
            return HttpResponse(json.dumps({'success': True}))
        else:
            context_dict['state'] += error_code['name']

            return HttpResponse(json.dumps(context_dict))

    context_dict = {'registered': registered}
    return render(request, 'donghu/register.html', context_dict)

def sendcode(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        state, yzm = sendyzm(email)
        print('----------state:'+str(state))
        # 发送成功
        if state:
            request.session['securityCode'] = yzm
            return HttpResponse(json.dumps({"res":True}))
        else:
            return HttpResponse()

def identifycode(request):

    if request.method == "POST":
        # get到的是字符串类型
        species = request.POST.get('species')
        if species == '1':
            if request.session['securityCode'] == request.POST.get("yzm"):
            # if '123' == request.POST.get("yzm"):

                # request.session['pass'] = True 不可以
                return HttpResponse(json.dumps({"state":True}))
            else:
                return HttpResponse(json.dumps({"state":False}))


        if species == '2':
            try:
                # get会抛出异常，filter不会
                User.objects.get(username=request.POST.get('username'))
            except:
                return HttpResponse(json.dumps({"namestate":True}))
            else:
                return HttpResponse(json.dumps({'namestate':False}))

    return HttpResponse(json.dumps({"state":False}))


# 需要修改
def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return render(request, 'donghu/login.html', {'errors': '账号或密码错误！'})
    else:
        return render(request, 'donghu/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')