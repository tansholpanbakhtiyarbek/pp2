import psycopg2
import config

def get_connection():
    return psycopg2.connect(**config.config)