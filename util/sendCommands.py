from infrastructure.communication_pi.comm_pi import *

comm_pi = Communication_pi()

while True:
    com = input("Enter command: ")

    if com == 'image':
        comm_pi.getImage()

    if com == 'imageHD':
        comm_pi.getImageFullHD()

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

    if com == "coord":
        x = input("Enter wanted x: ")
        y = input("Enter wanted y: ")
        comm_pi.sendCoordinates(int(x), int(y))

    if com == "up_bras":
        comm_pi.moveArm('2000')

    if com == "redOn":
        comm_pi.redLightOn()

    if com == "redOff":
        comm_pi.redLightOff()

    if com == "quit":
        break
