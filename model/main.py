from process import get_movie_from_inter,convert_inter_to_atom
from model import train, load_model, predict
import time
import random

if __name__ == "__main__":
    # get_movie_from_inter()
    # train()
    model = load_model()
    random.seed(int(time.time()))
    print(predict(userid="1", model=model))
