from django.forms import ModelForm
from article.models import Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article # Artık django bizim modelimizde hangi alanlar varsa ona göre alan oluşturacak.
        fields = ["title", "content", "article_image"] # diğer alanlardan değil sadece title ve content alanlarından model oluştur.
