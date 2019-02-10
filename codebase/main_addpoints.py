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

# Create function to save state
def saveState():
    print("SAVING")
    pos = getLatLng()
    print(pos)
    db.put(pos["lat"], pos["lng"])

# Create button, activate
button = ButtonActionThread(BUTTON_PIN, saveState, CONFIRM_PITCH)
button.activate()

# stay alive
while len(["y" for thing in db.getPoints()]) < 4:
    sleep(1)

button.playTone(CONFIRM_PITCH + 10)
button.playTone(CONFIRM_PITCH + 10)
