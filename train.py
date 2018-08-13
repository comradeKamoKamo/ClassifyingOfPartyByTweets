import numpy as np
import csv
from keras.models import Sequential
from keras.layers import Dropout,Dense,Reshape,Flatten
from keras import utils
from keras.callbacks import EarlyStopping
from keras.preprocessing.image import ImageDataGenerator
from keras.models import model_from_json
from sklearn.metrics import precision_recall_curve,auc,roc_curve,confusion_matrix
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt

PART_SIZE = 128

def main():

    n_classes = len(get_parties())
    X_train , y_train = np_load("Data/train.npz")
    y_train_ = utils.np_utils.to_categorical(y_train,n_classes)
    X_test , y_test = np_load("Data/test.npz")
    y_test_ = utils.np_utils.to_categorical(y_test,n_classes)
    
    model = build_model(PART_SIZE)
    model = train(model,X_train,y_train_,X_test,y_test_)
    
    """
    model = load_model("model.json","model.hdf5")
    """
    test(model,X_test,y_test)
    

def train(model,X_train,y_train,X_test,y_test):
    model.compile(optimizer="sgd",
            loss="categorical_crossentropy",
            metrics=["accuracy"])
    es_cb = EarlyStopping()
    model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=30,callbacks=[es_cb])
    model.save_weights("model.hdf5")
    r = model.evaluate(X_test,y_test)
    print(r)

    return model

def load_model(model_json_path,model_weights_path):
    json_string = open(model_json_path,'r').read()
    model = model_from_json(json_string)
    model.load_weights(model_weights_path)
    return model

def test(model,X_test,y_test):
    c_acc = 0
    b_acc = 0
    n_classes = len(get_parties())
    parties = get_parties()
    for x , y in zip(X_test,y_test):
        r = model.predict(x.reshape(1,PART_SIZE,n_classes))[0]
        p = np.where(r == max(r))[0][0]
        if p == y :
            c_acc += 1
        if parties[p] == "LDP" or parties[p] == "Komeito":
            if parties[y] == "LDP" or parties[y] == "Komeito":
                b_acc+=1
        else:
            if not (parties[y] == "LDP" or parties[y] == "Komeito"):
                b_acc+=1
    c_acc = c_acc / len(y_test)
    b_acc = b_acc / len(y_test)
    print(c_acc,b_acc)

    raw_preds = model.predict(X_test)
    preds = []
    for raw_pred in raw_preds:
        preds.append(np.where(raw_pred == max(raw_pred))[0][0])
    y_test = np.array(y_test)
    preds = np.array(preds)

    cm = confusion_matrix(y_test,preds)
    cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
    fig = plt.figure()
    ax = plt.subplot()
    cax = ax.matshow(cm, interpolation="nearest", cmap="jet")
    fig.colorbar(cax)
    ax.set_xticklabels([""]+parties)
    ax.set_yticklabels([""]+parties)
    plt.title("Normalized Confusion Matrix")
    plt.xlabel("Predicted class")
    plt.ylabel("True class")
    plt.show()

    labels = []
    for i in range(len(parties)):
        labels.append(i)
    y_test = label_binarize(y_test,classes=labels)
    preds = label_binarize(preds,classes=labels)
    precision, recall , _ = precision_recall_curve(y_test.ravel(),preds.ravel())
    prc_auc = auc(recall,precision)

    plt.figure()
    plt.step(recall, precision, color="b", alpha=0.2,where="post")
    plt.fill_between(recall, precision, step="post", alpha=0.2, color="b")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("P/R (Micro Average) AUC={0}".format(prc_auc))
    plt.show()

    fpr , tpr , _ = roc_curve(y_test.ravel(),preds.ravel())
    roc_auc = auc(fpr,tpr)

    plt.figure()
    plt.step(fpr, tpr, color="r", alpha=0.2,where="post")
    plt.fill_between(fpr,tpr, step="post", alpha=0.2, color="r")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.plot([0,1],[0,1],linestyle="dashed",color="pink")
    plt.title("ROC (Micro Average) AUC={0}".format(roc_auc))
    plt.show()

    return c_acc , b_acc
 
def build_model(part_size):
    n_classes = len(get_parties())
    model = Sequential()
    model.add(Flatten(input_shape=(part_size,n_classes)))
    model.add(Dropout(0.5))
    model.add(Dense(32,activation="relu"))
    model.add(Dense(n_classes,activation="softmax"))
    model.summary()
    json_string = model.to_json()
    open("model.json",'w').write(json_string)
    return model

def get_parties():
    parties = []
    with open("DataCollecting/Politicians.csv","r") as f:
        data = csv.DictReader(f)
        for row in data:
            parties.append(row["party_name"])
    return parties

def np_load(path):
    n_classes = len(get_parties())
    npz = np.load(path)
    return npz["X"] , npz["Y"]

if __name__=="__main__":
    main()