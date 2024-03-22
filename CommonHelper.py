
class CommonHelper:
    @staticmethod
    def readQss(style):
        with open(style,'r') as f:
            return f.read()

