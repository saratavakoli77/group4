import pandas as pd
from util import convert

def get_inter_from_raw(raw_csv_path="./movie_1M/kafka_raw.csv"):
    inter = pd.read_csv(raw_csv_path, header=None)
    inter = inter.rename(columns={0:"time", 1:"user_id", 2:"movie_id"})
    inter["rating"]=inter["movie_id"].apply(lambda row: row.split("=")[-1])
    inter["movie_id"]=inter["movie_id"].apply(lambda row: row.split("/")[-1][:-2])
    inter = inter.reset_index(drop=True)
    inter = inter[["user_id","movie_id","rating","time"]]
    inter.to_csv("./movie_1M/inter_1M.csv",index=False)

def get_movie_from_inter(inter_path="./movie_1M/inter_1M.csv"):
    inter = pd.read_csv(inter_path)
    movie = inter[['movie_id','rating']]
    movie = movie.reset_index()
    movie  = movie.rename(columns={"index": "movie_uid"})
    movie = movie.groupby(['movie_uid','movie_id']).mean().sort_values(by="rating", ascending=False)
    movie.to_csv("./movie_1M/movie.csv")


def convert_inter_to_atom(inter_path="./movie_1M/inter_1M.csv", 
    rename_col={"user_id":"user_id:token", "movie_id":"movie_id:token_seq", "rating":"rating:float" }, 
    input_dict={0:"user_id:token", 1:"movie_id:token_seq", 2:"rating:float"}):

    # process the inter
    inter = pd.read_csv(inter_path)
    # movie = pd.read_csv(movie_path)
    # inter = pd.merge(inter, movie, how='left', on=['movie_id'])
    inter = inter.rename(columns=rename_col).sort_values(by="user_id:token").reset_index(drop=True)
    # convert the inter
    input_dict = input_dict
    convert(inter, input_dict, "./movie_1M/movie_1M.inter")
