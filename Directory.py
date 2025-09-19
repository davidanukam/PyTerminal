class Directory:
    def __init__(self, name, parent=None, time_made=None, size=0):
        self.name = name
        self.children = []
        self.parent = parent
        self.time_made = time_made
        self.size = size