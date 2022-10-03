from kafka import KafkaConsumer
import json
import csv
import math
import random

server = 'fall2022-comp585.cs.mcgill.ca:9092'
topic = 'movielog4'

import json
import os
from pathlib import Path

# creates json file (initialized with inital_json) at filepath if doesn't exist
def json_file_not_exist_create(filepath, inital_json):
    if not (os.path.isfile(filepath) and os.access(filepath, os.R_OK)):
        json_object = json.dumps(inital_json, indent=4)
        with open(filepath, "w") as outfile:
            outfile.write(json_object)

# adds kafka log obj to json
def add_to_log_json(filepath, new_log):
    json_file_not_exist_create(filepath, {"logs": []})

    with open(filepath,'r+') as file:
        file_data = json.load(file)
        file_data["logs"].append(new_log)
        file.seek(0)
        json.dump(file_data, file, indent = 4)
        file.close()

# gets kafka consumer
def get_consumer():
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=server,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: x.decode('utf-8')
    )

    return consumer

# parses watch log
def parse_watch_log(log):
    log_data = log.split(",")
    split_mpg = log_data[2].rsplit("/", 2)
    movieid = split_mpg[-2]
    minute = split_mpg[-1].replace(".mpg", "")

    new_log = {
        "time": log_data[0],
        "userid": log_data[1],
        "movieid": movieid,
        "minute": minute
    }

    return new_log

# parses rate log
def parse_rate_log(log):
    log_data = log.split(",")
    split_path = log_data[2].rsplit("/", 1)[1].split("=")
    movieid = split_path[0]
    rating = split_path[1]

    new_log = {
        "time": log_data[0],
        "userid": log_data[1],
        "movieid": movieid,
        "rating": rating
    }
    
    return new_log

# gets log type from log (as string)
def get_log_type(log):
    log_data = log.split(",")
    watching = log_data[2].startswith("GET /data/")
    rating = log_data[2].startswith("GET /rate/")
    
    if watching:
        return "watch"
    elif rating:
        return "rate"
    else:
        return "request"

# gets string[] of logs from filepath
def get_logs_from_file(filepath):
    # df = pd.read_csv(f'../data/{filepath}')
    kafka_stream = open(filepath, "r").read().split("\n")
    rows = kafka_stream[0:]
    random.shuffle(rows)
    kafka_stream = rows
    return kafka_stream

# gets {amount} of logs from kafka stream and inserts into {filepath}
def get_log_file_from_kafka(filepath, amount, rating_only):
    print("Begin kafka log collection")
    consumer = get_consumer()
    curr = 0
    
    with open (filepath,'w+') as data_file:
        csv_writer = csv.writer(data_file)
        
        for log in consumer:
            log_data = log.value.split(",")
            if rating_only and len(log_data) > 2 and "/rate/" not in log_data[2]:
                continue
            csv_writer.writerow(log_data)
            curr += 1

            if curr % (amount/100) == 0:
                print(str(math.floor((curr/amount)*100)) + "%")

            if curr >= amount:
                break

        data_file.close()
    
    print("{amount} logs collected in {filepath}".format(amount=amount, filepath=filepath))

# does {action} for each log in {logs}
def for_each_log(logs, action):
    print("Start action on logs")
    total_count = len(logs)
    curr = 0

    for log in logs:
        if log == "":
            continue
        
        action(log)
        curr += 1

        if curr % (total_count/100) == 0:
            print(str(math.floor((curr/total_count)*100)) + "%")

    print("Completed action on {total_count} logs".format(total_count=total_count))