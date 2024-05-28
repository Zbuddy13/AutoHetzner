from datetime import date
import time
import os
import json
import requests
import subprocess

from hcloud import Client

from apscheduler.schedulers.blocking import BlockingScheduler


os.environ['TZ'] = 'America/New_York'

# For docker
# API TOKEN
apiToken = os.environ.get('token', "ErHvNPcU0xFR9UuxIiEJrtfhFrHx86pznrWRqYjVSoskOnFZbVOLhxS3BYYQb2Ku")
# Snapshot History
noOfSnapshotsKept = os.environ.get('snapshothistory', 4)
# Sleep variable
sleep = os.environ.get('sleep', 8)

#API Variables
jsondata = ""
url = os.environ.get('url', "http://127.0.0.1:2500/recieve")


# Todays date and time string
def getTime():
    now = time.localtime()
    current_time = time.strftime("%H:%M:%S", now)
    currentDateTime = str(date.today()) + " " + str(current_time) # Todays Date
    return currentDateTime

# Create all snapshots for servers
def createAllSnapshots(serverInfo, currentDateTime, client):
    for name in serverInfo: # Create images of servers
        nameAndTimeString = str(name.id) + ' ' + name.name + " at " + currentDateTime
        snapshotName = name.name + " at " + currentDateTime
        print("Starting image of " + nameAndTimeString)
        response = client.servers.create_image(server=name, description=snapshotName)
        if (len(str(response)) != 0):
            print("Success creating image for " + name.name)

# Delete all snapshots unwanted
def deleteAllSnapshots(image, serverNames, clientIn):
    if (len(clientIn.images.get_all(type="snapshot")) < len(serverNames)*int(noOfSnapshotsKept)): return
    if (len(clientIn.images.get_all(type="snapshot")) >= (len(serverNames)*int(noOfSnapshotsKept)+len(serverNames))):
        i=0
        for name in image:
            if(not name):
                print("Error deleting, does not exist")
            else:
                clientIn.images.delete(name)
                print("Image" + str(name) + "deleted")
                i+=1
            if(i == len(serverNames)): break

def createTestServer(serverNames, images, client): # enter serverNames[0] for first server
    response = client.servers.create(name = ("Test "+str(serverNames[0].name)), image=images[0], server_type=
                        client.server_types.get_by_name(serverNames[0].name))
    print(str(response))

# Protect all snapshots
def protectAllSnapshots(method, client):
    imagesToProtect = client.images.get_all(type="snapshot")
    for name in imagesToProtect:
        response = client.images.change_protection(name, delete=method)
    if(method):
        print("Locked images")
    else:
        print("Unlocked images")

# Run all commands above to create and delete snapshots
def runSnapshot():
    success = 0
    while(success == 0):
        dateTime = getTime()
        # Get the servers
        clientvar = Client(token=apiToken)
        # Pull server object
        serverNamesList = clientvar.servers.get_all() # Pull names via bound object for them all (boundserver)
        # Array of old times and dates
        images = clientvar.images.get_all(type="snapshot")
        # Run functions
        protectAllSnapshots(False, clientvar)
        print("Unprotect Snapshot Run")
        createAllSnapshots(serverNamesList, dateTime, clientvar)
        print("Snapshot Created")
        deleteAllSnapshots(images, serverNamesList, clientvar)
        print("Protect Snapshot Delete")
        protectAllSnapshots(True, clientvar)
        print("Protected all snapshots")
        apiSend({"Ran at ": dateTime}, url)
        success = 1

###########################################################
# Api for Discord
###########################################################

def apiSend(data, url):
    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        print("Data sent successfully!")
    else:
        print(f"Error sending data: {response.text}")

# Run program one time
runSnapshot()

#var = settings.snapshotStatus
#data = { 
          #  "Modules" : var, 
         #   "Subject" : "Data Structures and Algorithms", 
        #} 
# Get the servers
#client = Client(token=apiToken)
#serverNamesList = client.servers.get_all()
#images = client.images.get_all(type="snapshot")
#deleteAllSnapshots(images, serverNamesList, client)

# Run Job every _ hours
scheduler = BlockingScheduler()
scheduler.add_job(runSnapshot,'interval', hours=int(sleep))
scheduler.start()