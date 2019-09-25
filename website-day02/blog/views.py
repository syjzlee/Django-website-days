from django.shortcuts import render


def index(request):
    context = {
        '文章1': '1',
        '文章2': '2',
        '文章3': '3'
    }

    return render(request, 'index.html', {'context':context})
