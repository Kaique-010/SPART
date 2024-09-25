from django.db import models
from chat.utils import gerar_palavras_chave

class Manual(models.Model):
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    link = models.URLField()
    palavras_chave = models.TextField(blank=True)  

    def save(self, *args, **kwargs):
        # Se houver conteúdo e as palavras-chave não estiverem definidas, gera automaticamente
        if not self.palavras_chave and self.conteudo:
            self.palavras_chave = gerar_palavras_chave(self.conteudo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo