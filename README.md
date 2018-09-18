# ClassifyingOfPartyByTweets
日本の政党のツイートを政党ごとに分類する教師あり学習をしてみる。

# 目的
日本の政党の公式広報アカウントからツイートを取得する。それを訓練データとテストデータに分割し、訓練データをもとに機械学習を行い、テストデータのツイートについて正しい政党に分類できるモデルを構築する。  
ツイートという日本語の文章から特徴量を抽出する過程に、自然言語処理を用いる。
# 開発環境・ライブラリ・リポジトリ
## 環境
 - Python 3.5.4 | Anaconda custom (64-bit)
 - **Windows 10** Home (64-bit)
     - リポジトリのコードはWinでしか動かないものあり。
## ライブラリ
 - Janome 0.3.6
 - Keras 2.0.5 / Tensorflow 1.0.1
 - matplotlib,numpy
## リポジトリ
 - [https://github.com/comradeKamoKamo/ClassifyingOfPartyByTweets](https://github.com/comradeKamoKamo/ClassifyingOfPartyByTweets)
     - 要するにここ / branchとかはすごく適当に扱います。
     - 英語わからないので各名命があってるか知らない。
# 計画

## ツイートの取得
 - TwitterのUserStreamAPIを用いて、各党から一斉に取得する。  
その過程で、別リポジトリの自作モジュールを利用。  
     - [https://github.com/comradeKamoKamo/GetTweetsOfSpecifiedUser](https://github.com/comradeKamoKamo/GetTweetsOfSpecifiedUser)  
 - Twitterのゴミ開発者ルール改正のせいで9月以降はデータ取得がめんどくさくなりそう。Twitterを許してはいけない。
 - DataCollecting/Politicains.csv -> 政党のscreen_nameとこのプロジェクトで使う政党名(英略称)が記載。
 - DataCollecting/data_collect.py -> 取得スクリプト。
 - 取得したツイート -> DataCollecting/rawdata
## 形態素解析
 - Janomeを用いて、ツイートを形態素解析して、CSVで出力する。
     - Mecabを最初は使おうとしたけど、Winに導入するのは無理だった。
     - Filterを使う。
         - @スクリーンネーム、#ハッシュタグ、URL、記号は無視
             - 今考えてみたら$ハッシュタグも無視すべき？あんま使われないからセーフ？
         - 名詞の複合名詞化は正答率が下がったのでやめた。
         - 英単語は小文字に。
 - DataCollecting/data_tokenize.py -> スクリプト
 - DB->Data/政党名
     - SQLite化した。
## 訓練データとテストデータ分割
 - 乱数を用いて、7:3ぐらいに分割する。
     - numpyの乱数の種は19で固定する。
 - Data/政党名/train.txt | test.txt にそれぞれツイートIDを書き込む。
 - Data/split\_train\_and\_test.py
 - 以降は訓練ツイートのみを扱ってゆく。
## ツイートの特徴量化
- データ処理には速度、効率性を考慮して、SQLiteを用いる。
    - Data/nouns.db | verbs.db に記録。
    - SQL文を生成するのでコードが汚くなるなぁ。
    - 注意：テストツイートを解析してDBに加えないこと！！
### 動詞と名詞の数を数える。
 - 各政党ごとの訓練ツイートから動詞、名詞を抜き出し、登場回数を各政党ごとにDBに記録。
    - 動詞（内部処理的には名詞も）は原形でカウント。
    - Data/create_empty_db.py -> DB作成。（Counts テーブル）  
    - Data/insert_values_to_db.py -> 登場回数を記録。
### データを統計的に処理
 - ある単語について、
     - 各党の登場回数を各党の訓練ツイート数で割って正規化。(これをデータ集合Xとする。)
     - Xの平均E(X)、標準偏差σ(X)を求める。
     - Xの各データxについて、z = (x - E(X)) / σ(X)を求める。
        - 偏差を標準偏差で割った値。
     - この各党ごとのZをDBに保存。(Standards テーブル)
 -  Data/insert\_standard\_to\_db.py
### DBをもとにツイートから特徴量を出力する
 - ツイートから名詞、動詞を抜き出す。
 - (任意の数,政党数)の二次元numpy配列を作る。はじめは全要素0。
 - その単語がDBに登録されていたら、Standardテーブルよりその単語の各党ごとの値を配列に登録。
     - 登場回数が1回しかないものはここで無視する。
 - その配列を返す。
 - GetTweetScore.py -> 上を行うモジュール。
## 学習
 - train.py 
     - 受け取った特徴量配列を平面化(Flatten)して全結合層（ロジスティクス回帰）に投げる。活性化関数Relu。
     - 適当に他クラス分類。目的関数SGD、誤差関数は交差エントロピー法、最終層はsoftmax関数。
 - 学習済みモデル -> model.hdf5
 - モデル構造 -> model.json
 ## 学習評価
  - train.py
     - 正規化混合行列、マイクロ平均-適合率/再現率曲線、マイクロ平均-ROC曲線とそれぞれのAUC計算、出力。
         - CM.png , PR-AUC.png , ROC-AUC.png
     - 正答率を再計算。与野党正答率も。
         - 正答率 : 0.8293731041456016 
         - 与野党 : 0.9299797775530839