from django.contrib import admin
from .models import Manual, ImagemManual

class ImagemManualInline(admin.TabularInline):  # Também pode usar StackedInline
    model = ImagemManual
    extra = 1  # Define quantas imagens vazias serão mostradas por padrão
    fields = ['imagem', 'descricao']
    max_num = 10  # Limite opcional de imagens por manual

@admin.register(Manual)
class ManualAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'link')
    search_fields = ('titulo', 'palavras_chave')
    inlines = [ImagemManualInline]

# Registro direto de ImagemManual no admin (caso precise)
@admin.register(ImagemManual)
class ImagemManualAdmin(admin.ModelAdmin):
    list_display = ('manual', 'descricao')
    search_fields = ('descricao',)
