from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
import numpy as np  # type: ignore
from chat.utils import gerar_palavras_chave
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer



def resumir_texto(texto):
    parser = PlaintextParser.from_string(texto, Tokenizer("portuguese"))
    summarizer = LsaSummarizer()
    resumo = summarizer(parser.document, 10)  

    return ' '.join(str(frase) for frase in resumo)

def responder_pergunta(pergunta, manuais):
    palavras_chave_pergunta = gerar_palavras_chave(pergunta)

   
    conteudos_resumidos = [resumir_texto(manual.conteudo) for manual in manuais]
    palavras_chave_manuais = [manual.palavras_chave for manual in manuais]

   
    documentos = [palavras_chave_pergunta] + palavras_chave_manuais

    # Crie o vetor TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documentos)

    # Calcule a similaridade da pergunta com os manuais
    similaridades = np.dot(X[0], X[1:].T).toarray().flatten()

    # Encontre o índice do manual mais similar
    indice_mais_similar = np.argmax(similaridades)

    # Se a similaridade for suficientemente alta, retorne a resposta
    if similaridades[indice_mais_similar] > 0.1:  # Ajuste o threshold se necessário
        manual = manuais[indice_mais_similar]
        resposta_formatada = (
            f"Para sua pergunta sobre '{pergunta}', aqui estão as informações relevantes:\n\n"
            f"{conteudos_resumidos[indice_mais_similar]}\n\n"  # Use o resumo aqui
            f"[Leia mais aqui]({manual.link})"
        )
        return {
            "resposta": resposta_formatada,
            "sugerir_mais": "Você gostaria de saber sobre mais alguma coisa?"
        }

    return {
        "resposta": "Desculpe, não consegui encontrar a informação que você precisa.",
        "sugerir_mais": "Você gostaria de tentar outra pergunta?"
    }