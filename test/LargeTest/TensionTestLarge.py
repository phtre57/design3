from infrastructure.communication_pi.__comm_pi import *


def test():
    comm_pi = Communication_pi()
    comm_pi.connectToPi()
    time.sleep(3)

    tension = comm_pi.getTension()

    print("Tension: " + str(tension))

    comm_pi.disconnectFromPi()


test()