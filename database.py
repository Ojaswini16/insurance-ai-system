import sqlite3

def init_db():

    conn = sqlite3.connect("claims.db")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        tenure INTEGER,
        premium REAL,
        claim REAL,
        risk_score REAL,
        decision TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_claim(data,score,decision):

    conn = sqlite3.connect("claims.db")

    conn.execute(
    "INSERT INTO history(age,tenure,premium,claim,risk_score,decision) VALUES(?,?,?,?,?,?)",
    (data["age"],data["tenure"],data["premium_amount"],data["claim_amount"],score,decision)
    )

    conn.commit()
    conn.close()