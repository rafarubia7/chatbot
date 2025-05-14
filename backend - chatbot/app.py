from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import requests
from requests.exceptions import RequestException
import re
import json
from info import (
    SENAI_SAO_CARLOS_INFO, 
    CURSOS, 
    PROCESSO_INSCRICAO, 
    INFRAESTRUTURA, 
    EMPRESAS_PARCEIRAS,
    PERGUNTAS_FREQUENTES, 
    DIFERENCIAIS, 
    EVENTOS, 
    CONTATOS
)

app = Flask(__name__)
CORS(app)
app.secret_key = 'segredo-seguro'  # Em produção, use uma chave secreta forte e variável de ambiente

# Configurações do LM Studio
LM_STUDIO_URL = "http://localhost:1234/v1/completions"
MODEL_NAME = "llama-3.1-tulu-3-8b" 

# Formatação da informação estruturada para o prompt do sistema
def format_sao_carlos_info():
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
    info_text += "\n[INFRAESTRUTURA]\n"
    info_text += f"Laboratórios: {', '.join(INFRAESTRUTURA['laboratorios'][:4])}, entre outros.\n"
    
    # Adicionar contatos específicos
    info_text += "\n[CONTATOS]\n"
    for depto, info in CONTATOS.items():
        info_text += f"{depto.capitalize()}: Tel: {info['telefone']}, Email: {info['email']}\n"

    # Adicionar diferenciais
    info_text += "\n[DIFERENCIAIS DA UNIDADE]\n"
    for diferencial in DIFERENCIAIS[:3]:
        info_text += f"- {diferencial}\n"

    return info_text

# Prompt de sistema detalhado com informações específicas sobre o SENAI São Carlos
base_senai_system_prompt = """ 
[O QUE É O SENAI SÃO CARLOS]
O SENAI São Carlos - Escola SENAI "Antônio Adolpho Lobbe" é uma unidade do SENAI (Serviço Nacional de Aprendizagem Industrial) 
localizada em São Carlos, SP. Fundada em 1958, é uma instituição de referência em educação profissional na região, 
especializada na formação de profissionais qualificados para a indústria local. A unidade atua principalmente nas 
áreas de mecânica, eletroeletrônica e tecnologia da informação, oferecendo cursos técnicos, de aprendizagem industrial 
e de qualificação profissional, além de serviços de consultoria tecnológica para empresas.

[INSTRUÇÕES IMPORTANTES]
Você é o Assistente Virtual exclusivo do SENAI São Carlos.
- Responda APENAS perguntas sobre o SENAI São Carlos e seus serviços específicos
- Enfatize sempre que você representa o SENAI SÃO CARLOS (não o SENAI nacional)
- Você possui todas as informações específicas sobre cursos, processos e contatos da unidade de São Carlos
- Utilize SEMPRE informações específicas de São Carlos em suas respostas
- Nunca inclua tags como <|end_of_text|> ou <|begin_of_text|>
- Formate as respostas de forma clara e natural
- Se não souber a resposta específica para o SENAI São Carlos, diga que vai consultar a equipe da unidade e retornará em breve
- Quando falar sobre cursos técnicos, sempre mencione APENAS os disponíveis em São Carlos
- Quando falar sobre localização ou contato, sempre use os dados específicos da unidade de São Carlos
- Se o usuário perguntar sobre outras unidades do SENAI, redirecione gentilmente para informações sobre a unidade de São Carlos
"""

# Adicionar informações específicas de São Carlos ao prompt do sistema
senai_system_prompt = base_senai_system_prompt + format_sao_carlos_info()

# Mensagem inicial
initial_message = "Olá! Sou o assistente virtual exclusivo do SENAI São Carlos - Escola SENAI 'Antônio Adolpho Lobbe'. Posso ajudar com informações sobre nossos cursos, inscrições, localização e serviços específicos da unidade de São Carlos. Como posso ajudar você hoje?"

# Histórico de conversa
conversation_history = f"Sistema: {senai_system_prompt}\nAssistente: {initial_message}\n"

def clean_response(text):
    """Remove tags indesejadas e formatação especial"""
    text = re.sub(r'<\|.*?\|>', '', text)  # Remove tags como <|end_of_text|>
    text = re.sub(r'byline', '', text)  # Remove 'byline'
    text = re.sub(r'\n+', '\n', text).strip()  # Remove linhas extras
    return text

def is_about_senai_sao_carlos(message):
    """Verifica se a mensagem está relacionada ao SENAI São Carlos"""
    forbidden_terms = ['<|end_of_text|>', '<|begin_of_text|>', 'byline']
    if any(term.lower() in message.lower() for term in forbidden_terms):
        return False
        
    # Primeiro verifica menções diretas a São Carlos
    sao_carlos_keywords = [
        'são carlos', 'sao carlos', 'antonio adolpho', 'antônio adolpho', 
        'adolpho lobbe', 'lobbe', 'vila prado'
    ]
    
    # Se menciona diretamente São Carlos, retorna verdadeiro
    if any(keyword.lower() in message.lower() for keyword in sao_carlos_keywords):
        return True
        
    # Palavras-chave gerais do SENAI
    senai_keywords = [
        'senai', 'curso', 'cursos', 'inscrição', 'inscrições', 
        'aprendizagem', 'técnico', 'tecnológico', 'unidade', 'ola', 'olá',
        'como vai', 'quem é vc', 'quero saber sobre', 'me diga mais sobre',
        'educação profissional', 'sistema s', 'cni', 'sesi', 'sobre', 'sim', 'quero'
        'formação', 'profissionalizante', 'escola', 'matricula', 'matrícula',
        'endereço', 'endereco', 'onde fica', 'contato', 'telefone', 'mecânica',
        'eletroeletrônica', 'desenvolvimento', 'sistemas', 'informática',
        'qualificação', 'quando', 'como', 'quanto', 'valor', 'preço', 'preco',
        'bolsa', 'desconto', 'certificado', 'diploma', 'estágio', 'mercado'
    ]
    
    return any(keyword.lower() in message.lower() for keyword in senai_keywords)

def get_specific_info(query):
    """Tenta buscar informações específicas com base na consulta do usuário"""
    query = query.lower()
    
    # Verifica se é uma pergunta sobre localização ou como chegar
    if any(termo in query for termo in ['onde fica', 'localização', 'localizacao', 'endereço', 'endereco', 'como chego', 'como chegar']):
        return f"""
        O SENAI São Carlos está localizado na {SENAI_SAO_CARLOS_INFO['endereco']}.
        
        Pontos de referência:
        - Próximo ao Terminal Rodoviário de São Carlos
        - Na região da Vila Prado
        - A aproximadamente 3 km do centro da cidade
        
        Você pode chegar utilizando as linhas de ônibus municipal que passam pela Vila Prado,
        ou de carro seguindo pela Avenida São Carlos em direção à saída para Ribeirão Preto,
        entrando à direita na região da Vila Prado.
        """
    
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
        infra_info += "Laboratórios:\n"
        for lab in INFRAESTRUTURA['laboratorios']:
            infra_info += f"- {lab}\n"
        
        infra_info += "\nInstalações:\n"
        for inst in INFRAESTRUTURA['instalacoes']:
            infra_info += f"- {inst}\n"
            
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            return render_template('login.html', error="Por favor, insira seu nome")
        
        session['username'] = username
        global conversation_history
        conversation_history = f"Sistema: {senai_system_prompt}\nAssistente: Olá {username}, sou o assistente virtual do SENAI São Carlos. Como posso te ajudar?\n"
        return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    username = session.get('username', 'Usuário')
    
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type deve ser application/json"}), 415
            
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Mensagem vazia"}), 400
        
        # Verificar se a pergunta é sobre o SENAI São Carlos
        if not is_about_senai_sao_carlos(user_message):
            return jsonify({
                "reply": f"Olá {username}, sou o assistente virtual exclusivo do SENAI São Carlos! Posso te ajudar com informações sobre nossos cursos, inscrições, localização e serviços. O que você gostaria de saber sobre nossa unidade?"
            })
        
        # Tentar recuperar informação específica
        specific_info = get_specific_info(user_message)
        if specific_info:
            # Adicionar a informação específica ao contexto da conversa
            additional_context = f"[INFORMAÇÃO ADICIONAL RELEVANTE SOBRE O SENAI SÃO CARLOS]\n{specific_info}\n\n"
            temp_prompt = senai_system_prompt + "\n" + additional_context
            temp_history = f"Sistema: {temp_prompt}\n"
            
            # Adicionar último contexto de conversa (últimas 5 trocas)
            lines = conversation_history.split('\n')
            if len(lines) > 10:
                temp_history += '\n'.join(lines[-10:])
            else:
                temp_history += '\n'.join(lines[1:])  # Pular o sistema original
        else:
            temp_history = conversation_history
        
        # Adicionar mensagem do usuário ao histórico
        temp_history += f"{username}: {user_message}\nAssistente: "
        
        # Limitar o tamanho do histórico
        if len(temp_history.split('\n')) > 30:
            lines = temp_history.split('\n')
            system_prompt_lines = senai_system_prompt.count('\n') + 2
            temp_history = '\n'.join(lines[:system_prompt_lines]) + '\n' + '\n'.join(lines[-25:])
        
        # Configurar a requisição para o LM Studio
        headers = {"Content-Type": "application/json"}
        payload = {
            "prompt": temp_history,
            "model": MODEL_NAME,
            "temperature": 0.7,
            "max_tokens": 1000,
            "stop": [f"\n{username}:", "\nSistema:", "<|end_of_text|>", "<|begin_of_text|>"]
        }
        
        response = requests.post(LM_STUDIO_URL, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            response_data = response.json()
            if "choices" in response_data and len(response_data["choices"]) > 0:
                assistant_reply = clean_response(response_data["choices"][0]["text"].strip())
                
                # Verificar novamente se a resposta está relacionada ao SENAI São Carlos
                if not is_about_senai_sao_carlos(assistant_reply) or len(assistant_reply) < 10:
                    assistant_reply = f"Olá {username}, como assistente do SENAI São Carlos, posso te ajudar com informações sobre nossos cursos técnicos, processos de inscrição ou detalhes sobre nossa unidade na cidade de São Carlos. Como posso te ajudar hoje?"
                
                # Garantir que a resposta mencione São Carlos se ainda não mencionou
                if 'são carlos' not in assistant_reply.lower() and 'sao carlos' not in assistant_reply.lower():
                    assistant_reply += "\n\nEsta informação é específica para o SENAI São Carlos - Escola SENAI 'Antônio Adolpho Lobbe'."
                
                # Adicionar ao histórico de conversa permanente
                conversation_history += f"{username}: {user_message}\nAssistente: {assistant_reply}\n"
                
                # Limitar o histórico permanente
                if len(conversation_history.split('\n')) > 40:
                    lines = conversation_history.split('\n')
                    system_prompt_lines = senai_system_prompt.count('\n') + 2
                    conversation_history = '\n'.join(lines[:system_prompt_lines]) + '\n' + '\n'.join(lines[-30:])
                
                return jsonify({"reply": assistant_reply})
            
            return jsonify({"error": "Resposta inesperada do LM Studio"}), 500
        else:
            return jsonify({
                "error": f"Erro na API (HTTP {response.status_code})",
                "details": response.text[:200]  # Limita o tamanho do detalhe do erro
            }), 500
            
    except RequestException as e:
        return jsonify({
            "error": "Erro de conexão com o LM Studio. Verifique se o serviço está rodando.",
            "details": str(e)
        }), 503
    except Exception as e:
        return jsonify({
            "error": "Erro interno no servidor",
            "details": str(e)
    }), 500

@app.route('/reset', methods=['POST'])
def reset_conversation():
    global conversation_history
    username = session.get('username', 'Usuário')
    conversation_history = f"Sistema: {senai_system_prompt}\nAssistente: Olá {username}, sou o assistente virtual do SENAI São Carlos. Como posso te ajudar?\n"
    return jsonify({"status": "success", "message": "Conversa reiniciada"})

@app.route('/available-courses', methods=['GET'])
def available_courses():
    """Endpoint para obter todos os cursos disponíveis"""
    return jsonify(CURSOS)

@app.route('/senai-info', methods=['GET'])
def senai_info():
    """Endpoint para obter informações gerais sobre a unidade"""
    return jsonify(SENAI_SAO_CARLOS_INFO)

@app.route('/contacts', methods=['GET'])
def contacts():
    """Endpoint para obter informações de contato"""
    return jsonify(CONTATOS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)