"""
Funções de busca de informações específicas
"""
from typing import Optional

from .base_info import SENAI_SAO_CARLOS_INFO, CONTATOS
from .cursos import CURSOS
from .salas import SALAS
from .processos import PROCESSO_INSCRICAO, PERGUNTAS_FREQUENTES
from .institucional import (
    EMPRESAS_PARCEIRAS,
    EVENTOS,
    DIFERENCIAIS
)

def get_specific_info(query: str) -> Optional[str]:
    """Tenta buscar informações específicas com base na consulta do usuário"""
    query = query.lower()
    
    # Busca por informações sobre localização e navegação
    if any(palavra in query for palavra in ['onde fica', 'localização', 'localizacao', 'como chegar', 'como chego', 'onde está', 'onde esta', 'caminho', 'sabe chegar']):
        # Palavras-chave para identificar locais
        local_keywords = {
            'refeitorio': ['refeitório', 'refeitorio', 'cantina', 'comida', 'almoço', 'almoco', 'café', 'cafe', 'lanche'],
            'biblioteca': ['biblioteca', 'livros', 'estudar', 'leitura'],
            'lab_mecanica': ['laboratório de mecânica', 'lab mecânica', 'oficina mecânica', 'mecânica'],
            'secretaria': ['secretaria', 'atendimento', 'documentos', 'matrícula', 'matricula']
        }
        
        # Procurar por local específico na pergunta
        for sala_id, keywords in local_keywords.items():
            if any(keyword in query for keyword in keywords):
                sala = SALAS[sala_id]
                resposta = f"""Para chegar ao {sala.nome}:

"""
                # Adicionar instruções de navegação
                for instrucao in sala.navegacao.instrucoes:
                    resposta += f"- {instrucao}\n"
                
                resposta += f"\nLocalização: {sala.localizacao.predio}, {sala.localizacao.andar}"
                if sala.localizacao.sala:
                    resposta += f", Sala {sala.localizacao.sala}"
                
                if sala.horario_funcionamento:
                    resposta += f"\n\nHorário de funcionamento: {sala.horario_funcionamento}"
                
                if sala.navegacao.dicas_adicionais:
                    resposta += f"\n\nDica adicional: {sala.navegacao.dicas_adicionais}"
                
                resposta += "\n\nSe precisar de mais ajuda para encontrar, pode perguntar a qualquer funcionário no caminho! 😊"
                return resposta
    
    # Busca por cursos específicos
    if any(termo in query for termo in ['curso', 'formação', 'aprender', 'estudar']):
        for categoria, lista_cursos in CURSOS.items():
            for curso in lista_cursos:
                if curso['nome'].lower() in query:
                    curso_info = f"""
                    {curso['nome']} - SENAI São Carlos
                    
                    Descrição: {curso['descricao']}
                    """
                    
                    # Adicionar informações específicas dependendo do tipo de curso
                    if categoria == 'tecnico' or categoria == 'qualificacao':
                        curso_info += f"""
                        Duração: {curso['duracao']}
                        Modalidades: {', '.join(curso['modalidades'])}
                        Horários disponíveis: {', '.join(curso['horarios'])}
                        Requisitos: {curso['requisitos']}
                        
                        Para mais informações sobre valores e próximas turmas, 
                        entre em contato pelo telefone {CONTATOS['secretaria']['telefone']}
                        ou email {CONTATOS['secretaria']['email']}.
                        """
                    elif categoria == 'aprendizagem':
                        curso_info += f"""
                        Duração: {curso['duracao']}
                        Faixa etária: {curso['idade']}
                        Requisitos: {curso['requisitos']}
                        
                        Os cursos de aprendizagem industrial são gratuitos e realizados
                        em parceria com empresas. Para mais informações sobre o processo
                        seletivo, entre em contato pelo telefone {CONTATOS['secretaria']['telefone']}
                        ou email {CONTATOS['secretaria']['email']}.
                        """
                    
                    return curso_info
        
        # Se não encontrou um curso específico, lista os principais cursos por categoria
        if 'técnico' in query or 'tecnico' in query:
            cursos_info = "Cursos Técnicos disponíveis no SENAI São Carlos:\n\n"
            for curso in CURSOS['tecnico']:
                cursos_info += f"- {curso['nome']}: {curso['duracao']}, {', '.join(curso['horarios'])}\n"
            return cursos_info
            
        elif 'aprendizagem' in query:
            cursos_info = "Cursos de Aprendizagem Industrial disponíveis no SENAI São Carlos:\n\n"
            for curso in CURSOS['aprendizagem']:
                cursos_info += f"- {curso['nome']}: {curso['duracao']}, {curso['idade']}\n"
            return cursos_info
            
        elif 'qualificação' in query or 'qualificacao' in query or 'profissional' in query:
            cursos_info = "Cursos de Qualificação Profissional disponíveis no SENAI São Carlos:\n\n"
            for curso in CURSOS['qualificacao']:
                cursos_info += f"- {curso['nome']}: {curso['duracao']}, {', '.join(curso['modalidades'])}\n"
            return cursos_info
            
        elif 'curta' in query or 'rápido' in query or 'rapido' in query:
            cursos_info = "Cursos de Curta Duração disponíveis no SENAI São Carlos:\n\n"
            for curso in CURSOS['curta_duracao']:
                cursos_info += f"- {curso['nome']}: {curso['duracao']}, {', '.join(curso['modalidades'])}\n"
            return cursos_info
    
    # Busca por informações de contato
    if any(palavra in query for palavra in ['contato', 'telefone', 'email', 'e-mail', 'falar', 'comunicar']):
        if 'secretaria' in query:
            contato_info = f"""
            Contatos da Secretaria do SENAI São Carlos:
            Telefone: {CONTATOS['secretaria']['telefone']}
            Email: {CONTATOS['secretaria']['email']}
            Horário de atendimento: {CONTATOS['secretaria']['horario']}
            """
            return contato_info
        elif 'coordenação' in query or 'coordenacao' in query or 'coordenador' in query:
            contato_info = f"""
            Contatos da Coordenação de Cursos do SENAI São Carlos:
            Telefone: {CONTATOS['coordenacao_cursos']['telefone']}
            Email: {CONTATOS['coordenacao_cursos']['email']}
            Horário de atendimento: {CONTATOS['coordenacao_cursos']['horario']}
            """
            return contato_info
        elif 'empresa' in query or 'parceria' in query:
            contato_info = f"""
            Contatos do Departamento de Atendimento a Empresas do SENAI São Carlos:
            Telefone: {CONTATOS['atendimento_empresas']['telefone']}
            Email: {CONTATOS['atendimento_empresas']['email']}
            Horário de atendimento: {CONTATOS['atendimento_empresas']['horario']}
            """
            return contato_info
        else:
            contato_info = f"""
            Contatos principais do SENAI São Carlos:
            Endereço: {SENAI_SAO_CARLOS_INFO['endereco']}
            Telefone geral: {SENAI_SAO_CARLOS_INFO['telefone']}
            Email: {SENAI_SAO_CARLOS_INFO['email']}
            Site: {SENAI_SAO_CARLOS_INFO['site']}
            Horário de funcionamento: {SENAI_SAO_CARLOS_INFO['horario_funcionamento']}
            """
            return contato_info
    
    # Busca por informações sobre inscrição
    if any(palavra in query for palavra in ['inscrição', 'inscricao', 'matricula', 'matrícula', 'como fazer', 'como se inscrever']):
        if 'técnico' in query or 'tecnico' in query:
            return f"Processo de inscrição para cursos técnicos no SENAI São Carlos:\n\n{PROCESSO_INSCRICAO['tecnicos']}"
        elif 'aprendizagem' in query:
            return f"Processo de inscrição para cursos de aprendizagem industrial no SENAI São Carlos:\n\n{PROCESSO_INSCRICAO['aprendizagem']}"
        elif 'qualificação' in query or 'qualificacao' in query or 'profissional' in query:
            return f"Processo de inscrição para cursos de qualificação profissional no SENAI São Carlos:\n\n{PROCESSO_INSCRICAO['qualificacao']}"
        else:
            linha_tecnicos = PROCESSO_INSCRICAO['tecnicos'].strip().split('\n')[0]
            linha_aprendizagem = PROCESSO_INSCRICAO['aprendizagem'].strip().split('\n')[0]
            linha_qualificacao = PROCESSO_INSCRICAO['qualificacao'].strip().split('\n')[0]

        return "Processos de inscrição no SENAI São Carlos:\n\n" + \
            f"Para cursos técnicos: {linha_tecnicos}\n\n" + \
            f"Para cursos de aprendizagem: {linha_aprendizagem}\n\n" + \
            f"Para cursos de qualificação: {linha_qualificacao}"

    # Busca por informações sobre laboratórios e infraestrutura
    if any(palavra in query for palavra in ['laboratório', 'laboratorio', 'infraestrutura', 'instalações', 'instalacoes', 'equipamentos']):
        infra_info = "Laboratórios e Infraestrutura do SENAI São Carlos:\n\n"
        
        # Listar laboratórios com localização
        infra_info += "Laboratórios:\n"
        for key, sala in SALAS.items():
            if sala.tipo == "laboratorio":
                infra_info += f"- {sala.nome}: {sala.descricao}\n"
                infra_info += f"  Localização: Prédio {sala.localizacao.predio}, {sala.localizacao.andar}, Sala {sala.localizacao.sala}\n"
        
        # Listar outras instalações
        infra_info += "\nOutras Instalações:\n"
        for key, sala in SALAS.items():
            if sala.tipo == "instalacao":
                infra_info += f"- {sala.nome}: {sala.descricao}\n"
                infra_info += f"  Localização: Prédio {sala.localizacao.predio}, {sala.localizacao.andar}\n"
            
        return infra_info
    
    # Busca por informações sobre empresas parceiras
    if any(palavra in query for palavra in ['parceria', 'parcerias', 'empresa', 'empresas', 'parceiros']):
        parceiros_info = "Principais empresas parceiras do SENAI São Carlos:\n\n"
        for empresa in EMPRESAS_PARCEIRAS:
            parceiros_info += f"- {empresa}\n"
        
        parceiros_info += "\nO SENAI São Carlos mantém parcerias com diversas empresas da região para estágios, " \
                         "contratações e cursos de aprendizagem industrial."
        return parceiros_info
    
    # Busca por informações sobre bolsas e descontos
    if any(palavra in query for palavra in ['bolsa', 'bolsas', 'desconto', 'descontos', 'gratuito', 'preço', 'preco', 'valor']):
        return PERGUNTAS_FREQUENTES["Como obter bolsas de estudo?"]
    
    # Busca por informações sobre estágios
    if any(palavra in query for palavra in ['estágio', 'estagio', 'emprego', 'trabalho', 'contratar', 'contratação', 'contratacao']):
        return PERGUNTAS_FREQUENTES["O SENAI oferece estágios?"]
    
    # Busca por informações sobre certificados
    if any(palavra in query for palavra in ['certificado', 'certificados', 'diploma', 'comprovante']):
        return PERGUNTAS_FREQUENTES["Como obter certificados de cursos concluídos?"]
    
    # Busca por informações gerais sobre a unidade
    if any(palavra in query for palavra in ['sobre', 'história', 'historia', 'unidade', 'escola']):
        return SENAI_SAO_CARLOS_INFO['sobre']
    
    # Busca por diferenciais da unidade
    if any(palavra in query for palavra in ['diferencial', 'diferenciais', 'vantagem', 'vantagens', 'especial']):
        dif_info = "Diferenciais do SENAI São Carlos:\n\n"
        for dif in DIFERENCIAIS:
            dif_info += f"- {dif}\n"
        return dif_info
    
    # Busca por eventos
    if any(palavra in query for palavra in ['evento', 'eventos', 'feira', 'workshop', 'palestra', 'palestras', 'encontro']):
        eventos_info = "Principais eventos realizados pelo SENAI São Carlos:\n\n"
        for evento in EVENTOS:
            eventos_info += f"- {evento}\n"
        return eventos_info
    
    # Se não encontrou nada específico, retorna None
    return None 