"""
Módulo de informações do SENAI São Carlos
"""
from .base_info import SENAI_SAO_CARLOS_INFO, CONTATOS
from .cursos import CURSOS
from .salas import SALAS
from .processos import PROCESSO_INSCRICAO, PERGUNTAS_FREQUENTES
from .institucional import (
    EMPRESAS_PARCEIRAS,
    EVENTOS,
    DIFERENCIAIS
)
from .search import get_specific_info

def format_sao_carlos_info() -> str:
    """Formata as informações do SENAI São Carlos para inclusão no prompt do sistema"""
    info_text = f"""
[INFORMAÇÕES SOBRE O SENAI SÃO CARLOS]
Nome: {SENAI_SAO_CARLOS_INFO['nome_completo']}
Endereço: {SENAI_SAO_CARLOS_INFO['endereco']}
Telefone: {SENAI_SAO_CARLOS_INFO['telefone']}
Email: {SENAI_SAO_CARLOS_INFO['email']}
Site: {SENAI_SAO_CARLOS_INFO['site']}
Horário de funcionamento: {SENAI_SAO_CARLOS_INFO['horario_funcionamento']}
"""
    # Adicionar descrição
    info_text += f"\nSobre a unidade: {SENAI_SAO_CARLOS_INFO['sobre'].strip()}\n"

    # Adicionar cursos técnicos
    info_text += "\n[CURSOS TÉCNICOS OFERECIDOS]\n"
    for curso in CURSOS['tecnico']:
        info_text += f"- {curso['nome']}: {curso['descricao']} Duração: {curso['duracao']}. Modalidades: {', '.join(curso['modalidades'])}. Horários: {', '.join(curso['horarios'])}.\n"

    # Adicionar cursos de aprendizagem industrial
    info_text += "\n[CURSOS DE APRENDIZAGEM INDUSTRIAL]\n"
    for curso in CURSOS['aprendizagem']:
        info_text += f"- {curso['nome']}: {curso['descricao']} Duração: {curso['duracao']}. Idade: {curso['idade']}.\n"

    # Adicionar cursos de qualificação
    info_text += "\n[CURSOS DE QUALIFICAÇÃO PROFISSIONAL]\n"
    for curso in CURSOS['qualificacao'][:2]:  # Limitar para manter o prompt compacto
        info_text += f"- {curso['nome']}: {curso['descricao']} Duração: {curso['duracao']}.\n"

    # Adicionar informações sobre inscrição
    info_text += "\n[PROCESSO DE INSCRIÇÃO]\n"
    for tipo, processo in PROCESSO_INSCRICAO.items():
        linha = processo.strip().split('\n')[0]
        info_text += f"Para cursos {tipo}: {linha}\n"

    # Adicionar informações sobre infraestrutura
    info_text += "\n[INFRAESTRUTURA E LABORATÓRIOS]\n"
    for key, sala in SALAS.items():
        if sala.tipo == "laboratorio":
            info_text += f"- {sala.nome}: {sala.descricao}\n"
            info_text += f"  Localização: Prédio {sala.localizacao.predio}, {sala.localizacao.andar}, Sala {sala.localizacao.sala}\n"
    
    # Adicionar contatos específicos
    info_text += "\n[CONTATOS]\n"
    for depto, info in CONTATOS.items():
        info_text += f"{depto.capitalize()}: Tel: {info['telefone']}, Email: {info['email']}\n"

    # Adicionar diferenciais por categoria
    info_text += "\n[DIFERENCIAIS DA UNIDADE]\n"
    for categoria, lista in DIFERENCIAIS.items():
        info_text += f"\n{categoria.capitalize()}:\n"
        for item in lista[:2]:  # Limitando a 2 itens por categoria para manter o prompt compacto
            info_text += f"- {item}\n"

    return info_text

__all__ = [
    'SENAI_SAO_CARLOS_INFO',
    'CURSOS',
    'SALAS',
    'PROCESSO_INSCRICAO',
    'CONTATOS',
    'PERGUNTAS_FREQUENTES',
    'EMPRESAS_PARCEIRAS',
    'EVENTOS',
    'DIFERENCIAIS',
    'get_specific_info',
    'format_sao_carlos_info'
] 