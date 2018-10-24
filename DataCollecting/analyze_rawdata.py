import csv
from pathlib import Path
import numpy as np
from janome import tokenizer, tokenfilter ,analyzer

def main():
    t_analyzer = tokenize_init()

    parties = []
    with open("DataCollecting/Politicians.csv","r") as f:
        parties = csv.DictReader(f)
    
        parties_data = dict()
        for party in parties:
            parties_data[party["party_name"]] = []
            with Path("DataCollecting/rawdata/{0}.csv".format(party["party_name"])).open("r",encoding="utf-8") as d:
                tweets = csv.DictReader(d)
                for tweet in tweets:
                    data = dict()
                    data["id"] = tweet["id"]
                    data["len"] = len(tweet["text"])
                    parties_data[party["party_name"]].append(data)

        lens = []
        for party_data in parties_data.values():
            for data in party_data:
                lens.append(data["len"])
        lens = np.asarray(lens)
        average = np.mean(lens)
        std = np.std(lens)

        print("average:",average)
        print("std:",std)

        for party_name ,party_data in parties_data.items():
            with Path("Data/{0}/meet.txt".format(party_name)).open("w") as d:
                for data in party_data:
                    if data["len"] >= average - std:
                        d.write("{0}\n".format(data["id"]))
        

def tokenize(t_analyzer,tweet_text):
    return len(t_analyzer.analyze(tweet_text))

def tokenize_init():
    t = tokenizer.Tokenizer()
    char_filters = [analyzer.UnicodeNormalizeCharFilter(),
                        analyzer.RegexReplaceCharFilter(r"@[a-zA-Z\d]*",""),
                        analyzer.RegexReplaceCharFilter(r"#",""),
                        analyzer.RegexReplaceCharFilter(r"https?:[a-zA-Z\d/\.]*","")]
    token_filters = [tokenfilter.POSStopFilter(["記号"]),
                        tokenfilter.LowerCaseFilter()]
    t_analyzer = analyzer.Analyzer(char_filters,t,token_filters)
    return t_analyzer

if __name__=="__main__":
    main()