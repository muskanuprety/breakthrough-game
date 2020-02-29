# Work by Tamara Blagojevic and Muskan Uprety
import random
import copy
class Node(object):
    def __init__(self, state,level,parent=None):
        self.parent = parent
        self.child = []
        self.action = None 
        self.state = state
        self.utility = None
        self.level = level

    def get_parent(self):
        return self.parent
    def get_child(self):
        return self.child
    def get_action(self):
        return self.action
    def get_state(self):
        return self.state
    def get_utility(self):
        return self.utility
    def get_level(self):
        return self.level
    def set_level(self, n):
        self.level = n
    def set_child(self,listt):
        self.child=listt
    def set_utility(self, n):
        self.utility = n

    def utility_evasive(self):
        turrn = self.state.get_turn()
        if turrn == "white":
            x = len(self.state.get_white_list()) + random.random()
        if turrn == "black":
            x = len(self.state.get_black_list()) + random.random()
        self.utility = x



class Env_state():
    def __init__(self, board,turn):  # White is O and black is X
        self._board = board
        self._turn = turn

        self._row = len(self._board)
        self._column = len(self._board[0])

    def get_turn(self):
        return self._turn

    def get_row(self):
        return se;f._row

    def get_column(self):
        return self._column

    def get_black_list(self):
        black_list=[]
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                if self._board[i][j]=="X":
                    black_list.append((i,j))
        return black_list


    def get_white_list(self):
        white_list=[]
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                if self._board[i][j]=="O":
                    white_list.append((i,j))
        return white_list
       
    def get_board(self):
    	return self._board

    
    def get_legal_moves(self):
        legal_moves={}
        if self._turn=='white':
            for i in self.get_white_list():
                i_got_the_moves = []
                poss_one = (i[0]-1, i[1])
                poss_two = (i[0]-1, i[1]-1)
                poss_three = (i[0]-1, i[1]+1)

                if poss_one[0]>=0 and self._board[poss_one[0]][poss_one[1]]=='.' :
                    i_got_the_moves.append("UP")

                if poss_two[0]>=0 and poss_two[1]>=0 and (self._board[poss_two[0]][poss_two[1]]=='.' or self._board[poss_two[0]][poss_two[1]]=='X'):
                    i_got_the_moves.append("L")

                if poss_three[0]>=0 and poss_three[1] < self._column and (self._board[poss_three[0]][poss_three[1]]=='.' or self._board[poss_three[0]][poss_three[1]]=='X'):
                    i_got_the_moves.append("R")

                legal_moves[i]= i_got_the_moves

        if self._turn=='black':
            for i in self.get_black_list():
                i_got_the_moves = []
                poss_one = (i[0]+1, i[1])
                poss_two = (i[0]+1, i[1]-1)
                poss_three = (i[0]+1, i[1]+1)

                if poss_one[0]< self._row  and self._board[poss_one[0]][poss_one[1]]=='.' :
                    i_got_the_moves.append("UP")

                if poss_two[0]< self._row and  poss_two[1]>= 0 and (self._board[poss_two[0]][poss_two[1]]=='.' or self._board[poss_two[0]][poss_two[1]]=='O'):
                    i_got_the_moves.append("L")

                if poss_three[0]< self._row and poss_three[1]< self._column and (self._board[poss_three[0]][poss_three[1]]=='.' or self._board[poss_three[0]][poss_three[1]]=='O'):
                    i_got_the_moves.append("R")
                    
                legal_moves[i]= i_got_the_moves
        return legal_moves


def display_state(state):
    borad=state.get_board()
    for i in borad:
        print (" ".join(i))

def initial_state(row,column,pieces):
    board=[]
    for i in range(pieces):
        board.append(['X']*column)
    for i in range(row-2*pieces):
        board.append(['.']*column)
    for i in range(pieces):
        board.append(['O']*column)

    
    initial=Env_state(board,"white")
    display_state(initial)
    return initial


def transition(state,direction,loc_piece):
    last_board=copy.deepcopy(state.get_board())
    


    legal = state.get_legal_moves()
    if state.get_turn()=='white':

        if (direction=="L"):
            if direction in legal[loc_piece]:
                move=(loc_piece[0]-1, loc_piece[1]-1)
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='O'

        if (direction=="UP"):
            if direction in legal[loc_piece]:

                move=(loc_piece[0]-1, loc_piece[1])
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='O'
            

        if (direction=="R"):
            if direction in legal[loc_piece]:
                move=(loc_piece[0]-1, loc_piece[1]+1)
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='O'

        
        new_turn="black"



    if state.get_turn()=='black':
       
        if (direction=="L"):
            if direction in legal[loc_piece]:
                move=(loc_piece[0]+1, loc_piece[1]-1)
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='X'
            
        if (direction=="UP"):

            if direction in legal[loc_piece]:

                move=(loc_piece[0]+1, loc_piece[1])
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='X'
            

        if (direction=="R"):
            if direction in legal[loc_piece]:
                move=(loc_piece[0]+1, loc_piece[1]+1)
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='X'
            
        
        new_turn="white"

    new_state=Env_state(last_board,new_turn)

    return new_state


def da_goal(state):
    
    bb = state.get_board()
    row = state.get_row()
    if "X" in bb[0] :
        return True
    if  "O" in bb[len(bb)-1]:
        return True
    return False
        
    # turn = state.get_turn()
    # row = state.get_row()
    # if turn == "white":
    #     black = state.get_black_list()

    #     for i in black:
    #         if i[0] ==row-1:
    #             return True
    # if turn =="black":
    #     white = state.get_white_list()
    #     for i in white:
    #         if i[0] ==0:
    #             return True


def utility_evasive(state, turrn):
    
    if turrn == "white":
        x = len(state.get_white_list()) + random.random()
    if turrn == "black":
        x = len(state.get_black_list()) + random.random()
    return x


def utility_conquerer(state, turrn):
    
    if turrn == "white":
        x = (0 - len(state.get_black_list())) + random.random()
    if turrn == "black":
        x = (0 - len(state.get_white_list())) + random.random()
    return x


def utility_one(state, turrn):
    if turrn == "white":
        x = len(state.get_white_list())-len(state.get_black_list())
        for  i in state.get_white_list():
            if i[0]==0:
                x+=1000
    if turrn == "black":
        x = len(state.get_black_list())-len(state.get_white_list())
        for  i in state.get_black_list():
            if i[0]==state.get_row():
                x+=1000
    return (x+random.random())


def utility_two(state, turrn):
    if turrn == "white":
        util = 1000
        for i in state.get_white_list():
            util = util - i[0]
            if i[0]==0:
                util+=1000
        for i in state/get_black_list():
            util = util - i[0]
            if i[0]==state.get_row():
                util -=1000

    if turrn == "black":
        util = 1000
        for i in state.get_black_list():
            util = util + i[0]
            if i[0]==state.get_row():
                util+=1000
        for i in state/get_white_list():
            util = util + i[0]
            if i[0]==0:
                util -=1000
    return util 



def minimax(node, level): # level is 3
    front =[]
    expanded=[]
    node2expand = node
    current_level = 1
    front.append((node2expand, current_level))
    node2expand.set_level(0)
    #print(node2expand.get_level())
    goal_state = False
    while current_level < level:
        
        node2expand, current_level = front.pop(0)
        # if node2expand not in expanded:
        babies=[]
        legal_moves=node2expand.get_state().get_legal_moves()
        for loc,direct_list in legal_moves.items():

            for direct in direct_list:
                new_state=transition(node2expand.get_state(),direct,loc)
                #display_state(new_state)

                #print(new_state.get_turn())
                #print(new_state.get_legal_moves())
                new_node=Node(new_state,current_level, node2expand)

                #print(new_node.get_level())
                babies.append((new_node, current_level+1))
                # babies.append(new_node)
        node2expand.set_child(babies)
        front.extend(babies)
        expanded.append((node2expand, current_level))
    

    for leaf_node,j in expanded:        #assign utility value to leaf nodes
        if j==level:
            leaf_node.set_utility(utility_evasive(leaf_node.get_state(), leaf_node.get_state().get_turn()))
    
    for i,j in expanded:
        display_state(i.get_state())
        print(j)
        print('-------')

    temp = level
    temp = temp-1                       # working my way up

    while temp>=0:
        for i,j in expanded:
            display_state(i.get_state())
            if j == temp:
                if j%2==0:              #this is max
                    baby_list = i.get_child()
                    max(i.get_child())      
                else:                   # this is min
                    min(i.get_child())      

            


if __name__=="__main__":
    root_state=initial_state(3,3,1)
    root_node=Node(root_state,0)
    minimax(root_node,3)







