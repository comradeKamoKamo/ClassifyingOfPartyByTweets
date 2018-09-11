import sqlite3,csv
from pathlib import Path
import numpy as np
from contextlib import closing

class GetTweetScore:

    def __init__(self):
        self.__con_verbs = sqlite3.connect("Data/verbs.db")
        self.__con_nouns = sqlite3.connect("Data/nouns.db")
        self.__c_verbs = self.__con_verbs.cursor()
        self.__c_nouns = self.__con_nouns.cursor()

    def GetScore(self,tweet_id,its_party,rtn_index=64):
        with closing(sqlite3.connect("Data/{0}/{0}.db".format(its_party))) as con:
            c_parts  = con.cursor()
            sql = "SELECT * FROM Parts WHERE tweet_id = ?"
            tweet = []
            for row in c_parts.execute(sql,(tweet_id,)):
                part = dict()
                part["surface"] = row[0]
                part["part_of_speech"] = row[1]
                part["part_of_speech2"] = row[2]
                part["part_of_speech3"] = row[3]
                part["part_of_speech4"] = row[4]
                part["base_form"] = row[5]
                part["infl_type"] = row[6]
                part["infl_form"] = row[7]
                tweet.append(part)

            parties = self.__get_parties()

            rtn = np.zeros([rtn_index,len(parties)],dtype=float)
            rtn_c = 0

            for part in tweet:
               c = None
               if part["part_of_speech"]=="名詞":
                   c = self.__c_nouns
               elif part["part_of_speech"]=="動詞":
                    c = self.__c_verbs
               if c != None:
                    rep = part["base_form"].replace("'","''")
                    c.execute("SELECT * FROM Counts WHERE key='{0}'".format(rep))
                    row = c.fetchone()
                    if row == None:
                        continue
                    if max(row[1:]) == 1:
                        continue
                    c.execute("SELECT * FROM Standards WHERE key='{0}'".format(rep))
                    row = c.fetchone()
                    for i in range(1,len(row)):
                        try:
                            rtn[rtn_c,i-1] = row[i]
                        except IndexError:
                            print("The number of nouns and verbs is over ",rtn_index)
                            exit()
                    rtn_c += 1
            return rtn

    def __get_parties(self):
        parties = []
        with open("DataCollecting/Politicians.csv","r") as f:
            data = csv.DictReader(f)
            for row in data:
                parties.append(row["party_name"])
        return parties

    def close(self):
        self.__con_verbs.close()
        self.__con_nouns.close()