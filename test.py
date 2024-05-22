from datetime import date
import time
import hcloud
import os
import asyncio
import apscheduler

from apscheduler.schedulers.blocking import BlockingScheduler

from hcloud import Client
from hcloud.images import Image
from hcloud.server_types import ServerType

# API TOKEN
apiToken = os.environ.get('token', "")
# Snapshot History
noOfSnapshotsKept = os.environ.get('snapshothistory', 2)
# Sleep variable
sleep = os.environ.get('sleep', 8)

def deleteAllSnapshots(image, serverNames, clientIn):
    if (len(clientIn.images.get_all(type="snapshot")) < len(serverNames)*int(noOfSnapshotsKept)): return
    if (len(images) >= (len(serverNames)*int(noOfSnapshotsKept)+len(serverNames))):
        i=0
        for name in image:
            if(not name):
                print("Error deleting, does not exist")
            else:
                clientIn.images.delete(name)
                print("Image" + str(name) + "deleted")
                i+=1
            if(i == len(serverNames)): break


# Get the servers
clientvar = Client(token=apiToken)
# Pull server object
serverNamesList = clientvar.servers.get_all() # Pull names via bound object for them all (boundserver)
# Array of old times and dates
images = clientvar.images.get_all(type="snapshot")

deleteAllSnapshots(images, serverNamesList, clientvar)

#print(len(clientvar.images.get_all(type="snapshot")))
#print((len(serverNamesList)*int(noOfSnapshotsKept)+len(serverNamesList)))
#print(images)
#print(len(clientvar.images.get_all(type="snapshot")) == (len(serverNamesList)*int(noOfSnapshotsKept)+len(serverNamesList)))