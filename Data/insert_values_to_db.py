import sqlite3, csv
from pathlib import Path

con_nouns = sqlite3.connect("Data/nouns.db")
c_nouns = con_nouns.cursor()
con_verbs = sqlite3.connect("Data/verbs.db")
c_verbs = con_verbs.cursor()


def main():
    for p in Path("Data/").glob("*"):
        if p.is_dir():
            with (p / "train.txt").open("r",encoding="utf-8") as f:
                for l in f.readlines():
                    add_tweets(Path(l[:-1]),str(p).replace("Data\\",""))
                    # This line only supports Windows.

    con_nouns.commit()
    con_verbs.commit()
    con_nouns.close()
    con_verbs.close()

def add_tweets(tweet_csv,its_party):
    with tweet_csv.open("r",encoding="utf-8") as f:
        tweet = csv.DictReader(f,["surface",
                    "part_of_speech",
                    "part_of_speech2",
                    "part_of_speech3",
                    "part_of_speech4",
                    "base_form",
                    "infl_type",
                    "infl_form"])
        c = None
        for part in tweet:
            if part["part_of_speech"] == "名詞":
                c = c_nouns
            elif part["part_of_speech"] == "動詞":
                c = c_verbs
            else:
                c = None
            # エスケープ処理
            base = str(part["base_form"]).replace("'","''")
            if c!=None:
                sql = "SELECT {0} FROM Counts WHERE key = '{1}'".format(its_party,base)
                c.execute(sql)
                row = c.fetchone()
                if row==None:
                    sql = "INSERT INTO Counts (key,{1}) values ('{0}',1)".format(base,its_party)
                    c.execute(sql)
                else:
                    new_v = row[0] + 1
                    sql = "UPDATE Counts SET {0} = {1} WHERE key = '{2}'".format(
                        its_party,new_v,base)
                    c.execute(sql)


if __name__=="__main__":
    main()