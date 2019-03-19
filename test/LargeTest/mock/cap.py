import cv2

class Cap_mock():
	def __init__(self):
		print("Init cap mock")

	def read(self):
		print("Cap mock: read")
		return 0, cv2.imread('./testCam.jpg')