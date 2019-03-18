class Color():

    def __init__(self):
        self.color = 0

    def RED(self):
        self.color = 1
        self.color_code = ([0, 0, 170], [255, 110, 255])

    def GREEN(self):
        self.color = 2
        # self.color_code = ([0, 119, 0], [122, 255, 28])
        self.color_code = ([0, 120, 0], [151, 255, 127])

    def BLUE(self):
        self.color = 3
        self.color_code = ([130, 49, 0], [255, 255, 65])

    def YELLOW(self):
        self.color = 4
        self.color_code = ([4, 11, 234], [255, 255, 255])