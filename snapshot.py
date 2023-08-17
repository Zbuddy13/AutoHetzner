from datetime import date
import time
import hcloud
import os

from hcloud import Client
from hcloud.images import Image
from hcloud.server_types import ServerType



# Todays date and time string
now = time.localtime()
current_time = time.strftime("%H:%M:%S", now)
currentDateTime = str(date.today()) + " " + str(current_time) # Todays Date

# API TOKEN
apiToken = os.environ.get('token', None)

# Snapshot History
noOfSnapshotsKept = os.environ.get('snapshothistory', 3)

# Get the servers
client = Client(token=apiToken)

# Pull server object
serverNames = client.servers.get_all() # Pull names via bound object for them all (boundserver)

# Array of old times and dates
images = client.images.get_all(type="snapshot")

def createAllSnapshots(serverInfo):
    for name in serverInfo: # Create images of servers
        nameAndTimeString = str(name.id) + ' ' + name.name + " at " + currentDateTime
        snapshotName = name.name + " at " + currentDateTime
        print("Starting image of " + nameAndTimeString)
        response = client.servers.create_image(server=name, description=snapshotName)
        if (len(str(response)) != 0):
            print("Success creating image for " + name.name)

#Find a way for it to wait till new images are created
def deleteAllSnapshots(image):
    while True:
        if (len(client.images.get_all(type="snapshot")) == len(serverNames)*noOfSnapshotsKept): break
        elif (len(client.images.get_all(type="snapshot")) < len(serverNames)*noOfSnapshotsKept): return
    i=0
    for name in image:
        if(not name):
            print("Error deleting, does not exist")
        else:
            client.images.delete(name)
            print("Image" + str(name) + "deleted")
            i+=1
        if(i == len(serverNames)): break

def createTestServer(): # enter serverNames[0] for first server
    response = client.servers.create(name = ("Test "+str(serverNames[0].name)), image=images[0], server_type=
                          client.server_types.get_by_name(serverNames[0].name))
    print(str(response))
    
def protectAllSnapshots(method):
    imagesToProtect = client.images.get_all(type="snapshot")
    for name in imagesToProtect:
        response = client.images.change_protection(name, delete=method)
    if(method):
        print("Locked images")
    else:
        print("Unlocked images")
        

# Call the all snapshots function
protectAllSnapshots(False)
createAllSnapshots(serverNames)
deleteAllSnapshots(images)
protectAllSnapshots(True)
#createTestServer()

#print("Test"+str(images[0]))
