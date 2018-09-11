import csv,os,sqlite3
from janome import tokenizer, tokenfilter ,analyzer
from pathlib import Path
from contextlib import closing

# DBに書き込むように。
# テーブルの最後にツイートIDを

def main():
   for csv in Path("DataCollecting/rawdata/").glob("*.csv"):
        tokenize_tweets(csv)

def tokenize_tweets(party_csv):
    party_name = Path(party_csv.name).stem
    with closing(sqlite3.connect("Data/{0}/{0}.db".format(party_name))) as con:
        cursor = con.cursor()
        sql = "CREATE TABLE IF NOT EXISTS Parts "
        sql += "(surface TEXT, part_of_speech TEXT, part_of_speech2 TEXT, part_of_speech3 TEXT, part_of_speech4 TEXT, "
        sql += "base_form TEXT, infl_type TEXT, infl_form TEXT, tweet_id integer)"
        cursor.execute(sql)

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
                for token in t_analyzer.analyze(tweet["text"]):
                    part , part2 , part3 , part4 = token.part_of_speech.split(",")
                    values = (
                        token.surface,part,part2,part3,part4,
                        token.base_form,token.infl_type,token.infl_form,tweet["id"])
                    sql = "INSERT INTO Parts VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    cursor.execute(sql,values)
        con.commit()
                
if __name__ == "__main__":
    main()

