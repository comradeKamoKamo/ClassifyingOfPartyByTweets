from pathlib import Path
import numpy as np

def main():

    np.random.seed(19)

    for f in Path("Data/").glob("*"):
        if f.is_dir():
           print(f)
           train = (f / "train.txt").open("w",encoding="utf-8")
           test = (f / "test.txt").open("w",encoding="utf-8")
           for t in f.glob("*.csv"):
                if  np.random.rand() > 0.7:
                    msg = "{0}\n".format(str(t))
                    test.write(msg)
                    print("test ->",msg)
                else:
                    msg = "{0}\n".format(str(t))
                    train.write(msg)
                    print("train ->",msg)
           train.close()
           test.close()
            
if __name__=="__main__":
    main()