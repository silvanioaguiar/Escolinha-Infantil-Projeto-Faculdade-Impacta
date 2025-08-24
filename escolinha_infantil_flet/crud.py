from sqlalchemy.orm import Session, joinedload
import models
from datetime import date
from typing import List, Dict

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

