import csv,os
from janome import tokenizer, tokenfilter ,analyzer
from pathlib import Path

def main():
   for csv in Path("DataCollecting/rawdata/").glob("*.csv"):
        tokenize_tweets(csv)

def tokenize_tweets(party_csv):
    party_name = Path(party_csv.name).stem
    Path("./Data/{0}".format(party_name)).mkdir(exist_ok=True)

    t = tokenizer.Tokenizer()
    char_filters = [analyzer.UnicodeNormalizeCharFilter(),
                    analyzer.RegexReplaceCharFilter(r"@[a-zA-Z\d]*",""),
                    analyzer.RegexReplaceCharFilter(r"#",""),
                    analyzer.RegexReplaceCharFilter(r"https?:[a-zA-Z\d/\.]*","")]
    token_filters = [tokenfilter.POSStopFilter(["記号"]),
                 tokenfilter.LowerCaseFilter()]
    t_analyzer = analyzer.Analyzer(char_filters,t,token_filters)
    
    with party_csv.open("r",encoding="utf-8") as pcf:
        tweets = csv.DictReader(pcf)
        for tweet in tweets:
            with Path("./Data/{0}/{1}.csv".format(party_name,tweet["id"])).open("a",encoding="utf-8") as tcf:
                for token in t_analyzer.analyze(tweet["text"]):
                    tcf.write("{0},{1},{2},{3},{4}\n".format(
                        token.surface,token.part_of_speech,token.base_form,token.infl_type,token.infl_form))
                
if __name__ == "__main__":
    main()

