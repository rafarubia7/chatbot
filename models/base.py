"""
Modelos base para validação de dados usando Pydantic
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class Contato(BaseModel):
    """Modelo para informações de contato"""
    telefone: str
    email: str
    horario: str

class Localizacao(BaseModel):
    """Modelo para informações de localização"""
    predio: str
    andar: str
    sala: str
    coordenadas: Optional[str] = None
    referencia: Optional[str] = None

class Horario(BaseModel):
    """Modelo para horários de funcionamento"""
    dias: List[str]
    periodo: str
    hora_inicio: str
    hora_fim: str
    observacoes: Optional[str] = None

class Curso(BaseModel):
    """Modelo base para cursos"""
    nome: str
    duracao: str
    modalidades: List[str]
    horarios: List[str]
    requisitos: str
    valor: Optional[str] = "Consultar valores atualizados"
    descricao: str
    area: Optional[str] = None
    vagas: Optional[int] = None
    proxima_turma: Optional[str] = None

class Sala(BaseModel):
    """Modelo para salas e laboratórios"""
    nome: str
    tipo: str
    localizacao: Localizacao
    capacidade: int
    equipamentos: List[str]
    descricao: str
    horario_funcionamento: Optional[Horario] = None
    responsavel: Optional[Contato] = None 