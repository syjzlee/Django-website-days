from django.conf.urls import url
from . import views
from blog.views import RegisterView,LoginView,ActiveView

app_name = 'blog'

urlpatterns = [
    # url(r'^register$', views.register, name='register'),
    # url(r'^register_handle$', views.register_handle, name='register_handle'),
    # url(r'^login$', views.login, name='login'),
    # url(r'^login_handle$', views.login_handle, name='login_handle'),
    url(r'^$', views.index, name='index'),

    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'), # 一点链接就进行激活处理。因为这条链接只有他自己知道
]