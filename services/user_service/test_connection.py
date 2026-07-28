from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/user_db"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT current _database"))
        print("connected!")
        print(result.scalar())
except Exception as e:
    print(type(e).__name__)
    print(e)