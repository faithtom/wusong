from django.shortcuts import render, get_object_or_404
from .models import AppDoc

def app_title(request):
    blogs = AppDoc.objects.all()
    return render(request, "app/titles.html", {"blogs":blogs})   # 前台请求数据request，html从blogs变量获取所有数据



def app_article(request, article_id):
    # article = AppDoc.objects.get(id=article_id)
    article = get_object_or_404(AppDoc, id=article_id)
    pub = article.publish
    return render(request, "app/content.html", {"article":article, "publish":pub })