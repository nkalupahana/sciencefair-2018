import sys
sys.path.append("../../")
sys.path.append("../../api")

from time import sleep
from multiprocessing import Queue
from api.positioning import *

q = Queue()
while True:
    print(q.get())
