import numpy as np
import matplotlib.pyplot as plt
import csv

def main():
    cm = []
    for i in range(1, 4):
        cm.append(np.load("result/{0}/cm.npy".format(i)))
    cm = np.asarray(cm)
    cm_a = np.mean(cm,axis=0)

    fig = plt.figure()
    parties = get_parties()
    ax = plt.subplot()
    cax = ax.matshow(cm_a, interpolation="nearest", cmap="autumn_r")
    fig.colorbar(cax)
    ax.set_xticklabels([""]+parties)
    ax.set_yticklabels([""]+parties)
    plt.title("Normalized Confusion Matrix")
    plt.xlabel("Predicted class")
    plt.ylabel("True class")
    plt.show()

    with open("result/cm.csv","w") as f:
        writer = csv.writer(f,delimiter=",")
        writer.writerows(cm_a)


def get_parties():
    parties = []
    with open("DataCollecting/Politicians.csv" ,"r") as f:
        data = csv.DictReader(f)
        for row in data:
            parties.append(row["party_name"])
    return parties

if __name__ == "__main__":
    main()