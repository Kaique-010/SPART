#views.py

from django.http import JsonResponse
from django.shortcuts import render
from .models import Manual
from .qa import responder_pergunta

from django.http import JsonResponse
from django.shortcuts import render
from .models import Manual
from .qa import responder_pergunta

def perguntar(request):
    pergunta = request.GET.get('pergunta', '')
    if not pergunta:
        return JsonResponse({'error': 'Por favor, insira uma pergunta.'}, status=400)

    # Você pode usar um filtro para encontrar um manual relevante
    manuais = Manual.objects.filter(titulo__icontains=pergunta)  # Ajuste o filtro conforme necessário

    if not manuais.exists():
        return JsonResponse({'error': 'Nenhum manual encontrado para a pergunta.'}, status=404)

    resposta_texto = ""
    imagens = []

    for manual in manuais:
        resposta_texto += manual.conteudo + "\n"  # Ou outra lógica para compor a resposta
        imagens += [imagem.imagem.url for imagem in manual.imagens.all()]  # Assumindo que você tem um campo relacionado para imagens

    resposta = {
        "resposta": resposta_texto.strip(),
        "imagens": imagens,
    }

    return JsonResponse(resposta)



def home(request):
    return render(request, 'home.html')



def chat(request):
    sugerir_perguntas = [
        "Como emitir uma nota fiscal?",
        "Qual NCM utilizar?",
        "Como emitir uma nota de devolução",
    ]
    return render(request, 'chat.html', {'sugerir_perguntas': sugerir_perguntas})
