from model.recbole.quick_start import run_recbole, load_data_and_model
from model.recbole.utils.case_study import full_sort_scores,full_sort_topk
from model.recbole.config import Config
from model.recbole.data import create_dataset, data_preparation
import numpy as np
import pandas as pd
import random

def train(model="BPR", dataset='movie', config=["./BPR.yaml"]):
    run_recbole(model=model, dataset=dataset, config_file_list=config)


def load_model(model_path='saved/BPR-Sep-30-2022_16-55-08.pth'):
    model = load_data_and_model(model_file=model_path, movie_config=["./movie.yaml"], dataset='movie')
    return model

def predict(userid,  model, model_name='BPR', movie= "./movie/movie.item",
            dataset="movie", inter='./movie/movie.inter', config=['./movie.yaml']):

    config = Config(model=model_name, dataset=dataset, config_file_list=config)
    dataset = create_dataset(config)
    _, _, test_data = data_preparation(config, dataset)

    user_id = userid
    item = pd.read_csv(movie, delimiter='\t')

    try:
        uid_series = dataset.token2id(dataset.uid_field, [user_id])
        topk_score, topk_iid_list = full_sort_topk(uid_series, model, test_data, k=20)
        external_item_list = dataset.id2token(dataset.iid_field, topk_iid_list.cpu())

        ids = list(external_item_list[0])
        ids = [int(i) for i in ids]
        movie_ids = item.loc[item['tmdb_id:token'].isin(ids)]["movieid:token_seq"].tolist()

    except ValueError:
        inter = pd.read_csv(inter, delimiter='\t').drop_duplicates('tmdb_id:token')
        high_rating_movie = inter[inter["grades:float"]>=5]["tmdb_id:token"].to_numpy()
        movie_ids = []
        for ele in np.array_split(high_rating_movie, 20):
            movie_id = random.choice(ele)
            movie_ids.append(movie_id)
        movie_ids = item.loc[item['tmdb_id:token'].isin(movie_ids)]["movieid:token_seq"].tolist()

    return movie_ids