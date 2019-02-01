# Add API
import sys
sys.path.append("../../")
sys.path.append("../../api")


from api.globals import *
from api.positioning import *
from api.database import *

# Create database & GPS objects
db = Database(DATABASE_NAME)
db.prepare()
position = Positioning()

# Create function to save state
def saveState():
    print("SAVING")
    pos = position.getLatLng()
    db.put(pos.lat, pos.lng)

# Create button, activate
button = ButtonActionThread(BUTTON_PIN, saveState, CONFIRM_PITCH) # TODO: check pitch
button.activate()

# stay alive
while True:
    sleep(1)
