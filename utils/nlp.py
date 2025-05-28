"""
Utilitários para processamento de linguagem natural
"""
from typing import List, Dict, Any, Optional
from fuzzywuzzy import fuzz
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

# Download recursos necessários do NLTK
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

def normalize_text(text: str) -> str:
    """Normaliza o texto removendo acentos e convertendo para minúsculas"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def extract_keywords(text: str) -> List[str]:
    """Extrai palavras-chave do texto"""
    stop_words = set(stopwords.words('portuguese'))
    words = word_tokenize(normalize_text(text))
    return [word for word in words if word not in stop_words]

def find_best_match(query: str, options: List[str], threshold: int = 80) -> Optional[str]:
    """Encontra a melhor correspondência para uma query em uma lista de opções"""
    best_ratio = 0
    best_match = None
    
    query = normalize_text(query)
    for option in options:
        ratio = fuzz.partial_ratio(query, normalize_text(option))
        if ratio > best_ratio and ratio >= threshold:
            best_ratio = ratio
            best_match = option
    
    return best_match

def classify_question(text: str) -> Dict[str, Any]:
    """Classifica o tipo de pergunta e extrai informações relevantes"""
    text = text.lower()
    
    # Padrões de classificação
    patterns = {
        'localizacao': r'(onde|localiza|encontr|acha).*(sala|laboratorio|predio|setor)',
        'horario': r'(que horas|horario|quando|abre|fecha)',
        'curso': r'(curso|formacao|aprend|estud)',
        'inscricao': r'(inscricao|matricula|cadastr)',
        'valor': r'(quanto|preco|valor|custo)',
        'contato': r'(telefone|email|contato|falar)',
        'documento': r'(documento|certific|diplom)',
    }
    
    # Classifica a pergunta
    classificacao = {}
    for tipo, pattern in patterns.items():
        if re.search(pattern, text):
            classificacao[tipo] = True
    
    # Extrai entidades relevantes
    keywords = extract_keywords(text)
    
    return {
        'tipos': list(classificacao.keys()),
        'keywords': keywords,
        'texto_original': text
    }

def generate_natural_response(template: str, data: Dict[str, Any]) -> str:
    """Gera uma resposta natural baseada em um template e dados"""
    # Lista de conectores para variar as respostas
    conectores = {
        'localizacao': [
            'fica localizado em',
            'está localizado em',
            'você encontra em',
            'pode ser encontrado em'
        ],
        'horario': [
            'funciona de',
            'está aberto de',
            'atende de',
            'tem expediente de'
        ],
        'valor': [
            'custa',
            'tem o valor de',
            'está custando',
            'tem o investimento de'
        ]
    }
    
    # Substitui marcadores no template
    response = template
    for key, value in data.items():
        if isinstance(value, list):
            value = ', '.join(value)
        response = response.replace(f'{{{key}}}', str(value))
    
    return response 