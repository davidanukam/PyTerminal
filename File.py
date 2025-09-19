class File:
    def __init__(self, name, parent=None, time_made=None, size=0):
        self.name = name
        self.parent = parent
        self.time_made = time_made
        self.size = size