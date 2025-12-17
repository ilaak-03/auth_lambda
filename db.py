import os
import pg8000

def get_db_connection():
    return pg8000.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        port=int(os.environ["DB_PORT"]),
        ssl_context=True
    )
