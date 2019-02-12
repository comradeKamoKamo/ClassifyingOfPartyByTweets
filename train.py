import numpy as np
import csv
import sys
import pickle
from pathlib import Path
from keras.models import Sequential
from keras.layers import Dropout,Dense,Reshape,Flatten
from keras import utils
from keras.callbacks import EarlyStopping
from keras.preprocessing.image import ImageDataGenerator
from keras.models import model_from_json
from sklearn.metrics import precision_recall_curve,auc,roc_curve,confusion_matrix
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt

PART_SIZE = 240


def main():

    global NUM
    try:
        NUM = sys.argv[1]
    except IndexError:
        NUM = ""

    n_classes = len(get_parties())
    X_train , y_train , Z_train= np_load("../ClassifyingOfPartyByTweets/Data/train.npz")
    y_train_ = utils.np_utils.to_categorical(y_train,n_classes)
    X_test , y_test , Z_test = np_load("../ClassifyingOfPartyByTweets/Data/test.npz")
    y_test_ = utils.np_utils.to_categorical(y_test,n_classes)
    
    
    model = build_model(PART_SIZE)
    model = train(model,X_train,y_train_,X_test,y_test_)
    
    
    #model = load_model("model.json","model.hdf5")

    test(model,X_test,y_test,Z_test)
    

def train(model,X_train,y_train,X_test,y_test):
    model.compile(optimizer="adam",
            loss="categorical_crossentropy",
            metrics=["accuracy"])
    es_cb = EarlyStopping()
    model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=30,callbacks=[es_cb])
    model.save_weights("../ClassifyingOfPartyByTweets/model{0}.hdf5".format(NUM))
    r = model.evaluate(X_test,y_test)
    print(r)
    with Path("../ClassifyingOfPartyByTweets/result/accuracy_origin.txt").open("a") as f:
        f.write(str(r[1]) + "\n")
    return model

def load_model(model_json_path,model_weights_path):
    json_string = open(model_json_path,'r').read()
    model = model_from_json(json_string)
    model.load_weights(model_weights_path)
    return model

def test(model,X_test,y_test,Z_test):
    c_acc = 0
    n_classes = len(get_parties())
    parties = get_parties()
    #mis_p = []
    #ok_p = []

    raw_preds = model.predict(X_test)
    preds = []
    for raw_pred in raw_preds:
        preds.append(np.where(raw_pred == max(raw_pred))[0][0])
    y_test = np.array(y_test)
    preds = np.array(preds)

    pi = 0
    for x , y ,z in zip(X_test,y_test,Z_test):
        r = model.predict(x.reshape(1,PART_SIZE,n_classes))[0]
        if max(r) > 0.55:
            p = np.where(r == max(r))[0][0]
        else:
            with Path("data\\result{0}.pickle".format(NUM)).open("rb") as f:
                result = pickle.load(f)
            w2v_preds = result[0]
            z_r = result[1]
            z_softmax = result[2]
            for i in range(len(w2v_preds)):
                if y == z_r[i][0] and str(z[:-1]) == z_r[i][1]:       
                    if z_softmax[i] > max(r):
                        p = w2v_preds[i]
                        preds[pi] = p
                    else:
                        p = np.where(r == max(r))[0][0]

        if p == y :
            c_acc += 1
        pi+=1

    c_acc = c_acc / len(y_test)
    print("acc",c_acc)
    with Path("../ClassifyingOfPartyByTweets/result/accuracy.txt").open("a") as f:
        f.write(str(c_acc) + "\n")



    cm = confusion_matrix(y_test,preds)
    cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
    np.save("../ClassifyingOfPartyByTweets/result/cm{0}.npy".format(NUM),cm)
    """
    fig = plt.figure()
    ax = plt.subplot()
    cax = ax.matshow(cm, interpolation="nearest", cmap="autumn_r")
    fig.colorbar(cax)
    ax.set_xticklabels([""]+parties)
    ax.set_yticklabels([""]+parties)
    plt.title("Normalized Confusion Matrix")
    plt.xlabel("Predicted class")
    plt.ylabel("True class")
    plt.show()
    """
    return c_acc
 
def build_model(part_size):
    n_classes = len(get_parties())
    model = Sequential()
    model.add(Flatten(input_shape=(part_size,n_classes)))
    model.add(Dense(128, activation="relu"))
    model.add(Dense(64,activation="relu"))
    model.add(Dense(32,activation="relu"))
    model.add(Dense(16,activation="relu"))
    model.add(Dense(n_classes,activation="softmax")) 
    model.summary()
    json_string = model.to_json()
    open("../ClassifyingOfPartyByTweets/model.json",'w').write(json_string)
    return model

def get_parties():
    parties = []
    with open("../ClassifyingOfPartyByTweets/DataCollecting/Politicians.csv","r") as f:
        data = csv.DictReader(f)
        for row in data:
            parties.append(row["party_name"])
    return parties

def np_load(path):
    n_classes = len(get_parties())
    npz = np.load(path)
    return npz["X"] , npz["Y"] , npz["Z"]

if __name__=="__main__":
    main()