from kafka_utils import get_log_file_from_kafka, get_logs_from_file, get_log_type, parse_watch_log, parse_rate_log, add_to_log_json, for_each_log
from rest_api_utils import get_user_info, get_movie_info, add_to_info_json
import os.path
import json
import csv
import sys


import json
import os
from pathlib import Path


# removes all files in ../data folder
def cleanup_data_folder():
    [f.unlink() for f in Path("../data").glob("*") if f.is_file()] 
    
# example of a function to perform multiple actions on a single log
def action(log, get_user=False, get_movie=False, get_inter=True):
    # gets log type
    type = get_log_type(log)
    content = None

    if get_inter:
        # if it's type is watch
        if type == "watch":
            # parse content and add to json
            content = parse_watch_log(log)
            add_to_log_json("../data/watch_logs.json", content)
        # if it's type is rate
        if type == "rate":
            # parse content and add to json
            content = parse_rate_log(log)
            add_to_log_json("/home/rsong7/Team-4/data/rate_logs.json", content)

    if get_user:
        # call collect user and movie info from rest api and add to json
        user = get_user_info(content.get("userid"))
        add_to_info_json("../data/user_info.json", user, "user_id")
    
    if get_movie:
        movie = get_movie_info(content.get("movieid"))
        if movie != None:
            add_to_info_json("../data/movie_info.json", movie, "id")

def process_json(prefix, rating_filepath, userinfo_filepath, movieinfo_filepath):
    if not os.path.exists(prefix + rating_filepath):
        print ("No rating file!")
        return None
    
    rating_file = open(prefix + rating_filepath)
    rating_datas = json.load(rating_file)

    movie_file = open(prefix + movieinfo_filepath)
    movie_datas = json.load(movie_file)

    user_file = open(prefix + userinfo_filepath)
    user_datas = json.load(user_file)

    user_movie_rating_dict = []
    user_info_dict = []
    movie_info_dict = []
    for data in rating_datas["logs"]:
        if data["movieid"] not in movie_datas or data["userid"] not in user_datas:
            continue

        user_movie_rating_data = {}
        user_movie_rating_data["userid"] = int(data["userid"])

        user_movie_rating_data["movieid"] = data["movieid"]
        movie_info = movie_datas[data["movieid"]]
        user_movie_rating_data["tmdb_id"] = movie_info["tmdb_id"]
        user_movie_rating_data["popularity"] = float(movie_info["popularity"])
        user_movie_rating_data["vote_average"] = float(movie_info["vote_average"])
        user_movie_rating_data["rating"] = int(data["rating"])
        user_movie_rating_dict.append(user_movie_rating_data)


        user_info = user_datas[data["userid"]]
        user_info_data = {}
        user_info_data["userid"] = data["userid"]
        user_info_data["age"] = user_info["age"]
        user_info_data["occupation"] = user_info["occupation"]
        user_info_data["gender"] = user_info["gender"]
        user_info_dict.append(user_info_data)

        movie_info_data = {}
        movie_info_data["tmdbid"] = movie_info["tmdb_id"]
        movie_info_data["movieid"] = data["movieid"]
        movie_info_data["genres"] = 0 if len(movie_info["genres"]) == 0 else movie_info["genres"][0]["id"]
        movie_info_data["belongs_to_collection"] = 1 if movie_info["belongs_to_collection"] else 0
        movie_info_data["popularity"] = float(movie_info["popularity"])
        movie_info_data["vote_average"] = float(movie_info["vote_average"])
        movie_info_dict.append(movie_info_data)

    user_movie_rating_dict_columns = ["userid", "tmdb_id", "movieid", "popularity", "vote_average", "rating"]
    with open(prefix + "user_movie_rating.csv", "w+") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=user_movie_rating_dict_columns)
        writer.writeheader()
        writer.writerows(user_movie_rating_dict)
    csv_file.close()

    user_info_dict_columns = ["userid", "age", "occupation", "gender"]
    with open(prefix + "user_info.csv", "w+") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=user_info_dict_columns)
        writer.writeheader()
        writer.writerows(user_info_dict)
    csv_file.close()

    movie_info_dict_columns = ["tmdbid", "genres", "belongs_to_collection", "popularity", "vote_average"]
    with open(prefix + "movie_info.csv", "w+") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=movie_info_dict_columns)
        writer.writeheader()
        writer.writerows(movie_info_dict)
    csv_file.close()

# example on how to use some of the util methods for data collection
if __name__ == '__main__':
    amt_logs_collect = 1000000
    amt_logs_parse = 1000000# smaller amt so it doesn't take forever to parse through

    # file path for raw data from kafka stream
    raw_filepath = "/home/rsong7/Team-4/data/kafka_raw.csv"

    # creates csv file of {amt_logs_collect} kafka logs

    # rating_only = len(sys.argv) >= 2 and sys.argv[1] == "true"
    # get_log_file_from_kafka(raw_filepath, amt_logs_collect, rating_only)

    # string[] of kafka log data
    logs = get_logs_from_file(raw_filepath)
    # performs {action(log)} on each log up to {amt_logs_parse}

    for_each_log(logs[:amt_logs_parse], action)

    # path_prefix = "../data/"
    # rating_filepath = "rate_logs.json"
    # userinfo_filepath = "user_info.json"
    # movieinfo_filepath = "movie_info.json"

    # process_json(path_prefix, rating_filepath, userinfo_filepath, movieinfo_filepath)
    # remove all files in data folder
    # cleanup_data_folder()
