# Add API
import sys
sys.path.append("./")
sys.path.append("./api")

from api.globals import *
from api.positioning import *
from api.database import *
from api.button import *
from multiprocessing import Queue

# Create database & GPS objects
db = Database(DATABASE_NAME)
db.prepare()

count = 0

# Create function to save state
def saveState():
    global count
    print("SAVING")
    pos = getLatLng()
    print(pos)
    db.put(pos["lat"], pos["lng"])
    count += 1

# Create button, activate
button = ButtonActionThread(BUTTON_PIN, saveState, CONFIRM_PITCH) # TODO: check pitch
button.activate()

# stay alive
while count < 4:
    sleep(1)
