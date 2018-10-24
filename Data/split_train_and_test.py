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
            dbs = list(f.glob("*.db"))
            if len(dbs) == 0:
                continue
            db_path = str(dbs[0])
            with closing(sqlite3.connect(db_path)) as con:
                c = con.cursor()
                sql = "SELECT DISTINCT tweet_id FROM Parts"
                for row in c.execute(sql):
                    rand = np.random.rand()
                    if rand <= 0.5:
                        #skip
                        continue
                    t = row[0]
                    if  rand > 0.85:
                        msg = "{0}\n".format(str(t))
                        test.write(msg)
                        #print("test ->",msg)
                    else:
                        msg = "{0}\n".format(str(t))
                        train.write(msg)
                        #print("train ->",msg)
            train.close()
            test.close()
            
if __name__=="__main__":
    main()