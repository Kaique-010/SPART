from django.http import JsonResponse
from django.shortcuts import render
from .models import Manual
from .qa import responder_pergunta

def perguntar(request):
    pergunta = request.GET.get('pergunta', '')
    if not pergunta:
        return JsonResponse({'error': 'Por favor, insira uma pergunta.'}, status=400)

    manuais = list(Manual.objects.all())   # Pegue todos os objetos do modelo Manual
    resposta = responder_pergunta(pergunta, manuais)  # Passa os objetos diretamente
    return JsonResponse(resposta)

def home(request):
    
    return render(request, 'home.html')

def chat(request):
    sugerir_perguntas = [
        "Como emitir uma nota fiscal?",
        "Qual NCM utilizar?",
        "Como realizar vendas em frente de caixa?",
    ]
    return render(request, 'chat.html', {'sugerir_perguntas': sugerir_perguntas})
