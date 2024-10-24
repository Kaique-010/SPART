import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
from gensim.models import Word2Vec  # type: ignore
import numpy as np  # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
import os



def extrair_links_manuais(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erro ao acessar a URL: {response.status_code} - URL: {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = [link['href'] for link in soup.find_all('a', href=True)]
    return links



def extrair_conteudo(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        conteudo = soup.get_text(separator=' ', strip=True)
        return conteudo
    except Exception as e:
        print(f"Erro ao acessar o link {link}: {e}")
        return None



def gerar_palavras_chave(texto):
    stop_words = ['e', 'a', 'o', 'que', 'de', 'do', 'da', 'em', 'para', 'com', 'um', 'uma', 'os', 'as', 'na', 'no']
    
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    X = vectorizer.fit_transform([texto])
    
    feature_array = vectorizer.get_feature_names_out()
    tfidf_sorting = X.toarray().flatten().argsort()[::-1]
    
    palavras_chave = feature_array[tfidf_sorting][:10]  
    return ', '.join(palavras_chave)



def treinar_modelo_word2vec(sentencas):
    """
    Treina um modelo Word2Vec com uma lista de sentenças.
    
    :param sentencas: List of sentences (list of list of words)
    :return: modelo Word2Vec treinado
    """
    modelo = Word2Vec(sentencas, vector_size=100, window=5, min_count=1, workers=4)
    return modelo


