import time
from infrastructure.communication_pi import comm_pi

comm_pi.connectToPi()
time.sleep(5)

switch = True

while switch:

    """
    comm_pi.sendCoordinates("390,0\n")
    time.sleep(5)

    comm_pi.sendCoordinates("0,381\n")
    time.sleep(5)

    comm_pi.sendCoordinates("-390,0\n")
    time.sleep(5)

    comm_pi.sendCoordinates("0,-381\n")
    time.sleep(5)
    """

    coord = input("Coord:")
    print(coord)

    if coord == "end":
        switch = False
        break

    comm_pi.sendCoordinates(coord + "\n")
    time.sleep(5)