# qa.py

from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
import numpy as np  # type: ignore
from chat.models import Manual
from chat.utils import gerar_palavras_chave
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from nltk.tokenize import sent_tokenize
from django.utils.safestring import mark_safe
import os
from django.http import JsonResponse



def resumir_texto(texto):
    try:
        parser = PlaintextParser.from_string(texto, Tokenizer("portuguese"))
    except LookupError:
        sentencas = sent_tokenize(texto, language='portuguese')
        parser = PlaintextParser.from_string(" ".join(sentencas), Tokenizer("english"))

    summarizer = LsaSummarizer()
    resumo = summarizer(parser.document, 10)  # Limitar a 5 frases no resumo
    return ' '.join(str(frase) for frase in resumo)



def responder_pergunta(pergunta, manuais, imagens):
    palavras_chave_pergunta = gerar_palavras_chave(pergunta)

    # Gerar o resumo dos conteúdos dos manuais
    conteudos_resumidos = [resumir_texto(manual.conteudo) for manual in manuais]
    palavras_chave_manuais = [manual.palavras_chave for manual in manuais]

    # Preparar os documentos para o TF-IDF
    documentos = [palavras_chave_pergunta] + palavras_chave_manuais

    # Criar o vetor TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documentos)

    # Calcular a similaridade da pergunta com os manuais
    similaridades = np.dot(X[0], X[1:].T).toarray().flatten()

    # Encontrar o índice do manual mais similar
    indice_mais_similar = np.argmax(similaridades)

    resposta_formatada = ""

    if similaridades[indice_mais_similar] > 0.1:
        manual = manuais[indice_mais_similar]
        imagens_relevantes = imagens.get(manual.id, [])

        # Formatar a resposta com as imagens
        imagens_html = "".join(
            f"<img src='{img_url}' >"
            for img_url in imagens_relevantes
        )

        resposta_formatada = (
            f"Para a sua pergunta: {pergunta}<br><br>"
            f"Aqui estão informações relevantes:<br>"
            f"<p><strong>{conteudos_resumidos[indice_mais_similar]}</strong></p>"
            f"{imagens_html}<br>"
            f"Caso queria ver o Manual completo, leia mais aqui: "
            f"<a href='{manual.link}' target='_blank'>{manual.link}</a>"
        )
    else:
        resposta_formatada = "Desculpe, não encontrei uma resposta adequada."

    # Retorna a resposta formatada
    return {
        "resposta": mark_safe(resposta_formatada),
        "sugerir_mais": "Você gostaria de saber sobre mais alguma coisa?"
    }




def buscar_manual(request, manual_id):
    manual = Manual.objects.get(id=manual_id)
    return JsonResponse({
        'titulo': manual.titulo,
        'conteudo': manual.conteudo,
    })