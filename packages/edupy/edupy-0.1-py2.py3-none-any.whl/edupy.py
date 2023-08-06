""" An package for Education """

__version__ = "0.1"


from random import choice
class Die:
    def __init__(self, faces=None):
        self.faces = faces

    def roll(self):
        print(choice(self.faces))


if __name__ == "__main__":
    die = Die(["+", "-", "×", "÷"])
    die.roll()
    die.roll()
