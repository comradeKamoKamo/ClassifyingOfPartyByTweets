from pathlib import Path
import pickle
import copy

train_indexes = dict()
test_indexes = dict()
for pd in [v for v in Path("../ClassifyingOfPartyByTweets/Data").glob("*") if v.is_dir() and v.name[0:1]!="_"]:
    with (pd / Path("train.txt")).open("r") as f:
        train_ids = [v[:-1] for v in f.readlines()]
    with (pd / Path("test.txt")).open("r") as f:
        test_ids = [v[:-1] for v in f.readlines()]
    train_indexes[pd.name] = copy.deepcopy(train_ids)
    test_indexes[pd.name] = copy.deepcopy(test_ids)
split_info = dict()
split_info["train"] = train_indexes
split_info["test"] = test_indexes
with Path("split_data.pickle").open("wb") as f:
    pickle.dump(split_info, f)
