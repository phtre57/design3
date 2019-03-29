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

    if com == "quit":
        break


