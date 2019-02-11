from pathlib import Path
import os

# Data
for f in Path("../ClassifyingOfPartyByTweets/Data").glob("*.npz"):
    os.remove(str(f))

for f in Path("../ClassifyingOfPartyByTweets/Data").glob("*.db"):
    os.remove(str(f))

# 各政党のフォルダ
for pd in [v for v in Path("Data").glob("*") if v.is_dir()] :
    if (pd / Path("train.txt")).exists():
        for f in pd.glob("*.txt"):
            os.remove(str(f))