"""
Gerenciador de chat e processamento de mensagens
"""
import re
import requests
from datetime import datetime
from typing import List, Dict, Optional

from config import LM_STUDIO_URL, MODEL_NAME, REQUEST_TIMEOUT
from info.responses import RESPOSTAS_PADRAO
from info import (
    get_specific_info,
    format_sao_carlos_info
)

# Prompt base do sistema
BASE_SYSTEM_PROMPT = """ 
[O QUE É O SENAI SÃO CARLOS]
O SENAI São Carlos - Escola SENAI "Antônio Adolpho Lobbe" é uma unidade do SENAI 
localizada em São Carlos, SP. Fundada em 1958, é uma instituição de referência em 
educação profissional na região, especializada na formação de profissionais 
qualificados para a indústria local.

[INSTRUÇÕES IMPORTANTES]
Você é o Assistente Virtual exclusivo do SENAI São Carlos.
- Responda APENAS perguntas sobre o SENAI São Carlos e seus serviços específicos
- Enfatize sempre que você representa o SENAI SÃO CARLOS (não o SENAI nacional)
- Utilize SEMPRE informações específicas de São Carlos em suas respostas
- Formate as respostas de forma clara e natural
"""

# Adicionar informações específicas ao prompt
SYSTEM_PROMPT = BASE_SYSTEM_PROMPT + format_sao_carlos_info()

def clean_response(text: str) -> str:
    """Remove tags indesejadas e formatação especial"""
    text = re.sub(r'<\|.*?\|>', '', text)  # Remove tags como <|end_of_text|>
    text = re.sub(r'byline', '', text)  # Remove 'byline'
    text = re.sub(r'\n+', '\n', text).strip()  # Remove linhas extras
    return text

def is_about_senai_sao_carlos(message: str) -> bool:
    """Verifica se a mensagem está relacionada ao SENAI São Carlos"""
    forbidden_terms = ['<|end_of_text|>', '<|begin_of_text|>', 'byline']
    if any(term.lower() in message.lower() for term in forbidden_terms):
        return False
        
    # Primeiro verifica menções diretas a São Carlos
    sao_carlos_keywords = [
        'são carlos', 'sao carlos', 'antonio adolpho', 'antônio adolpho', 
        'adolpho lobbe', 'lobbe', 'vila prado'
    ]
    
    if any(keyword.lower() in message.lower() for keyword in sao_carlos_keywords):
        return True
        
    # Palavras-chave gerais do SENAI
    senai_keywords = [
        'senai', 'curso', 'inscrição', 'aprendizagem', 'técnico', 'tecnológico',
        'unidade', 'ola', 'olá', 'como vai', 'quem é vc', 'sobre', 'mais',
        'educação profissional', 'sistemas', 'formação', 'profissionalizante',
        'escola', 'matricula', 'endereço', 'onde fica', 'contato', 'telefone',
        'mecânica', 'eletroeletrônica', 'desenvolvimento', 'informática',
        'qualificação', 'quando', 'como', 'quanto', 'valor', 'preço',
        'bolsa', 'desconto', 'certificado', 'diploma', 'estágio', 'mercado'
    ]
    
    return any(keyword.lower() in message.lower() for keyword in senai_keywords)

def format_chat_history_for_prompt(chat_history: List[Dict]) -> str:
    """Formata o histórico do chat para o prompt do LM Studio"""
    prompt = f"Sistema: {SYSTEM_PROMPT}\n"
    
    for message in chat_history[-5:]:  # Usar apenas as últimas 5 mensagens
        sender = "Usuário" if message['sender'] == "user" else "Assistente"
        prompt += f"{sender}: {message['text']}\n"
    
    prompt += "Assistente: "
    return prompt

def process_message(message: str, chat_history: List[Dict]) -> str:
    """Processa a mensagem e retorna uma resposta"""
    try:
        # Verificar se a pergunta é sobre o SENAI São Carlos
        if not is_about_senai_sao_carlos(message):
            return RESPOSTAS_PADRAO["fora_escopo"]
        
        # Tentar recuperar informação específica
        specific_info = get_specific_info(message)
        if specific_info:
            return specific_info
            
        # Se não houver informação específica, usar o LM Studio
        try:
            # Preparar o histórico para o prompt
            prompt = format_chat_history_for_prompt(chat_history)
            
            payload = {
                "model": MODEL_NAME,
                "prompt": prompt,
                "max_tokens": 500,
                "temperature": 0.7,
                "stop": ["Usuário:", "Sistema:"]
            }
            
            response = requests.post(
                LM_STUDIO_URL,
                json=payload,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('choices', [{}])[0].get('text', '')
                return clean_response(ai_response)
            else:
                return RESPOSTAS_PADRAO["erro_tecnico"]
                
        except requests.exceptions.RequestException:
            return RESPOSTAS_PADRAO["erro_conexao"]
            
    except Exception as e:
        print(f"Erro ao processar mensagem: {str(e)}")
        return RESPOSTAS_PADRAO["erro_geral"] 