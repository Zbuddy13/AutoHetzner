FROM --platform=linux/amd64 python:3.10.11-alpine3.17 as build

LABEL AUTHOR=ZBUDDY

RUN pip3 install --upgrade pip
RUN pip3 install hcloud
RUN pip3 install apscheduler
RUN apk update
RUN apk upgrade

WORKDIR /app
COPY . .

#Token variable
ENV token="TOKEN"
ENV snapshothistory="NUMBER"
ENV sleep="SLEEP"

#Run the main program
CMD [ "python3", "snapshot.py" ]

#Compile on mac
#sudo docker build . -t zbuddy19/autohetzner:
#docker push zbuddy19/autohetzner:tagname