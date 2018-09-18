from pathlib import Path
import numpy as np
import sqlite3
from contextlib import closing

def main():

    np.random.seed(1919)

    for f in Path("Data/").glob("*"):
        if f.is_dir():
            #print(f)
            train = (f / "train.txt").open("w",encoding="utf-8")
            test = (f / "test.txt").open("w",encoding="utf-8")
            meet_exist = list(f.glob("meet.txt"))
            if len(meet_exist) == 0:
                continue
            meet = (f / "meet.txt").open("r",encoding="utf-8")
            meets = []
            for line in meet.readlines():
                meets.append(line[:-1])
            dbs = list(f.glob("*.db"))
            if len(dbs) == 0:
                continue
            db_path = str(dbs[0])
            with closing(sqlite3.connect(db_path)) as con:
                c = con.cursor()
                sql = "SELECT DISTINCT tweet_id FROM Parts"
                for row in c.execute(sql):
                    t = row[0]
                    for tweet_id in meets:
                        if t == int(tweet_id):
                            msg = "{0}\n".format(str(t))
                            if  np.random.rand() > 0.7:
                                test.write(msg)
                                #print("test ->",msg)
                            else:
                                train.write(msg)
                                #print("train ->",msg)
                            break
            train.close()
            test.close()
            
if __name__=="__main__":
    main()