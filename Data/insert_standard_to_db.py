import sqlite3
from pathlib import Path
import numpy as np
from collections import OrderedDict
import csv
from contextlib import closing

#   x = 回数 / ツイート数
#   Z = (X − μ)/σ を求めてDBに記録。

def main():
    set_standard_to_db("Data/verbs.db")
    set_standard_to_db("Data/nouns.db")
    
def set_standard_to_db(db_name):
    parties = get_parties()
    counts = get_parties_count(parties)
    with closing(sqlite3.connect(db_name)) as con:
        c = con.cursor()

        sql = "CREATE TABLE IF NOT EXISTS Standards (key TEXT primary key"
        for party in parties:
            sql += ", {0} REAL DEFAULT 0 NOT NULL".format(party)
        sql += ")"
        c.execute(sql)

        c.execute("SELECT Count(*) FROM Counts")
        row_count = c.fetchone()[0]
        for i in range(1,row_count+1):
            sql = "SELECT * FROM Counts WHERE ROWID={0}".format(i)
            c.execute(sql)
            row = c.fetchone()
            key = row[0].replace("'","''")
            parties_values = row[1:]

            X = []
            for count,party in zip(parties_values,parties):
                X.append(count / counts[party])

            Ex = np.mean(X,dtype=float)
            Sigx = np.std(X,dtype=float)
            Zx = []
            for x in X:
                z = (x-Ex)/Sigx
                Zx.append(z)
            
            sql = "INSERT INTO Standards (key) values ('{0}')".format(key)
            c.execute(sql)
            for z,party in zip(Zx,parties):
                sql = "UPDATE Standards SET {0}={1} WHERE key='{2}'".format(party,z,key)
                c.execute(sql)
        con.commit()

def get_parties():
    parties = []
    with open("DataCollecting/Politicians.csv","r") as f:
        data = csv.DictReader(f)
        for row in data:
            parties.append(row["party_name"])
    return parties

def get_parties_count(parties):
    counts = OrderedDict()
    for party in parties:
        with Path("Data/{0}/train.txt".format(party)).open("r",encoding="utf-8") as f:
            counts[party] = len(f.readlines())
    return counts

if __name__=="__main__":
    main()