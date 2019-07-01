from celery import Celery
import time
from django.core.mail import send_mail
from django.conf import settings
# from celery_tasks import celeryconfig

"""
celery是一个python的分布式任务队列框架，支持 分布的 机器/进程/线程的任务调度。采用典型的生产者-消费者模型
"""
# 生celery实例
# app = Celery('email_register_celery_task', broker='redis://127.0.0.1:6379/8')
app = Celery('email_register_celery_task')
app.conf.update(
    result_backend = 'redis://@127.0.0.1:6379/5',
    broker_url = 'amqp://',
    # broker_url = 'redis://127.0.0.1:6379/9'
)
# app.config_from_object('celeryconfig')

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()


# 邮件注册任务
@app.task
def send_register_mail(token, email, user):
    subject = '个人博客注册欢迎您'
    message = ''
    from_email = settings.EMAIL_FROM
    recipient_list = [email]
    # 生成加密的激活连接，发送邮件进行激活
    html_message = '<h1>%s,您好，请点击下面的链接完成注册</h1></br><a  href="http://127.0.0.1:8000/blog/active/%s">http://127.0.0.1:8000/blog/active/%s</a>' %(user,token,token)
    print(html_message)
    send_mail(subject, message, from_email, recipient_list, html_message=html_message )
    time.sleep(5)




