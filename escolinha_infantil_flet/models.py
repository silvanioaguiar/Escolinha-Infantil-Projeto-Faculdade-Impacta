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

    agendas = relationship("Agenda", back_populates="aluno")


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
    agendas_associadas = relationship("AgendaAtividade", back_populates="atividade")

class Cardapio(Base):
    __tablename__ = "cardapios"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False, index=True)
    tipo_refeicao = Column(String(50), nullable=False) # Ex: Lanche da Manhã, Almoço
    descricao = Column(Text, nullable=False)   
    
class Agenda(Base):
    __tablename__ = "agendas"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False, index=True)
    humor = Column(String(50))
    # alimentacao = Column(String(100))
    lanche_manha = Column(String(100))
    almoco = Column(String(100))
    lanche_tarde = Column(String(100))
    jantar = Column(String(100))
    cardapio = Column(String(200))

    sono = Column(String(100))
    observacoes = Column(Text)
    atividades_outras = Column(Text) # Novo campo para atividades manuais
    
    aluno_id = Column(Integer, ForeignKey("alunos.id"))
    professor_id = Column(Integer, ForeignKey("professores.id"))
    aluno = relationship("Aluno", back_populates="agendas")
    professor = relationship("Professor")
    atividades_realizadas = relationship("AgendaAtividade", back_populates="agenda")

# Nova tabela de associação para Agenda e Atividades
class AgendaAtividade(Base):
    __tablename__ = "agenda_atividades"

    id = Column(Integer, primary_key=True, index=True)
    horario = Column(String(20)) # Ex: "10:30"
    
    agenda_id = Column(Integer, ForeignKey("agendas.id"))
    atividade_id = Column(Integer, ForeignKey("atividades.id"))

    agenda = relationship("Agenda", back_populates="atividades_realizadas")
    atividade = relationship("Atividade", back_populates="agendas_associadas")

    

