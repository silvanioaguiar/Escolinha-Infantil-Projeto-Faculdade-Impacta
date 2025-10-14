from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    nome_responsavel = Column(String(100), nullable=False)
    telefone_responsavel = Column(String(20), nullable=False)
    endereco = Column(String(200))

class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=False)
    telefone = Column(String(20))
    email = Column(String(100))

class Atividade(Base):
    __tablename__ = "atividades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    idade_recomendada = Column(String(50))

    # Relacionamento com a tabela de associação
    # agendas_associadas = relationship("AgendaAtividade", back_populates="atividade")

class Cardapio(Base):
    __tablename__ = "cardapios"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False, index=True)
    tipo_refeicao = Column(String(50), nullable=False) # Ex: Lanche da Manhã, Almoço
    descricao = Column(Text, nullable=False)   
    

