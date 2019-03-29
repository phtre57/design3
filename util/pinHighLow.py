from infrastructure.communication_pi.comm_pi import *


comm_pi = Communication_pi()


while True:
    com = input("Enter command: ")

    if com == "high":
        comm_pi.changeCondensateurHigh()

    if com == "low":
        comm_pi.changeCondensateurLow()

    if com == "tension":
        comm_pi.getTension()

    if com == "angle":
        angle = input("Enter wanted angle: ")
        angle = int(angle)
        comm_pi.sendAngle(angle)

    if com == "quit":
        break


