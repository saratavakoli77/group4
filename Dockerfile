# FROM ubuntu:18.04

# RUN useradd -ms /bin/bash -g root -G sudo user1

# RUN apt-get update
# RUN apt-get install python3 -y
# RUN apt-get install python3-pip -y

# USER user1
# WORKDIR /home/user1

# COPY api.py .
# RUN mkdir -p data_collection
# COPY data_collection ./data_collection
# RUN mkdir -p data

# # COPY requirements.txt .

# RUN echo '#!/bin/bash' > api_run.sh
# RUN echo 'pip3 install flask' >> api_run.sh
# RUN echo 'pip3 install kafka-python' >> api_run.sh
# RUN echo 'pip3 install requests' >> api_run.sh
# # RUN echo 'pip3 install -r requirements.txt' >> api_run.sh
# RUN echo 'python3 api.py' >> api_run.sh

# RUN chmod +x api_run.sh

# EXPOSE 8083

# CMD /home/user1/api_run.sh


FROM python:3.9

WORKDIR /app

COPY . .

RUN pip3 install flask kafka-python requests pathlib torch
# RUN pip3 install -r requirements.txt

EXPOSE 8083

CMD [ "python3", "api.py" ]