from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os


# ATENÇÃO: Substitua com suas credenciais do MySQL e nome do banco de dados.
# É necessário criar o banco de dados 'escolinha' no seu MySQL antes de rodar.
# Comando para criar o banco de dados no MySQL: CREATE DATABASE escolinha;
# Formato da URL: "mysql+mysqlconnector://<usuario>:<senha>@<host>[:<porta>]/<banco_de_dados>"

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM que criaremos em models.py
Base = declarative_base()
