from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.EmailField(max_length=40)
    head = models.ImageField(upload_to='profile_images', blank=True, null=True)
    gender = models.CharField(max_length=3, blank=True, null=True)
    motto = models.CharField(max_length=40, blank=True, null=True)
    sustime = models.DateTimeField(null=True) # 封号开始时间
    exper = models.IntegerField(default=0)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username

class Module(models.Model):
    name = models.CharField(max_length=20, unique=True)
    name_zh = models.CharField(max_length=30, unique=True)
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Module, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
 
class Article(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, to_field='slug')
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    lable = models.CharField(max_length=10, blank=True)
    content = models.TextField()
    content_ismd = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Commentary(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

class ReCommentary(models.Model):
    from_id = models.ForeignKey(User, on_delete=models.CASCADE)
    to_id = models.ForeignKey(Commentary, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    '''
    谁(from)评论/点赞了谁(to)
    action是行为，1为like 2为评论 3为分享
    args:
        action: 1: likes; 2: comments; 3: share;
    '''
    # 两个外键都来自User表，所以需要加related_name，related_name不能为python保留字
    id_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='id_from')
    id_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='id_to')
    action = models.IntegerField()


# 以下为投票字段

class Question(models.Model):
    title = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_times = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Voter(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} | {}'.format(self.voter_id.username, self.choice.choice_text)