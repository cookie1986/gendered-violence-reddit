import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_db_connection() -> psycopg.Connection:
    """Establish a local connection to the PostgreSQL database."""
    return psycopg.connect(
        host = os.getenv("POSTGRES_HOST", "localhost"),
        port = os.getenv("POSTGRES_PORT", "5432"),
        dbname = os.getenv("POSTGRES_DB"),
        user = os.getenv("POSTGRES_USER"),
        password = os.getenv("POSTGRES_PASSWORD")   
    )