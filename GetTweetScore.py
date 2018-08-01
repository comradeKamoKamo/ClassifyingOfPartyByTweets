import sqlite3,csv
from pathlib import Path
from collections import OrderedDict

class GetTweetScore:
    def GetScore(self,tweet_csv):
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
            scores = OrderedDict()
            for party in parties:
                scores[party] = 0

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
                        scores[parties[i-1]] += row[i]
            con_verbs.close()
            con_nouns.close()
            return scores

    def __get_parties(self):
        parties = []
        with open("DataCollecting/Politicians.csv","r") as f:
            data = csv.DictReader(f)
            for row in data:
                parties.append(row["party_name"])
        return parties