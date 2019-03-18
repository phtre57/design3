

INCREMENT = 30


class PathSmoother:

    def __init__(self, path):
        self.path = path
        self.smoother_path = []

    def smooth_path(self):
        i = 0
        for point in self.path:
            if i % INCREMENT == 0:
                self.smoother_path.append((point[0], point[1]))
            i = i + 1

        return self.smoother_path
