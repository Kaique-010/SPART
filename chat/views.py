#views.py

from django.http import JsonResponse
from django.shortcuts import render
from .models import Manual
from .qa import responder_pergunta

from django.http import JsonResponse
from django.shortcuts import render
from .models import Manual, Pergunta
from .qa import responder_pergunta

def perguntar(request):
    pergunta = request.GET.get('pergunta', '')
    if not pergunta:
        return JsonResponse({'error': 'Por favor, insira uma pergunta.'}, status=400)

    
    nova_pergunta = Pergunta.objects.create(texto=pergunta)
    
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
    perguntas = Pergunta.objects.order_by('-data_hora')[:10]
    return render(request, 'chat.html', {'sugerir_perguntas': sugerir_perguntas, 'perguntas': perguntas})


def listar_perguntas(request):
    perguntas = Pergunta.objects.all().order_by('-data_hora')
    perguntas_lista = [{'id': p.id, 'texto': p.texto, 'data_hora': p.data_hora} for p in perguntas]
    return JsonResponse(perguntas_lista, safe=False)
