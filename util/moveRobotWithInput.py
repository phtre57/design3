from infrastructure.communication_pi.comm_pi import *

comm_pi = Communication_pi()

while True:

    command = input()

    if "w":
        comm_pi.sendCoordinates(10, 0)

    if "s":
        comm_pi.sendCoordinates(-10, 0)

    if "d":
        comm_pi.sendCoordinates(0, 10)

    if "a":
        comm_pi.sendCoordinates(0, -10)

    if "q":
        comm_pi.sendAngle(-2)

    if "e":
        comm_pi.sendAngle(2)