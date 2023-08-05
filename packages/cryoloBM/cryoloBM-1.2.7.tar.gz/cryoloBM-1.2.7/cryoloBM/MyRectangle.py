from matplotlib.patches import Rectangle


class MyRectangle(Rectangle):
    def __init__(self, xy, width, height, angle=0.0, **kwargs):
        self.confidence = None
        super(MyRectangle, self).__init__(xy, width, height, angle, **kwargs)

    def set_confidence(self,confidence):
        self.confidence = confidence
