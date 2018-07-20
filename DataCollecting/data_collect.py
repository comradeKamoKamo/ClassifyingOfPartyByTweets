import GetTweets
import csv 
from collections import OrderedDict
from path import Path

with open("Politicians.csv","r") as f:
    parties = csv.DictReader(f)

    get_tweets = GetTweets.GetTweets("OAuth.json")

    #実際にはAPIの制限があるので途中で止まる。その場合は続きから。
    for party in parties:
        get_tweets.get_tweets(party["screen_name"])
        get_tweets.save_tweets(Path("rawdata/" + party["party_name"] + ".csv"))
