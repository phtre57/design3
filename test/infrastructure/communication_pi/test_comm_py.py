import time
from infrastructure.communication_pi import comm_pi

comm_pi.connectToPi()
time.sleep(5)

start = time.time()

switch = True

while switch:

    comm_pi.sendCoordinates("390,0\n")
    time.sleep(5)

    comm_pi.sendCoordinates("0,381\n")
    time.sleep(5)

    comm_pi.sendCoordinates("-390,0\n")
    time.sleep(5)

    comm_pi.sendCoordinates("0,-381\n")
    time.sleep(5)

    end = time.time()

    if end - start > 240:
        switch = False



