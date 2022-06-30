import csv
from pathlib import Path
import sqlite3

db_path = str(Path(Path(__file__).parent, 'pitch_accents.sqlite'))

def test_pitch():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT pitch FROM Dict WHERE expression=?", ("えび反り",))
    print(cur.fetchall())
    con.close()

def parse_csv():
    path = str(Path(Path(__file__).parent, 'pitch_accents.csv'))
    accents =[]
    with open(path, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        accents = list(spamreader)
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("CREATE TABLE Dict(expression TEXT, reading TEXT, pitch TEXT)")
        cur.execute("CREATE INDEX ix_expression ON dict(expression ASC)")
        cur.execute("CREATE INDEX ix_reading ON dict(reading ASC)")
        cur.executemany("INSERT INTO Dict VALUES (?, ?, ?)", accents)
        con.commit()
        con.close()

if __name__ == "__main__":
    test_pitch()