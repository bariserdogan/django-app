from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

# NOT: Modelde herhangi bir değişiklik yaptığımız zaman bunu database'e migration yoluyla söylememiz gerekiyor.

class Article(models.Model):
    author = models.ForeignKey('auth.user', on_delete=models.CASCADE, verbose_name="Yazar")
    title = models.CharField(max_length=100, verbose_name="Başlık")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    article_image = models.FileField(blank=True, null=True, verbose_name="Makaleye Fotoğraf Ekleyin.")
    def __str__(self): ## one of python default methods
        return self.title

    class Meta():
        ordering = ['-created_date']


class Comment(models.Model):    
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE, verbose_name="Makale")
    # related_name sayesinde  article.comments diyerek comments tablosuna erişebiliriz.
    comment_author = models.CharField(max_length=50, verbose_name="İsim")
    comment_content = models.CharField(max_length=200, verbose_name="Yorum")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    def __str__(self):
        return self.comment_content
    
    class Meta():
        ordering = ['-created_date']