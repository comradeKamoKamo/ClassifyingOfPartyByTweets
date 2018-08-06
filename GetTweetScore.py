import sqlite3,csv
from pathlib import Path
import numpy as np

class GetTweetScore:
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
            con_verbs = sqlite3.connect("Data/verbs.db")
            con_nouns = sqlite3.connect("Data/nouns.db")
            c_verbs = con_verbs.cursor()
            c_nouns = con_nouns.cursor()

            parties = self.__get_parties()

            rtn = np.zeros([rtn_index,len(parties)],dtype=float)
            rtn_c = 0

            for part in tweet:
               c = None
               if part["part_of_speech"]=="名詞":
                   c = c_nouns
               elif part["part_of_speech"]=="動詞":
                    c = c_verbs
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
            con_verbs.close()
            con_nouns.close()
            return rtn

    def __get_parties(self):
        parties = []
        with open("DataCollecting/Politicians.csv","r") as f:
            data = csv.DictReader(f)
            for row in data:
                parties.append(row["party_name"])
        return parties