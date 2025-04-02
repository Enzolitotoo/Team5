class Tree:
    #This part define the data structure
    def __init__(self, state, move=None, parent=None, is_max=True):
        self.state = state # state = state because a child inheritate its state from its parent and then modifiy it
        self.parent = parent # to remember who is the parent of the noce that are being expand
        self.move = move # To remember which move as been done to get to the state
        self.is_max = is_max  # True = Max (odd), False = Min (even)
        self.children = [] # List the children of the current node
        self.visited_nodes = 0
        
    def add_child(self, move, child_node):
        self.children.append(child_node) # Add the node into the list of children of the current node

    def possible_moves(self):
        number = self.state['number']
        return [i for i in range(2, 6) if number % i == 0] # Define the possibles moves that can be done from a node

    def Minmax_leaf_value(self):
        # MinMax Value definition
        if self.state['score'] % 2 == 0: # If the score is even then the Final score is score - Bank and the oposit if the score is odd
            Final_score = self.state['score'] - self.state['Bank']
        else:  # if odd then add the bank to the score
            Final_score = self.state['score'] + self.state['Bank']
        if Final_score % 2 == 0:
            self.state['MinMax_ana'] = -1 #determine who wins if it's odd then a +1 (for the first player) value is given 
        else:
            self.state['MinMax_ana'] = 1 #determine who wins if it's odd then a -1 (for the second player) value is given 

    def expand(self, depth=0, max_depth=10):
        """Développe l'arbre en appliquant Minimax."""
        if depth >= max_depth:
            return
        self.visited_nodes += 1
        possible_moves = self.possible_moves()

        if not possible_moves:  # Reached leaf
            self.Minmax_leaf_value()
            return

        for i in possible_moves: # Main difference with the alpha beta pruning we give the value of the new state in the expand function
            numbr = self.state['number'] // i # definition of the state
            new_state = {
                'number': numbr,
                'score': self.state['score'],
                'Bank': self.state['Bank'],
                'MinMax_ana': 0
            }

            if numbr % 10 == 5 or numbr % 10 == 0:
                new_state['Bank'] += 1
            if numbr % 2 == 0:
                new_state['score'] = new_state['score'] - 1  
            if numbr % 2 == 1:
                new_state['score'] += 1

            child_node = Tree(new_state, move=i, parent=self, is_max=not self.is_max) # First we call the Class Tree to add the node to the Tree
            self.add_child(i, child_node) # We add the node to the node list of the current analize node
            child_node.expand(depth=depth + 1, max_depth=max_depth) # We expend this node to check if it got any child itself

        # Apply MinMax
        if self.is_max:
            self.state['MinMax_ana'] = max(child.state['MinMax_ana'] for child in self.children)
        else:
            self.state['MinMax_ana'] = min(child.state['MinMax_ana'] for child in self.children)

    def best_move(self):
        # Look for the best move depending on the value of min max for the children
        if self.is_max:
            best_child = max(self.children, key=lambda child: child.state['MinMax_ana'])
        else:
            best_child = min(self.children, key=lambda child: child.state['MinMax_ana'])
        return best_child.move

    def count_node(self, level=0, i = 0):
        node_count = 1  # Start with 1 for the current node
        for child in self.children:
            node_count += child.count_node(level + 1, i + 1)  # Recursively count nodes
        return node_count

# Code Made By Enzo Kerebel
