import cv2

class Cap_mock():
	def __init__(self):
		print("Init cap mock")
		self.image = cv2.imread('./testCam2.jpg')

	def read(self):
		print("Cap mock: read")
		return 0, self.image

	def copy(self):
		print("Cap mock: copy")
		return cv2.imread('./testCam2.jpg')
