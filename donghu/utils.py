from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from donghu.models import UserProfile
from django.utils import timezone

from django.core.mail import send_mail
from donghubbs.settings import EMAIL_FROM

import datetime
import random
import smtplib
import pytz



def get_code():
    a = ''
    for i in range(6):
        a += str(random.randint(0, 9))
    return a

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def sendyzm(studentid):
    '''
        接收学号作为参数
        若发送成功，返回True和发送的验证码
        否则返回False和None
    '''
    
    email_to = (studentid.split('@')[0] + '@qq.com',)


    yzm = get_code()
    send_title = 'DonghuBBS验证码'
    send_massage = '您正在注册东湖论坛，验证码是:{0}。请勿告知他人。'.format(yzm)
    try:
        send_status = send_mail(send_title, send_massage, EMAIL_FROM, email_to)
    except:
        return False, yzm
    return send_status, yzm


# 将输入的html标签转义，以防止可能存在的注入及其它安全问题
def replace(stri):
    ascii_list = {'"':'&quot;', "'":"&apos;", '&':'&amp;',
                 '<':'&lt', '>':'&gt;'}
    for old, new in ascii_list.items():
        stri = stri.replace(old, new)
    return stri

def suspend(user):
    """
    封号处理，
    1. 将用户 is_active 设置为false
    2. 加入封禁时间
    """
    user.is_active = False
    user.save()
    try:
        up = UserProfile.objects.get_or_create(user=user)[0]
    except:
        pass
    up.sustime = timezone.now() #不然会出问题
    up.save()

def can_login(user):
    """
    检查封号是否到期
    TODO: 直接返回封号时间，具体时间运算由js进行
    """
    try:
        up = UserProfile.objects.get_or_create(user=user)[0]
    except:
        return False
    time = up.sustime
    delta = datetime.datetime.now().replace(tzinfo=(pytz.timezone('Asia/Shanghai'))) - time
    endtime = time + datetime.timedelta(days=1) - datetime.datetime.now().replace(tzinfo=(pytz.timezone('Asia/Shanghai')))
    endtime = endtime.total_seconds()
    if delta.days >= 1:
        user.is_active = True
        return (True, )
    return False, "{:.0f}小时{:.0f}分{:.0f}秒".format(endtime//60//60, endtime//60%60, endtime%60)


if __name__ == '__main__':
    # str1 = '<abcdeft>'
    # str2 = replace(str1)
    # print(str1, str2)
    # str1.replace('<', '&')
    # print(str1)
    print(sendyzm('123@qq.com'))
