from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.urls import reverse_lazy
from django.db.models import Q, F

from donghu.utils import sendyzm
from donghu.forms import UserForm
from donghu.models import UserProfile
from donghu.models import Article, Module, Commentary, ReCommentary
from donghu.models import Question, Choice, Voter

import json
from donghu import utils

# Create your views here.
def index(request):
    module_list = Module.objects.all()
    modules = {}
    for i in module_list:
        if i.name == 'vote':
            modules[i] = (Question.objects.all().order_by('-create_time')[:8])
        else:
            modules[i] = (Article.objects.filter(module=i).order_by('-create_time')[:8])


    hot_article_list = Article.objects.all().order_by('-likes')[:8]

    context_dict = {'category': 'index', 'modules':modules, 'hot_article_list':hot_article_list}

    return render(request, 'donghu/index.html', context_dict)

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
                return HttpResponseRedirect('/index/')
            else:
                if utils.can_login(user)[0]:
                    login(request, user)
                    return HttpResponseRedirect('/index/')
                else:
                    return render(request, 'donghu/login.html', {'errors': '因违规操作，您的账号暂时无法登录请在'+utils.can_login(user)[1]+'后登录'})
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return render(request, 'donghu/login.html', {'errors': '账号或密码错误！'})
    else:
        if request.user.username!='':
            return HttpResponseRedirect('/index/')
        return render(request, 'donghu/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def category(request, category_name_slug, page=1):
    context_dict = {'curpage':page, 'category': category_name_slug}
    context_dict['modules'] = Module.objects.all()

    page = page*10

    if category_name_slug == 'vote':
        article_list = Question.objects.all().order_by('-create_time')
    else:
        article_list = Article.objects.filter(module=category_name_slug).order_by('-create_time')
        context_dict['top_list'] = article_list.filter(is_sticky=True).order_by('-create_time')[:5]
        article_list = article_list.filter(is_sticky=False)
        
    items = len(article_list)
    context_dict['pagenums'] = items//10 if items%10==0 else items//10+1
    
    article_list = article_list[page-10:page]
    context_dict['article_list'] = article_list

    return render(request, 'donghu/category.html', context_dict)

@login_required
def add_article(request):
    # 如果账号已经被禁
    if not request.user.is_active:
        logout(request)
        return render(request, 'donghu/login.html', {'errors': '因违规操作，您的账号暂时无法登录'})

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        try:
            user = User.objects.get(username=request.user)
        except Exception:
            # print(Exception)
            return HttpResponse('用户信息错误，请重新登录')
        try:
            module = Module.objects.get(name=request.POST.get('module'))
        except:
            return HttpResponse("分类丢了，请重新填写。")
        c = Article(module=module, title=title,author=user, content=content, content_ismd=True)
        c.save()
        return category(request, module.name)
    return render(request, 'donghu/index.html')

def detail(request, category_name_slug, username, aid):

    try:
        a = Article.objects.get(id = aid)
    except:
        return render(request, 'donghu/404.html')
    if not request.session.get('read{}'.format(aid)):
        request.session['read{}'.format(aid)] = True
        a.views += 1
        a.save()

    comment_list = Commentary.objects.filter(article=a)
    recomment_list = {}
    for comment in comment_list:
        recomment_list[comment] = ReCommentary.objects.filter(to_id=comment)
    context_dict = {"passage": a, 'comments': recomment_list, 'category': category_name_slug}
    return render(request, 'donghu/passage.html', context_dict)

@login_required
def delete_article(request, aid, category_name_slug):
    
    if category_name_slug == 'vote':
        try:
            a = Question.objects.get(pk = aid)
        except:
            return HttpResponseRedirect('/404.html')
        else:
            a.delete()
        return HttpResponseRedirect('/category/vote')

    try:
        a = Article.objects.get(id=aid)
    except:
        return HttpResponseRedirect('/404.html')
    
    user = a.author

    if (request.user == a.author or 
    request.user.has_perm('donghu.have_permission_'+category_name_slug)):
        a.delete()

    # 封号
    if (request.method == 'POST' and 
    request.user.has_perm('donghu.have_permission_'+category_name_slug)):
        utils.suspend(user) # 暂封账号
        return JsonResponse({'success':True})

    return HttpResponseRedirect('/category/'+category_name_slug)

@login_required
def delete_comment(request, category_name_slug, aid, cid):
    try:
        c = Commentary.objects.get(id=cid)
    except:
        return HttpResponseRedirect('/404.html')


    user = c.author

    # TODO(huilight@oulook.com): 管理员，版主等亦可删除
    if (request.user == c.author or
    request.user.has_perm('donghu.have_permission_'+category_name_slug)):
        c.delete()

    # 封号
    if (request.method == 'POST' and 
    request.user.has_perm('donghu.have_permission_'+category_name_slug)):
        utils.suspend(user) # 暂封账号
        return JsonResponse({'success':True})

    try:
        a = Article.objects.get(id = aid)
    except:
        return HttpResponseRedirect('/404.html')

    return detail(request, category_name_slug, a.author, aid)

@login_required
def submit_comment(request):
    try:
        article = Article.objects.get(id=request.POST.get('to'))
    except:
        return JsonResponse({'success':False})

    content = request.POST.get('content')
    # content = utils.replace(content)
    com = Commentary(article=article, author=request.user, content=content)
    com.save()
    return JsonResponse({'success':True})

@login_required
def personal(request, username, uid):
    '''
    两个入口：
        一、 自己查看自己的个人中心
            显示个人资料入口
            显示与我相关  建立相应表，有用户评论或 @我 时，在表中加入数据，另一表格有应已读标志位
                用来确定是否有未读消息
            列出我发表的文章等
        二、 他人查看
            列出发表的文章
    '''
    context_dict = {'is_visitor': True}
    context_dict['article_list'] = Article.objects.filter(author=uid).order_by('-create_time')
    if request.user.id == uid:
        context_dict['is_visitor'] = False
        context_dict['comment_list'] = Commentary.objects.filter(author=uid).order_by('-create_time')
        context_dict['poll_list'] = Question.objects.filter(author=uid).order_by('-create_time')
        return render(request, 'donghu/personalpage.html', context_dict)
    # 避免构造链接打开此页面
    else:
        return render(request, 'donghu/personalpage.html', context_dict)

@login_required
def profile(request):
    if request.method == 'POST':
        head = request.FILES.get('file')
        print(head.content_type)
        if head.content_type.split('/')[-1] not in ['jpg', 'gif', 'png', 'jpeg']:
            return render(request, 'donghu/404.html')
        name = '{}{}.{}'.format(request.user.username, request.user.id, head.content_type.split('/')[-1])
        print(name, request.user.username)
        head.name = name
        gender = request.POST.get('gender')
        motto = request.POST.get('motto')
        with open('media/profile_images/{}'.format(name), "wb+") as f:
            for chunk in head.chunks():
                f.write(chunk)
        up = UserProfile.objects.get_or_create(user = request.user)[0]
        up.head = head
        up.gender = gender
        up.motto = motto
        up.save()
        return HttpResponseRedirect('/')
        # return render(request, 'donghu/profile.html', {'message':'修改成功' ,'pro':up})

    up = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'donghu/profile.html', {'pro':up})

def search(request):
    try:
        search_content = request.POST.get('search').strip()
    except:
        return render(request, 'donghu/404.html')
    try:
        username = request.POST.get('usersearch').strip()
    except:
        pass
    if search_content != '':
        results = Article.objects.filter(Q(title__contains=search_content)|Q(content__contains=search_content)).order_by('-create_time')

        context_dict = {'keywords':search_content, 'results':results}
        return render(request, 'donghu/result.html', context_dict)
    elif username != '':
        results = User.objects.filter(Q(username__contains=username))
        return render(request, 'donghu/userlist.html', {"userlist":results})

    return render(request, 'donghu/result.html')
# -----------------------vote----------------------------


def vote_detail(request, question_id):

    q = get_object_or_404(Question, pk=question_id)

    cho = Choice.objects.filter(question=q)

    context_dict = {'question':q, 'choice': cho}
    return render(request, 'donghu/vote_detail.html', context_dict)

# show the results of vote
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    res = [['votes', 'item']]
    for c in question.choice_set.all():
        d = [c.votes, c.choice_text]
        res.append(d)
    return render(request, 'donghu/vote_results.html', {'question': question, 'result':res})

@login_required
def vote(request, question_id):
    """
    """
    question = get_object_or_404(Question, pk=question_id)
    
    vot = Voter.objects.filter(question=question, voter_id=request.user)
    if len(vot) != 0:
        return render(request, 'donghu/vote_detail.html',{
                'question': question,
                'error_message': "您已投过票，请不要重复投票。",
                })

    question.vote_times += 1
    question.save()
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'donghu/vote_detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        try:
            Voter.objects.create(question=question, choice=selected_choice, voter_id=request.user)
        except:
            return render(request, 'donghu/vote_detail.html',{
                'question': question,
                'error_message': "用户错误，请重试！",
                })
  
        return HttpResponseRedirect(reverse('donghu:results', args=(question.id,)))

@login_required
def add_vote(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        count = int(request.POST.get("count"))

        q = Question.objects.create(title=title, author=request.user)
        for i in range(count):
            content = request.POST.get("item{}".format(i+1))
            if content != '':
                Choice.objects.create(question=q, choice_text=content)
        return HttpResponseRedirect(reverse('donghu:vote_detail', args=(q.id,)))

    return render(request, 'donghu/addvote.html')

def advanced_search(request):
    if request.method == 'POST':
        try:
            search_content = request.POST.get('srchtxt').strip()
            username = request.POST.get('srchuname').strip()
            srchfilter = request.POST.get('srchfilter').strip()
            srchfrom = request.POST.get('srchfrom').strip()
            orderby = request.POST.get('orderby').strip()
            ascdesc = request.POST.get('ascdesc').strip()
            srchfid = request.POST.getlist('srchfid')
        except:
            return render(request, 'donghu/404.html')

        results = Article.objects.filter(Q(title__contains=search_content)|
            Q(content__contains=search_content))
        if username != '':
            user = User.objects.filter(username=username)
            if user != None:
                results = results.filter(author=user)

        if srchfid != 'all':
            results = results.filter(module__id__in=srchfid)

        if orderby == 'dateline':
            if ascdesc == 'asc':
                results = results.order_by('create_time')
            if ascdesc == 'desc':
                results = results.order_by('-create_time')
        elif orderby == 'views':
            if ascdesc == 'asc':
                results = results.order_by('views')
            if ascdesc == 'desc':
                results = results.order_by('-views')

        context_dict = {'keywords':search_content, 'results':results}
        return render(request, 'donghu/result.html', context_dict)


    else:
        module = Module.objects.all()
        return render(request, 'donghu/search.html', {'module': module})