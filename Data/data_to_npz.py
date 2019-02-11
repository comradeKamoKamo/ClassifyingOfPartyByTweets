import numpy as np
import csv
from GetTweetScore import GetTweetScore
from pathlib import Path

def main():
    X_test , Y_test , Z_test = load_data("test")
    np.savez("../ClassifyingOfPartyByTweets/Data/test.npz",X=X_test,Y=Y_test,Z=Z_test)
    X_train , Y_train , Z_train = load_data("train")
    np.savez("../ClassifyingOfPartyByTweets/Data/train.npz",X=X_train,Y=Y_train,Z=Z_train)
    
def load_data(mode):
    parties = get_parties()
    get_tweet_score = GetTweetScore()
    X , Y , Z = [] , [] , []
    for party in parties:
        y_party = parties.index(party)
        with Path("../ClassifyingOfPartyByTweets/Data/{0}/{1}.txt".format(party,mode)).open("r",encoding="utf-8") as f:
            for l in f.readlines():
                p = l.replace("\n","")
                # PART_SIZE = 240
                r = get_tweet_score.GetScore(l[:-1],party,240)
                X.append(r)
                Y.append(y_party)
                Z.append(l)
    get_tweet_score.close()
    X = np.asarray(X,dtype=float)
    return X, Y, Z

def get_parties():
    parties = []
    with open("../ClassifyingOfPartyByTweets/DataCollecting/Politicians.csv","r") as f:
        data = csv.DictReader(f)
        for row in data:
            parties.append(row["party_name"])
    return parties

if __name__=="__main__":
    main()
