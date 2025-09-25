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
    
    

