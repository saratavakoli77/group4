import requests
import json

import json
import os
from pathlib import Path

# creates json file (initialized with inital_json) at filepath if doesn't exist
def json_file_not_exist_create(filepath, inital_json):
    if not (os.path.isfile(filepath) and os.access(filepath, os.R_OK)):
        json_object = json.dumps(inital_json, indent=4)
        with open(filepath, "w") as outfile:
            outfile.write(json_object)

user_info_url = "http://fall2022-comp585.cs.mcgill.ca:8080/user/"
movie_info_url = "http://fall2022-comp585.cs.mcgill.ca:8080/movie/"

# adds obj to info json
def add_to_info_json(filepath, json_item, index):
    json_file_not_exist_create(filepath, {})
    
    with open(filepath,'r+') as file:
        file_data = json.load(file)
        file_data.update({str(json_item[index]): json_item})
        file.seek(0)
        json.dump(file_data, file, indent = 4)
    
        file.close()

# get request to provided {url} for {id}
def get_info_from_rest(url, id):
    type = url.rsplit('/', 2)[1]
    url = url+str(id)
    filepath = "../data/"+type+'_info.json'
    response = requests.get(url)
    json_item = response.json()

    return json_item

# gets info of {id} user
def get_user_info(id):
    return get_info_from_rest(user_info_url, id)

# gets info of {id} movie
def get_movie_info(id):
    movie = get_info_from_rest(movie_info_url, id)
    if movie == {'message': 'movie not found'}:
        return None
    return movie
