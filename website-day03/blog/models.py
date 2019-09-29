from django.db import models
from django.contrib.auth.models import User  # 导入内建的User模型，之后方便用户认证等。博客就可以快速加入用户登录注册认证等功能。


class Categorys(models.Model):
    category_name = models.CharField(max_length=128, verbose_name='博客分类')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = '博客分类'


class Tags(models.Model):
    tag_name = models.CharField(max_length=128, verbose_name='博客标签')

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = '博客标签'
        verbose_name_plural = '博客标签'


class Article(models.Model):
    title = models.CharField(max_length=128, verbose_name='标题')
    auth = models.ForeignKey(User, verbose_name='作者')  # 作者和文章是一对多的关系，所以这边使用ForeignKey用于关联查询
    categorys = models.ManyToManyField(Categorys, verbose_name='分类') # 文章和分类是多对多的关系
    tags = models.ManyToManyField(Tags,verbose_name='标签')  # 标签和分类也是多对多的关系
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')
    abstract = models.TextField(max_length=256, blank=True, verbose_name='摘要')
    body = models.TextField(verbose_name='正文')
    img = models.ImageField(upload_to='images', blank=True, null=True, verbose_name='博客插图')
    page_view = models.SmallIntegerField(default=0,verbose_name='访问量')

    class Meta:
        verbose_name = '博客文章'
        verbose_name_plural = '博客文章'
        ordering = ['-created_time']