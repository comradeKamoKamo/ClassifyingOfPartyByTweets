import sqlite3, csv
from pathlib import Path

def main():
    parties = []
    with open("DataCollecting/Politicians.csv","r") as f:
        data = csv.DictReader(f)
        for row in data:
            parties.append(row["party_name"])
    create_empty_db("Data/nouns.db","noun",parties)
    create_empty_db("Data/verbs.db","verb",parties)

def create_empty_db(name,main_key,paties):
    with sqlite3.connect(name) as con:
        c = con.cursor()
        sql = "CREATE TABLE IF NOT EXISTS Counts ({0} varchar(128) primary key".format(main_key)
        for party in paties:
            sql += ", {0} integer".format(party)
        sql += ")"
        c.execute(sql)
        con.commit()

if __name__=="__main__":
    main()