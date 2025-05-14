"""
Arquivo de informações específicas sobre o SENAI de São Carlos para uso no chatbot.
Contém dados estruturados sobre cursos, localização, contatos e demais informações
relevantes sobre a unidade do SENAI em São Carlos.
"""

# Informações gerais da unidade
SENAI_SAO_CARLOS_INFO = {
    "nome_completo": "SENAI São Carlos - Escola SENAI 'Antônio Adolpho Lobbe'",
    "endereco": "Rua Cândido Padim, 25 - Vila Prado, São Carlos - SP, 13574-320",
    "telefone": "(16) 3373-9900",
    "email": "saocarlos@sp.senai.br",
    "site": "https://saocarlos.sp.senai.br/",
    "horario_funcionamento": "Segunda a Sexta-feira, das 8h às 21h",
    "diretor": "Carlos Alberto Vieira",
    "ano_fundacao": "1958",
    "sobre": """
    A Escola SENAI "Antônio Adolpho Lobbe" em São Carlos é uma instituição de referência 
    em educação profissional na região, atuando há mais de 60 anos na formação de 
    profissionais qualificados para a indústria. A unidade oferece diversos cursos 
    técnicos, de aprendizagem industrial e de qualificação profissional, além de 
    serviços de consultoria tecnológica e laboratorial para empresas locais.
    """
}

# Cursos oferecidos
CURSOS = {
    "tecnico": [
        {
            "nome": "Técnico em Mecânica",
            "duracao": "1 ano e meio (3 semestres)",
            "modalidades": ["Presencial"],
            "horarios": ["Manhã", "Noite"],
            "requisitos": "Estar cursando ou ter concluído o 2º ano do Ensino Médio",
            "valor": "Consultar valores atualizados no site ou por telefone",
            "descricao": "Forma profissionais para atuar no planejamento, controle e execução de processos de fabricação mecânica."
        },
        {
            "nome": "Técnico em Eletroeletrônica",
            "duracao": "1 ano e meio (3 semestres)",
            "modalidades": ["Presencial"],
            "horarios": ["Manhã", "Noite"],
            "requisitos": "Estar cursando ou ter concluído o 2º ano do Ensino Médio",
            "valor": "Consultar valores atualizados no site ou por telefone",
            "descricao": "Forma profissionais para desenvolver e executar projetos de instalações elétricas e eletrônicas."
        },
        {
            "nome": "Técnico em Desenvolvimento de Sistemas",
            "duracao": "1 ano e meio (3 semestres)",
            "modalidades": ["Presencial", "Semipresencial"],
            "horarios": ["Manhã", "Noite"],
            "requisitos": "Estar cursando ou ter concluído o 2º ano do Ensino Médio",
            "valor": "Consultar valores atualizados no site ou por telefone",
            "descricao": "Forma profissionais para desenvolver e implementar sistemas de informação, websites e aplicativos móveis."
        },
    ],
    "aprendizagem": [
        {
            "nome": "Aprendizagem Industrial em Mecânica",
            "duracao": "1 ano",
            "idade": "De 14 a 22 anos",
            "requisitos": "Estar cursando ou ter concluído o Ensino Médio",
            "descricao": "Curso gratuito em parceria com empresas, onde o jovem recebe formação teórica no SENAI e prática na empresa."
        },
        {
            "nome": "Aprendizagem Industrial em Eletroeletrônica",
            "duracao": "1 ano",
            "idade": "De 14 a 22 anos",
            "requisitos": "Estar cursando ou ter concluído o Ensino Médio",
            "descricao": "Curso gratuito em parceria com empresas, onde o jovem recebe formação teórica no SENAI e prática na empresa."
        },
    ],
    "qualificacao": [
        {
            "nome": "Eletricista Instalador",
            "duracao": "160 horas",
            "modalidades": ["Presencial"],
            "horarios": ["Noite", "Finais de semana"],
            "requisitos": "Ensino Fundamental completo e idade mínima de 18 anos",
            "valor": "Consultar valores atualizados no site ou por telefone",
            "descricao": "Capacita profissionais para realizar instalações elétricas residenciais e prediais."
        },
        {
            "nome": "Mecânico de Manutenção Industrial",
            "duracao": "160 horas",
            "modalidades": ["Presencial"],
            "horarios": ["Noite", "Finais de semana"],
            "requisitos": "Ensino Fundamental completo",
            "valor": "Consultar valores atualizados no site ou por telefone",
            "descricao": "Capacita profissionais para atuar na manutenção de máquinas e equipamentos industriais."
        },
        {
            "nome": "Programação de Sistemas",
            "duracao": "160 horas",
            "modalidades": ["Presencial", "EAD"],
            "horarios": ["Noite", "Finais de semana"],
            "requisitos": "Ensino Médio completo",
            "valor": "Consultar valores atualizados no site ou por telefone",
            "descricao": "Capacita profissionais para desenvolver software utilizando linguagens de programação modernas."
        },
    ],
    "curta_duracao": [
        {
            "nome": "Excel Avançado",
            "duracao": "40 horas",
            "modalidades": ["Presencial", "EAD"],
            "horarios": ["Noite", "Finais de semana"],
            "requisitos": "Conhecimentos básicos de informática",
            "valor": "Consultar valores atualizados no site ou por telefone",
            "descricao": "Curso para aprimorar conhecimentos em Excel, incluindo funções avançadas, macros e VBA."
        },
        {
            "nome": "Desenho Técnico Mecânico",
            "duracao": "40 horas",
            "modalidades": ["Presencial"],
            "horarios": ["Noite", "Finais de semana"],
            "requisitos": "Ensino Fundamental completo",
            "valor": "Consultar valores atualizados no site ou por telefone",
            "descricao": "Capacita para a elaboração e interpretação de desenhos técnicos mecânicos."
        },
        {
            "nome": "AutoCAD",
            "duracao": "40 horas",
            "modalidades": ["Presencial"],
            "horarios": ["Noite", "Finais de semana"],
            "requisitos": "Conhecimentos básicos de informática e desenho técnico",
            "valor": "Consultar valores atualizados no site ou por telefone",
            "descricao": "Capacita para utilizar o software AutoCAD para desenho técnico 2D."
        },
    ]
}

# Processo de inscrição
PROCESSO_INSCRICAO = {
    "tecnicos": """
    Para cursos técnicos no SENAI São Carlos:
    1. Consulte os cursos disponíveis no site ou presencialmente
    2. Verifique datas de inscrição e requisitos
    3. Realize a inscrição online pelo site do SENAI São Carlos ou presencialmente na secretaria
    4. Efetue o pagamento da taxa de matrícula
    5. Compareça na data informada com a documentação necessária para efetivar a matrícula
    
    Documentos necessários:
    - RG e CPF (original e cópia)
    - Comprovante de escolaridade
    - Comprovante de residência
    - Foto 3x4 recente
    """,
    
    "aprendizagem": """
    Para cursos de aprendizagem industrial no SENAI São Carlos:
    1. Acompanhe o site do SENAI para abertura de processo seletivo
    2. Realize a inscrição online
    3. Participe das etapas de seleção (prova escrita e entrevista)
    4. Se aprovado, será encaminhado para entrevista nas empresas parceiras
    5. Após contratação pela empresa, inicia-se o curso
    
    Documentos necessários:
    - RG e CPF (original e cópia)
    - Comprovante de escolaridade
    - Comprovante de residência
    - Carteira de trabalho
    """,
    
    "qualificacao": """
    Para cursos de qualificação no SENAI São Carlos:
    1. Consulte os cursos disponíveis e datas
    2. Realize a inscrição online ou presencialmente
    3. Efetue o pagamento
    4. Compareça no primeiro dia de aula com documentação
    
    Documentos necessários:
    - RG e CPF (original e cópia)
    - Comprovante de escolaridade conforme requisito do curso
    """
}

# Laboratórios e infraestrutura
INFRAESTRUTURA = {
    "laboratorios": [
        "Laboratório de Mecânica e Usinagem",
        "Laboratório de Automação Industrial",
        "Laboratório de Eletroeletrônica",
        "Laboratório de Informática",
        "Laboratório de Metrologia",
        "Laboratório de Hidráulica e Pneumática",
        "FabLab - Laboratório de Fabricação Digital"
    ],
    "instalacoes": [
        "Biblioteca técnica",
        "Auditório para 120 pessoas",
        "Refeitório",
        "Salas de aula climatizadas",
        "Estacionamento gratuito"
    ]
}

# Empresas parceiras
EMPRESAS_PARCEIRAS = [
    "Volkswagen", 
    "Electrolux", 
    "Faber-Castell", 
    "Tecumseh do Brasil", 
    "TAM MRO",
    "Embraer",
    "CBC Indústrias Pesadas"
]

# Perguntas frequentes
PERGUNTAS_FREQUENTES = {
    "Como obter bolsas de estudo?": """
    O SENAI São Carlos oferece algumas opções de bolsas:
    - Bolsas para funcionários de empresas contribuintes
    - Descontos para pagamento antecipado
    - Programas de bolsas especiais em parceria com empresas
    - Programa SENAI de Gratuidade (PSG) para pessoas de baixa renda
    
    Consulte a secretaria para mais informações sobre os requisitos e disponibilidade.
    """,
    
    "Como obter certificados de cursos concluídos?": """
    Para solicitar certificados de cursos concluídos no SENAI São Carlos:
    - Presencialmente: Compareça à secretaria com documento de identificação
    - Online: Acesse o portal do aluno com seu login e senha
    - Segunda via: Pode ser solicitada mediante pagamento de taxa administrativa
    
    O prazo para emissão de certificados é de até 30 dias úteis após a conclusão do curso.
    """,
    
    "O SENAI oferece estágios?": """
    Sim, o SENAI São Carlos possui um setor de encaminhamento de estágios que auxilia:
    - No cadastro de currículos
    - Na divulgação de vagas de empresas parceiras
    - No processo de contratação de estagiários
    
    Os alunos matriculados nos cursos técnicos têm prioridade no encaminhamento para vagas.
    """,
    
    "Como transferir de curso ou unidade?": """
    Para transferências no SENAI São Carlos:
    - Solicite na secretaria acadêmica o requerimento de transferência
    - A transferência está sujeita à disponibilidade de vagas e compatibilidade de currículos
    - Pode haver necessidade de adaptação curricular
    - Para transferência entre unidades, é necessário verificar se o curso desejado é oferecido na unidade de destino
    
    Consulte a secretaria para mais informações sobre prazos e requisitos.
    """
}

# Diferenciais da unidade de São Carlos
DIFERENCIAIS = [
    "Laboratório FabLab com impressoras 3D e equipamentos de última geração",
    "Parceria com empresas de tecnologia do Parque Tecnológico de São Carlos",
    "Integração com universidades (USP e UFSCar) em projetos de pesquisa",
    "Programas de inovação tecnológica para pequenas e médias empresas",
    "Projetos integradores com aplicação prática na indústria local",
    "Participação em olimpíadas do conhecimento e torneios de robótica"
]

# Eventos regulares
EVENTOS = [
    "Feira de Profissões (anual - outubro)",
    "INOVA SENAI - Mostra de projetos inovadores (anual - novembro)",
    "Workshop de Tecnologia e Indústria 4.0 (semestral)",
    "Semana da Tecnologia (anual - maio)",
    "Torneio de Robótica SENAI (regional - agosto)"
]

# Dados de contato específicos
CONTATOS = {
    "secretaria": {
        "telefone": "(16) 3373-9901",
        "email": "secretaria.saocarlos@sp.senai.br",
        "horario": "Segunda a sexta, das 8h às 21h"
    },
    "coordenacao_cursos": {
        "telefone": "(16) 3373-9910",
        "email": "cursos.saocarlos@sp.senai.br",
        "horario": "Segunda a sexta, das 8h às 17h"
    },
    "atendimento_empresas": {
        "telefone": "(16) 3373-9920",
        "email": "empresas.saocarlos@sp.senai.br",
        "horario": "Segunda a sexta, das 8h às 17h"
    }
}