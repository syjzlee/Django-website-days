from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login
from django.views.generic import View
from blog.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from celery_tasks.tasks import send_register_mail

@login_required
def index(request):
    return render(request,'index.html')

#
# def detail(request,blog_id):
#
#     return render(request,'blog/detail.html',locals())
#
# def login(request):
#     errors =[]
#     account = None
#     password = None
#     if request.method == "POST":
#         if not request.POST.get('account'):
#             errors.append('用户名不能为空')
#         else:
#             account = request.POST.get('account')
#
#         if not request.POST.get('password'):
#             errors = request.POST.get('密码不能为空')
#         else:
#             password = request.POST.get('password')
#
#         if account is not None and password is not None:
#             user = auth.authenticate(username=account,password=password)
#             if user is not None:
#                 if user.is_active:
#                     auth.login(request,user)
#                     return HttpResponseRedirect('/blog')
#                 else:
#                     errors.append('用户名错误')
#             else:
#                 errors.append('用户名或密码错误')
#     return render(request,'blog/login.html', {'errors': errors})

class RegisterView(View):
    def get(self,request):
        return render(request, 'register.html')
    def post(self,request):
        # 接收参数
        email = request.POST.get('email')
        password = request.POST.get('pwd')

        # 数据校验
        if not all([email, password]):
            return render(request, 'register.html', {'errmsg': '请填写所有信息'})
        try:
            user = User.objects.get(username=email)
        except Exception as err:  # User.DoesNotExist:
            user = None
            print(err)
        if user:
            return render(request, 'register.html', {'errmsg': '该用户已存在'})

        # 业务处理：进行注册
        user = User.objects.create_user(username=email, password=password, email=email)
        user.is_active = 0
        user.save()  # 一定要记得设置激活状态为未激活， 添加保存操作
        # 发送邮件激活，生成激活链接，链接要含有用户表示信息，比如ID，然后ID要加密，不能被用户随便试出来，itsdangerous

        # 根据新注册用户的信息（比如ID），利用itsdangerous生成用户token（口令）
        print('start加密')
        serializer = Serializer(settings.SECRET_KEY, 3600)  # 第一个参数是密钥，这边使用django setting中默认的SECRET_KEY， 第二个参数为过期时间
        info = {'confirm': user.id}
        token = serializer.dumps(info).decode()

        print('start')
        # 由代码发布任务。用celery的delay函数
        send_register_mail.delay(token,email,email)
        print('end')


        # 返回结果
        return redirect(reverse('blog:index'))

class ActiveView(View):
    def get(self,reuqest, token):  # 传入url配置中捕获的url参数。
        #对接到参数进行解密
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token.encode())
            user_id = info['confirm']

        #解密完成，进行 数据库激活。  可能的异常是激活链接失效了(此时直接返回一个响应)
        # 待解决问题：激活链接失效了，怎么重新生成激活链接

            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()  # 激活完成

            # 激活结束，返回登录页面
            return redirect(reverse("blog:index"))
        except SignatureExpired as err:
            return HttpResponse("激活链接失效") # 这边失效了，就应该重新生成激活链接（暂时没写，回去看视频有没有更好的方法）



class LoginView(View):
    def get(self,request):
        if 'mysession' in request.COOKIES:  # 注意这边是大写
            username = request.COOKIES['mysession']
            checked = 'checked'  # checked 只要非空就行， 然后接收数据时候就会都变成on
        else:
            username = ''
            checked = ''
        print(username, checked)
        return render(request, 'login.html', {'username':username, 'checked': checked})
    def post(self,request):
        # 接收参数
        username = request.POST.get('email')
        password = request.POST.get('pwd')
        remember = request.POST.get('remember')
        print(username, password, remember)

        # 数据校验
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '请填写完整信息'})

        user = authenticate(username=username, password=password)
        if user is not None:
            # 检测用户是否激活成功
            if user.is_active:
                login(request, user)
                response = redirect(reverse('blog:index'))
                if remember == 'on':
                    print('记住用户名')
                    response.set_cookie('mysession',user.username, 30*24*3600)
                else:
                    print('删除记住的用户名')
                    response.delete_cookie('mysession')
                return response
            else:
                return render(request, 'login.html', {'errmsg': '用户未激活'})
            # login(request, user)  # 登录？ 不太懂
            # response = HttpResponseRedirect('/blog')
            # response.set_cookie('name',user.username, 60*60*24*1)
            # return response
            # return redirect('/blog/')  # 这里要是直接写模板渲染，就不能设置cookie的过期时间了 !  这个有待确认。
        else:
            return render(request, 'login.html', {'errmsg': "用户名或密码错误"})







# def register(request):
#     return render(request,'register.html')

# def register_handle(request):
#     # 接收参数
#     email = request.POST.get('email')
#     password = request.POST.get('pwd')
#
#     # 数据校验
#     if not all([email, password]):
#         return render(request, 'register.html',{'errmsg': '请填写所有信息'})
#     try:
#         user = User.objects.get(username= email)
#     except Exception as err: # User.DoesNotExist:
#         user = None
#         print(err)
#     if user:
#         return render(request, 'register.html', {'errmsg': '该用户已存在'})
#
#     # 业务处理：进行注册
#     User.objects.create_user(username=email, password=password, email=email)
#
#     # 返回结果
#     return redirect(reverse('blog:index'))

# def login(request):
#
#     return render(request, 'login.html')


# def login_handle(request):
#     # 接收参数
#     username = request.POST.get('email')
#     password = request.POST.get('pwd')
#
#     # 数据校验
#     if not all([username, password]):
#         return render(request, 'login.html', {'errmsg': '请填写完整信息'})
#     try:
#         user = authenticate(username=username, password=password)
#     except User.DoesNotExist:
#         user = None
#
#     print(username, password)
#
#     if not user:
#         return render(request, 'login.html', {'errmsg': "用户名或密码错误"})
#     else:
#         return redirect('/blog/')


