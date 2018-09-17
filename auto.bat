del Data\*.db
del Data\*.npz
python Data/create_empty_db.py
python Data/insert_values_to_db.py
python Data/insert_standard_to_db.py
python Data/data_to_npz.py
python train.py