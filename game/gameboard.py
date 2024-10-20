"""
immitates the game board
"""

class gameboard:
    def __init__(self,current=None):
        if current:
            self.board = current
        pass

    def possible_outcomes(self,player,action):
        """return the possible outcomes of the action
        [[possibility1, status1], [possibility2, status2], ...]
        """
        return []
    
    def status(self):
        """return the current status of the game"""
        pass

    def print(self):
        """print the game board"""
        pass