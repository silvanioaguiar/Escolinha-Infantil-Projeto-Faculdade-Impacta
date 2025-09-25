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