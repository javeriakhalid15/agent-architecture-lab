class Displayable:
    """Base class for objects that can display information"""
    
    def __init__(self):
        self.display_level = 1

    def display(self, level, *args, **kwargs):
        if self.display_level >= level:
            print(*args, **kwargs)