from sqlalchemy.orm import Session
import models
from datetime import date

# --- Funções CRUD para Aluno ---
def create_aluno(db: Session, nome_completo: str, data_nascimento: date, nome_responsavel: str, telefone_responsavel: str, endereco: str):
    db_aluno = models.Aluno(
        nome_completo=nome_completo,
        data_nascimento=data_nascimento,
        nome_responsavel=nome_responsavel,
        telefone_responsavel=telefone_responsavel,
        endereco=endereco
    )
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

def get_alunos(db: Session):
    return db.query(models.Aluno).all()

def update_aluno(db: Session, aluno_id: int, nome_completo: str, data_nascimento: date, nome_responsavel: str, telefone_responsavel: str, endereco: str):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if db_aluno:
        db_aluno.nome_completo = nome_completo
        db_aluno.data_nascimento = data_nascimento
        db_aluno.nome_responsavel = nome_responsavel
        db_aluno.telefone_responsavel = telefone_responsavel
        db_aluno.endereco = endereco
        db.commit()
        db.refresh(db_aluno)
    return db_aluno

def delete_aluno(db: Session, aluno_id: int):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if db_aluno:
        db.delete(db_aluno)
        db.commit()
    return db_aluno

# --- Funções CRUD para Professor ---
def create_professor(db: Session, nome_completo: str, cpf: str, telefone: str, email: str):
    db_professor = models.Professor(nome_completo=nome_completo, cpf=cpf, telefone=telefone, email=email)
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

def get_professores(db: Session):
    return db.query(models.Professor).all()

def update_professor(db: Session, professor_id: int, nome_completo: str, cpf: str, telefone: str, email: str):
    db_professor = db.query(models.Professor).filter(models.Professor.id == professor_id).first()
    if db_professor:
        db_professor.nome_completo = nome_completo
        db_professor.cpf = cpf
        db_professor.telefone = telefone
        db_professor.email = email        
        db.commit()
        db.refresh(db_professor)
    return db_professor


def delete_professor(db: Session, professor_id: int):
    db_professor = db.query(models.Professor).filter(models.Professor.id == professor_id).first()
    if db_professor:
        db.delete(db_professor)
        db.commit()
    return db_professor

# --- Funções CRUD para Atividade ---
def create_atividade(db: Session, nome: str, descricao: str, idade_recomendada: str):
    db_atividade = models.Atividade(nome=nome, descricao=descricao, idade_recomendada=idade_recomendada)
    db.add(db_atividade)
    db.commit()
    db.refresh(db_atividade)
    return db_atividade

def get_atividades(db: Session):
    return db.query(models.Atividade).all()

def update_atividade(db: Session, atividade_id: int, nome: str, descricao: str, idade_recomendada: str):
    db_atividade = db.query(models.Atividade).filter(models.Atividade.id == atividade_id).first()
    if db_atividade:
        db_atividade.nome = nome
        db_atividade.descricao = descricao
        db_atividade.idade_recomendada = idade_recomendada       
        db.commit()
        db.refresh(db_atividade)
    return db_atividade

def delete_atividade(db: Session, atividade_id: int):
    db_atividade = db.query(models.Atividade).filter(models.Atividade.id == atividade_id).first()
    if db_atividade:
        db.delete(db_atividade)
        db.commit()
    return db_atividade

# --- Funções CRUD para Cardapio ---
def create_cardapio(db: Session, data: date, tipo_refeicao: str, descricao: str):
    db_cardapio = models.Cardapio(data=data, tipo_refeicao=tipo_refeicao, descricao=descricao)
    db.add(db_cardapio)
    db.commit()
    db.refresh(db_cardapio)
    return db_cardapio

def get_cardapios(db: Session):
    return db.query(models.Cardapio).order_by(models.Cardapio.data.desc()).all()


def update_cardapio(db: Session, cardapio_id: int, data: date, tipo_refeicao: str, descricao: str):
    db_cardapio = db.query(models.Cardapio).filter(models.Cardapio.id == cardapio_id).first()
    if db_cardapio:        
        db_cardapio.data = data
        db_cardapio.tipo_refeicao = tipo_refeicao
        db_cardapio.descricao = descricao        
        db.commit()
        db.refresh(db_cardapio)
    return db_cardapio


def delete_cardapio(db: Session, cardapio_id: int):
    db_cardapio = db.query(models.Cardapio).filter(models.Cardapio.id == cardapio_id).first()
    if db_cardapio:
        db.delete(db_cardapio)
        db.commit()
    return db_cardapio
