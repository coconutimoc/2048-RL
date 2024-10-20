"""
DGT(Dynamic Game Tree) is a data structure that simulate the game tree in a game of one or multiple players.
The root of tree is updated by the current status of the game, with tree growing dynamically.
The level tree grows is calculated by function level() according to game status.

The structure of DGT:
tree = [[possibility, status, player], {
            action1:[[p1, s1, next(player)], {
                        action1: ...,
                        action2: ...}, 
                        ...], 
                    [p2, s2, next(player)], {
                        action1: ...,
                        action2: ...}, 
                        ...], 
                    ...]
            action2:...
        }
        ]
"""
# import the gameboard
# the name of gameboard class is self-defined, but should be imported as gameboard in this file
from gameboard import gameboard as gameboard

class DGT:
    def __init__(self, root_status:list, players_and_actions:dict, action_order:list):
        """
        root_status: the current status of the game
        players_and_actions: the players and the actions they can take
            {player1: [action1, action2, ...], player2: [action1, action2, ...], ...}
        action_order: the order of the actions
          [player1, player2, ...]
        """
        self.tree = [[1,root_status,action_order[0]]]
        self.actions = players_and_actions
        self.next = {}
        for order in range(len(action_order)):
            self.next[action_order[order]] = action_order[(order+1)%len(action_order)]
        self.grow(self.tree,self.level())

    def level(self):
        """calculate the ideal level of tree dynamically"""
        level = 0
        return len(self.actions)*level
    
    def watch(self,game_log):
        """watch other player's action and record in self."""
        return game_log[len(game_log)-len(self.actions):]
    
    def is_leaf(self, tree):
        """check if the tree is a leaf"""
        return len(tree) == 1

    def change_root(self):
        """change the root of the tree according to the game log"""
        for gamestatus,player,action in self.game_log:
            assert player == self.tree[0][2],"Player unmatched."
            for tree in self.tree[1][action]:
                if tree[0][1] == gamestatus:
                    tree[0][0] = 1
                    self.tree = tree
                    break
    
    def grow(self, tree, level:int):
        """grow the tree"""
        player = tree[0][2]
        if level == 0:
            return tree
        if not self.is_leaf(tree):
            for action in self.actions[player]:
                for child in tree[1][action]:
                    self.grow(child, level-1)
        else:
            action_outcomes = {}
            for action in self.actions[player]:
                current_gameboard = gameboard(tree[0][1])
                outcomes = current_gameboard.possible_outcomes(player,action)
                action_outcomes[action]=[self.grow([outcome.append(self.next[player])],level-1) for outcome in outcomes]
            tree.append(action_outcomes)

    def update(self):
        """update the tree"""
        self.change_root()
        self.grow(self.tree,self.level())
        pass