from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
import numpy as np  # type: ignore
from chat.utils import gerar_palavras_chave

def responder_pergunta(pergunta, manuais):
    # Gere as palavras-chave da pergunta
    palavras_chave_pergunta = gerar_palavras_chave(pergunta)

    # Obtenha os conteúdos dos manuais e suas palavras-chave
    conteudos = [manual.conteudo for manual in manuais]
    palavras_chave_manuais = [manual.palavras_chave for manual in manuais]

    # Combine a pergunta e os manuais em uma lista
    documentos = [palavras_chave_pergunta] + palavras_chave_manuais

    # Crie o vetor TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documentos)

    # Calcule a similaridade da pergunta com os manuais
    similaridades = X[0].dot(X[1:].T).toarray().flatten()  # Melhorar a legibilidade

    # Encontre o índice do manual mais similar
    indice_mais_similar = np.argmax(similaridades)

    # Se a similaridade for suficientemente alta, retorne a resposta
    if similaridades[indice_mais_similar] > 0.1:  # Ajuste o threshold se necessário
        manual = manuais[indice_mais_similar]
        resposta_formatada = (
            f"Para sua pergunta sobre '{pergunta}', aqui estão as informações relevantes:\n\n"
            f"{manual.conteudo.replace('\n', '\n\n')}\n\n"  # Duas quebras de linha para separar parágrafos
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
