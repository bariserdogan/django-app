from django.contrib import admin

# Register your models here.

from .models import Article
from .models import Comment

# Register comment without spesification
admin.site.register(Comment)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date') # Admin panelinde article listesinde görünecek kolonları belirliyoruz.
    list_display_links = ('title', 'created_date') # Article listesinde link olarak vermek istediğimiz kolonları belirliyoruz.
    search_fields = ['author__username'] # author_username'e göre arama yapılabileceğini söylüyoruz.
    list_filter = ['created_date'] # created_date kolonuna göre filtreleme yapılabileceğini söylüyoruz.
    class Meta():
        model = Article # Bu Meta classını ArticleAdmin ile Article'ı eşleştirmek için yaptık
    
    


