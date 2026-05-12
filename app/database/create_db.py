from sqlalchemy import text
from app.database.db_connection import engine

def create_sample_data():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                product_name TEXT,
                size TEXT,
                quantity INTEGER
            )
        """))

        conn.execute(text("""
            INSERT INTO products (product_name, size, quantity)
            VALUES
            ('Shirt', 'L', 120),
            ('Shirt', 'M', 80),
            ('Shirt', 'S', 60),
            ('T-Shirt', 'L', 150),
            ('Jeans', '32', 90)
        """))

        conn.commit()

if __name__ == "__main__":
    create_sample_data()
    print("Database created successfully!")