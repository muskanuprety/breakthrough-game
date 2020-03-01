
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
        self.direction=None
        self._row = len(self._board)
        self._column = len(self._board[0])

    def get_turn(self):
        return self._turn

    def get_row(self):
        return self._row

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
    def get_direction(self):
        return self.direction
    
    def set_direction(self,d):
        self.direction=d
    
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
    
    return initial


def transition(state,direction,loc_piece):
    last_board=copy.deepcopy(state.get_board())
    

    move=None
    legal = state.get_legal_moves()
    if state.get_turn()=='white':

        if (direction=="L"):
            if direction in legal[loc_piece]:
                move=(loc_piece[0]-1, loc_piece[1]-1)
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='O'
                move="L"

        if (direction=="UP"):
            if direction in legal[loc_piece]:

                move=(loc_piece[0]-1, loc_piece[1])
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='O'
                move="UP"

        if (direction=="R"):
            if direction in legal[loc_piece]:
                move=(loc_piece[0]-1, loc_piece[1]+1)
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='O'
                move="R"
        
        new_turn="black"



    if state.get_turn()=='black':
       
        if (direction=="L"):
            if direction in legal[loc_piece]:
                move=(loc_piece[0]+1, loc_piece[1]-1)
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='X'
                move="L"
        if (direction=="UP"):

            if direction in legal[loc_piece]:

                move=(loc_piece[0]+1, loc_piece[1])
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='X'
                move="UP"

        if (direction=="R"):
            if direction in legal[loc_piece]:
                move=(loc_piece[0]+1, loc_piece[1]+1)
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='X'
                move="R"
        
        new_turn="white"

    new_state=Env_state(last_board,new_turn)
    new_state.set_direction(move)

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
    
  
    front.append(node)
    
    #print(node2expand.get_level())
    goal_state = False
    node2expand=node
    while node2expand.get_level() <= level:
        
        node2expand = front.pop(0)
        # if node2expand not in expanded:
        babies=[]
        legal_moves=node2expand.get_state().get_legal_moves()
        for loc,direct_list in legal_moves.items():

            for direct in direct_list:
                new_state=transition(node2expand.get_state(),direct,loc)
                #display_state(new_state)

                #print(new_state.get_turn())
                #print(new_state.get_legal_moves())
                new_node=Node(new_state,node2expand.get_level()+1, node2expand)

                #print(new_node.get_level())
                babies.append(new_node)
                # babies.append(new_node)
        expanded.append(node2expand)
        node2expand.set_child(babies)
        front.extend(babies)
        
    return(calc_utility(expanded, level, "evasive"))
    

    
    
    # for i in expanded:
        
    #     print(i.get_level())
    #     display_state(i.get_state())
    #     print('-------')

def calc_utility(expanded, level, utility):
    for i in expanded:
        if i.get_level()==level:
            if utility=="evasive":
                i.utility_evasive()
                #print(i.get_utility())
    for i in range(len(expanded)-1, -1, -1):
        print(expanded[i].get_level())
        
        if expanded[i].get_level()!= level and expanded[i].get_level()<level:
            utilities=[]
            for j in expanded[i].get_child():

                utilities.append(j.get_utility())
            #print(utilities)

            if expanded[i].get_level()%2==0:
                expanded[i].set_utility(max(utilities))
            else:
                expanded[i].set_utility(min(utilities))
    the_answer=expanded[0].get_utility()
   
    d_way=0
    for i in expanded[0].get_child():
        
        if the_answer==i.get_utility():

            d_way=((i.get_state().get_row(), i.get_state().get_column()), i.get_state().get_direction())
            break
    print(d_way)
    return d_way


if __name__=="__main__":
    root_state=initial_state(3,3,1)
    root_node=Node(root_state,0)
    minimax(root_node,3)







