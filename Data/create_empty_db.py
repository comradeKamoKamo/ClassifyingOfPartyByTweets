import sqlite3, csv
from pathlib import Path
from contextlib import closing

def main():
    parties = []
    with open("../ClassifyingOfPartyByTweets/DataCollecting/Politicians.csv","r") as f:
        data = csv.DictReader(f)
        for row in data:
            parties.append(row["party_name"])
    create_empty_db("../ClassifyingOfPartyByTweets/Data/nouns.db",parties)
    create_empty_db("../ClassifyingOfPartyByTweets/Data/verbs.db",parties)

def create_empty_db(name,paties):
    with closing(sqlite3.connect(name)) as con:
        c = con.cursor()
        sql = "CREATE TABLE IF NOT EXISTS Counts (key TEXT primary key"
        for party in paties:
            sql += ", {0} integer DEFAULT 0 NOT NULL".format(party)
        sql += ")"
        c.execute(sql)
        con.commit()

if __name__=="__main__":
    main()