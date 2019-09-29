from django.shortcuts import render
from blog.models import Categorys,Tags,Article

def index(request):
    article_list = Article.objects.all()

    return render(request, 'index.html', {'article_list':article_list})
