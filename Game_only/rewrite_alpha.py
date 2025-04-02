class Tree_A:
    def __init__(self, state, move=None, parent=None, is_max=True):
        self.state = state # state = state because a child inheritate its state from its parent and then modifiy it
        self.parent = parent # to remember who is the parent of the noce that are being expand
        self.move = move # To remember which move as been done to get to the state
        self.is_max = is_max  # True = Max (odd), False = Min (even)
        self.children = [] # List the children of the current node

    def add_child(self, move, child_node):
        self.children.append(child_node) # Add the node into the list of children of the current node

    def possible_moves(self):
        number = self.state['number']
        return [i for i in range(2, 6) if number % i == 0]  # Define the possibles moves that can be done from a node

    def Minmax_leaf_value(self):
        # MinMax Value definition
        if self.state['score'] % 2 == 0:  # If the score is even then the Final score is score - Bank and the oposit if the score is odd
            Final_score = self.state['score'] - self.state['Bank']
        else:  # if odd then add the bank to the score
            Final_score = self.state['score'] + self.state['Bank']
        
        self.state['MinMax_ana'] = 1 if Final_score % 2 == 1 else -1 #Choose who wins if it's odd then a +1 (for the first player wins) value is given else -1 (for the second player win) is given

    def expand(self, alpha=float('-inf'), beta=float('inf')):
        possible_moves = self.possible_moves()

        if not possible_moves:  # Reached leaf
            self.Minmax_leaf_value()
            return self.state['MinMax_ana']

        if self.is_max:
            max_eval = float('-inf')  # Negative infinite value for the alpha value
            for i in possible_moves:
                new_state = self.new_state_g(i)
                child_node = Tree_A(new_state, move=i, parent=self, is_max=False)
                self.add_child(i, child_node)
                eval_value = child_node.expand(alpha, beta)
                max_eval = max(max_eval, eval_value)
                alpha = max(alpha, eval_value)
                
               # if max_eval == 1: # not obligatory
                #    break
                
                if beta <= alpha: # Make the cut for the alpha beta 
                    break
                
            self.state['MinMax_ana'] = max_eval
            return max_eval
        
        else:
            min_eval = float('inf')  # Positive infinite value for the beta value
            for i in possible_moves:
                new_state = self.new_state_g(i)
                child_node = Tree_A(new_state, move=i, parent=self, is_max=True)
                self.add_child(i, child_node)
                eval_value = child_node.expand(alpha, beta)
                min_eval = min(min_eval, eval_value)
                beta = min(beta, eval_value)
                
              #  if min_eval == -1:
               #     break
                
                if beta <= alpha: # base of the Alpha prunning
                    break
                
            self.state['MinMax_ana'] = min_eval
            return min_eval

    def new_state_g(self, move): # We create a specific function for it in order to get a more understandable code 
        if move == 0:
            raise ValueError("Division par zéro détectée dans new_state_g()")
        
        numbr = self.state['number'] // move
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
        
        return new_state

    def best_move(self): # Apply Min_max algorithm
        if not self.children:
            return None  # If there are no possible move (if it's a leaf)
        
        if self.is_max: 
            best_child = max(self.children, key=lambda child: child.state['MinMax_ana'])
        else:
            best_child = min(self.children, key=lambda child: child.state['MinMax_ana'])
        
        return best_child.move
    
    def count_node(self, level=0):
        node_count = 1  # Start with 1 for the current node
        for child in self.children:
            node_count += child.count_node(level + 1)  # Recursively count nodes
        return node_count

# Code Made By Enzo Kerebel
