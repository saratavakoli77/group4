# Team-4

### Notes:
- requirements.txt in docker does not seem to be working. Would be good idea to keep track on what is `pip install`d in order to add to the `Dockerfile`
- in order to start api server, all files imported under data_collection must have `data_collection.` before the imported file's name.
- `main.py` not meant to be ran under api, is meant to be an example on how to use the other util files under data_collection. `main.py` must be ran under `data_collection` directory.

### Setup for dev:
Install python requirements

`pip3 install flask kafka-python requests`

Start kafka stream

`docker run -it --log-opt max-size=50m --log-opt max-file=5 bitnami/kafka kafka-console-consumer.sh --bootstrap-server fall2022-comp585.cs.mcgill.ca:9092 --topic movielog4 --from-beginning`

### How to start API server:
Build and run docker container
`docker build -t "movierecc4:1.0" .`
`docker run -d -p 8083:8083 movierecc4:1.0`

Get movie reccomendations for user_id
`curl fall2022-comp585-4.cs.mcgill.ca:8083/recommend/{user_id}`

Find docker container id
`docker container ls`

Stop docker container
`docker stop {container_id}`
