"""
Informações sobre salas, laboratórios e navegação interna do SENAI São Carlos
"""
from typing import Dict, List, Optional
from pydantic import BaseModel

class Coordenadas(BaseModel):
    lat: float
    lon: float

class Localizacao(BaseModel):
    predio: str
    andar: str
    sala: Optional[str] = None
    referencia: str
    coordenadas: Coordenadas

class Navegacao(BaseModel):
    partida: str = "entrada_principal"
    instrucoes: List[str]
    pontos_referencia: List[str]
    dicas_adicionais: Optional[str] = None

class Sala(BaseModel):
    nome: str
    tipo: str  # "laboratorio", "instalacao", "administrativo", "comum"
    descricao: str
    localizacao: Localizacao
    navegacao: Navegacao
    capacidade: Optional[int] = None
    horario_funcionamento: Optional[str] = None

SALAS: Dict[str, Sala] = {
    "refeitorio": Sala(
        nome="Refeitório",
        tipo="comum",
        descricao="Espaço para refeições com cantina e área de convivência",
        localizacao=Localizacao(
            predio="Principal",
            andar="Térreo",
            sala="R-01",
            referencia="Próximo à entrada principal",
            coordenadas=Coordenadas(lat=-22.123456, lon=-47.123456)
        ),
        navegacao=Navegacao(
            instrucoes=[
                "Passe pela catraca na entrada da escola",
                "Siga reto por aproximadamente 15 passos",
                "Vire à direita",
                "O refeitório estará à sua direita"
            ],
            pontos_referencia=["Catraca da entrada", "Corredor principal"],
            dicas_adicionais="Ao entrar no refeitório, você encontrará a AAPM (sala de achados e perdidos) à sua direita"
        ),
        horario_funcionamento="Segunda a Sexta, das 7h às 22h"
    ),
    
    "biblioteca": Sala(
        nome="Biblioteca",
        tipo="comum",
        descricao="Biblioteca técnica com acervo especializado e área de estudos",
        localizacao=Localizacao(
            predio="Principal",
            andar="1º Andar",
            sala="103",
            referencia="Acima do refeitório",
            coordenadas=Coordenadas(lat=-22.123457, lon=-47.123457)
        ),
        navegacao=Navegacao(
            instrucoes=[
                "Entre pelo acesso principal",
                "Suba a escada à direita do refeitório",
                "Vire à esquerda no corredor",
                "A biblioteca é a terceira porta à direita"
            ],
            pontos_referencia=["Escada principal", "Corredor do 1º andar"],
            dicas_adicionais="Há uma placa indicativa grande na porta"
        ),
        horario_funcionamento="Segunda a Sexta, das 8h às 21h"
    ),
    
    "lab_mecanica": Sala(
        nome="Laboratório de Mecânica",
        tipo="laboratorio",
        descricao="Laboratório equipado com tornos, fresas e equipamentos CNC",
        localizacao=Localizacao(
            predio="Oficinas",
            andar="Térreo",
            sala="O-01",
            referencia="Próximo ao estacionamento dos fundos",
            coordenadas=Coordenadas(lat=-22.123458, lon=-47.123458)
        ),
        navegacao=Navegacao(
            instrucoes=[
                "Da entrada principal, siga pelo corredor à direita",
                "Passe pelo pátio coberto",
                "Entre no prédio das oficinas",
                "O laboratório é a primeira porta à esquerda"
            ],
            pontos_referencia=["Pátio coberto", "Prédio das oficinas"],
            dicas_adicionais="Você pode identificar o laboratório pelo som das máquinas"
        ),
        capacidade=30
    ),
    
    "secretaria": Sala(
        nome="Secretaria",
        tipo="administrativo",
        descricao="Setor de atendimento e processos administrativos",
        localizacao=Localizacao(
            predio="Principal",
            andar="Térreo",
            sala="A-01",
            referencia="Ao lado da entrada principal",
            coordenadas=Coordenadas(lat=-22.123459, lon=-47.123459)
        ),
        navegacao=Navegacao(
            instrucoes=[
                "Entre pela porta principal",
                "A secretaria é a primeira sala à esquerda",
                "Procure o balcão de atendimento"
            ],
            pontos_referencia=["Entrada principal", "Hall de entrada"],
            dicas_adicionais="Há uma TV com senhas de atendimento no local"
        ),
        horario_funcionamento="Segunda a Sexta, das 7h às 21h"
    )
}

def obter_navegacao(local: str, ponto_partida: str = "entrada_principal") -> str:
    """
    Retorna instruções de navegação formatadas para um local específico
    """
    if local not in SALAS:
        return "Desculpe, não tenho informações sobre como chegar a este local."
        
    sala = SALAS[local]
    nav = sala.navegacao
    
    # Monta a resposta
    resposta = f"Para chegar ao {sala.nome}:\n"
    resposta += "\n".join(f"- {instrucao}" for instrucao in nav.instrucoes)
    
    if nav.dicas_adicionais:
        resposta += f"\n\n{nav.dicas_adicionais}"
        
    return resposta

def buscar_sala_por_nome(nome: str) -> Optional[Sala]:
    """
    Busca uma sala pelo nome ou palavras-chave
    """
    nome = nome.lower()
    for key, sala in SALAS.items():
        if nome in key.lower() or nome in sala.nome.lower():
            return sala
    return None 