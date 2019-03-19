class Communication_pi_mock():
	def __init__(self):
		print("Init communication mock")

	def connectToPi(self):
		print("Communication mock: connect")

	def getImage(self):
		print("Communication mock: getImage")

	def sendCoordinates(self, str):
		print("Communication mock: sendCoordinates ## " + str)

	def disconnectFromPi(self):
		print("Communication mock: disconnect")

	def robotReady(self):
		print("Communication mock: robotReady")

	def changeCondensateur(self):
		print("Communication mock: changeCondensateur")