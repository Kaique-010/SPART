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


class ImagemManual(models.Model):
    manual = models.ForeignKey(Manual, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='manuais/')
    descricao = models.CharField(max_length=200, blank=True, null=True)  # Descrição opcional da imagem

    def __str__(self):
        return f"Imagem para {self.manual.titulo}"


class Pergunta(models.Model):
    texto = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texto