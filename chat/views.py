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

    manuais = list(Manual.objects.all())
    imagens = {
        manual.id: [imagem.imagem.url for imagem in manual.imagens.all()]
        for manual in manuais
    }

    resposta = responder_pergunta(pergunta, manuais, imagens)
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
