# Import modules
import time
from CarAPI import CarApi


print("Testing ultrasonic sensor (30 reads)")
api = CarApi()
api.startContDistMeas()

for i in range(30):
    time.sleep(0.5)
    print(api.getLastDistance())

api.stopContDistMeas()
print("Test ended")
