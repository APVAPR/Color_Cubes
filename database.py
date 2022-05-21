import sqlite3

with sqlite3.connect('color_cubs.sqlite') as db:
    cur = db.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS RECORDS (
        gamer text,
        score integer,
        moves integer)
    """)
    db.commit()


def insert_result(name, score, moves):
    cur.execute("""
    INSERT INTO RECORDS VALUES (?, ?, ?) 
    """, (name, score, moves))
    db.commit()
