from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import ArticleForm
from django.contrib import messages
from .models import Article
from .models import Comment
from django.http import Http404
from django.contrib.auth.decorators import login_required

# Create your views here.
# Vİew fonksiyonlarımızı bu classta yazacağız
# yani url'ler bu classta çalışacak.

def index(request): # bu request değişkeninin her view fonksiyonunda ilk parametre olarak bulunması gerekiyor.
    context = {
        "numbers":[1,2,3,4,5,6]
    }
    return render(request, "index.html", context)

def about(request):
    return render(request, "about.html")

def detail(request, id):
    #article = Article.objects.filter(id=id).first()
    article = get_object_or_404(Article, id=id)

    comments = article.comments.all()

    context = {
        "article": article,
        "comments": comments
    }
    return render(request, "detail.html", context)

def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains=keyword) # keyword'ün geçtiği article'ları gönderecek.
        return render(request, "articles.html", {'articles': articles})
    articles = Article.objects.all()
    return render(request, "articles.html", {"articles": articles})

@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author=request.user)
    context = {
        "articles": articles
    }
    return render(request, "dashboard.html", context)


@login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None) # image dosyaları request.FILES'ta tutulur. 
    
    if form.is_valid():
        article = form.save(commit=False) # save işlemini gerçekleştirme, bunu ben gerçekleştireceğim diyoruz. O nedenle False verdik.
        
        article.author = request.user # Şu anda sistemdeki kullanıcı
        article.save() # Artık commit işlemini kendimiz yapmış oluyoruz.

        messages.success(request, "Makale başarıyla oluşturuldu")
        return redirect("article:dashboard")
    context = {
        "form": form
    }
    return render(request, "addArticle.html", context)


@login_required(login_url="user:login")
def updateArticle(request, id):
    article = get_object_or_404(Article, id=id, author=request.user)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)

    if form.is_valid():
        article = form.save(commit=False) # save işlemini gerçekleştirme, bunu ben gerçekleştireceğim diyoruz. O nedenle False verdik.
        article.author = request.user # Şu anda sistemdeki kullanıcı
        article.save() # Artık commit işlemini kendimiz yapmış oluyoruz.

        messages.success(request, "Makale başarıyla güncellendi")
        return redirect("article:dashboard")
    context = {
        "form": form
    }
    return render(request, "update.html", context)


@login_required(login_url="user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id=id, author=request.user)

    if article:
        article.delete()
        messages.success(request, "Makale başarıyla silindi")
        return redirect("article:dashboard")

def addComment(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        comment_author = request.POST.get('commentAuthor')
        comment_content = request.POST.get('commentContent')
        new_comment = Comment(comment_author=comment_author, comment_content=comment_content)
        new_comment.article = article
        new_comment.save()
    return redirect(reverse("article:detail",kwargs={"id": id})) # Dinamik bir url'yi redirect ederken reverse fonksiyonunu kullanmamız gerekiyor.