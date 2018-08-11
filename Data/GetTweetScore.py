import sqlite3,csv
from pathlib import Path
import numpy as np

class GetTweetScore:

    def __init__(self):
        self.__con_verbs = sqlite3.connect("Data/verbs.db")
        self.__con_nouns = sqlite3.connect("Data/nouns.db")
        self.__c_verbs = self.__con_verbs.cursor()
        self.__c_nouns = self.__con_nouns.cursor()

    def GetScore(self,tweet_csv,rtn_index=64):
        with tweet_csv.open("r",encoding="utf-8") as f:
            tweet = csv.DictReader(f,["surface",
                        "part_of_speech",
                        "part_of_speech2",
                        "part_of_speech3",
                        "part_of_speech4",
                        "base_form",
                        "infl_type",
                        "infl_form"])

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