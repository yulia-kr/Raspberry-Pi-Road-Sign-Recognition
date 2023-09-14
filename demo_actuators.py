# Import modules
import time
from CarAPI import CarApi


print("Testing motor and servo")
api = CarApi()

# STEERING
# Steer from left to right
api.setSteeringAngle(-100)
time.sleep(0.4)

for perc in range(-100, 100, 3):
    api.setSteeringAngle(perc)
    time.sleep(0.03)
time.sleep(0.4)

# Leave steering in the middle
api.setSteeringAngle(0)


# MOTOR
# Drive motor forward and backwards
time.sleep(0.5)
api.setMotorPower(70)
time.sleep(2.5)
api.setMotorPower(0)

time.sleep(0.4)
api.setMotorPower(-65)
time.sleep(2.5)
api.setMotorPower(0)

print("Test ended")
