import GetTweets
import csv 
from collections import OrderedDict
from path import Path

with open("DataCollecting/Politicians.csv","r") as f:
    parties = csv.DictReader(f)

    get_tweets = GetTweets.GetTweets("DataCollecting/OAuth.json")

    #GetTweets.pyを修正したのでAPI規制は回避できる。遅くなるけど。
    for party in parties:
        get_tweets.get_tweets(party["screen_name"],avoid_api_regulation=True)
        get_tweets.save_tweets(Path("DataCollecting/rawdata/" + party["party_name"] + ".csv"))
