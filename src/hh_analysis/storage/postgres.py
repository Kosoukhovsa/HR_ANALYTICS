"""PostgreSQL connection and load helpers will live here."""
import psycopg2


def get_connection():
    return psycopg2.connect(
        dbname="hr_analysis",
        user="postgres",
        password="12345qwz",
        host="localhost",
        port=5434
    )
