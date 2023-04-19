from pathlib import Path
# IMPORT PARA TRABAJAR CON ORACLE
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle_cli\instantclient_21_9")

BASE_DIR = Path(__file__).resolve().parent.parent

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

ORACLEXE = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'XE',
        'USER': 'system',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '1522',
    }
}