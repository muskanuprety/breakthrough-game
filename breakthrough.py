
# Work by Tamara Blagojevic and Muskan Uprety
import random
import copy
import sys
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

    def utility_conquerer(self):
        turrn = self.state.get_turn()
        if turrn == "white":
            x = (0 - len(self.get_state().get_black_list())) + random.random()
        if turrn == "black":
            x = (0 - len(self.get_state().get_white_list())) + random.random()
        self.utility = x

    def utility_kill_and_survive(self):
        turrn = self.state.get_turn()
        util=0
        if turrn == "white":
            util = len(self.state.get_white_list()) - len(self.get_state().get_black_list()) + random.random()
            for i in self.get_state().get_white_list():
                if i[0] == 0:
                    util+=1000

        if turrn == "black":
            util = len(self.state.get_black_list())*len(self.state.get_black_list()) - len(self.get_state().get_white_list()) + random.random()
            for i in self.get_state().get_white_list():
                if i[0] == self.state.get_row()-1:
                    util+=1000

        self.utility = util



            

    def utility_forward_move(self, turrn):
        # turrn = self.state.get_turn()

        if turrn == "white":
            util = 0
            listt=[]
            for i in self.get_state().get_white_list():
                listt.append(i[0])
            top=self.get_state().get_white_list()[listt.index(min(listt))]
            util=self.get_state().get_row()-top[0]
            for i in self.get_state().get_white_list():
                if i[0] == 0:
                    util+=1000
            

        if turrn == "black":
            
            util = 0
            listt=[]
            for i in self.get_state().get_black_list():
                listt.append(i[0])
            top=self.get_state().get_black_list()[listt.index(max(listt))]
            util=top[0]    
            for i in self.get_state().get_white_list():
                if i[0] == self.state.get_row()-1:
                    util+=1000 


        self.utility = util + random.random()

class Env_state():
    def __init__(self, board,turn):  # White is O and black is X
        self._board = board
        self._turn = turn
        self.direction=None
        self.pos=None
        self._row = len(self._board)
        self._column = len(self._board[0])

    def get_turn(self):
        return self._turn

    def get_row(self):
        return self._row
    def get_pos(self):
        return self.pos
    def set_pos(self, n):
        self.pos=n
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

                x="L"

        if (direction=="UP"):
            if direction in legal[loc_piece]:

                move=(loc_piece[0]-1, loc_piece[1])
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='O'
                x="UP"

        if (direction=="R"):
            if direction in legal[loc_piece]:
                move=(loc_piece[0]-1, loc_piece[1]+1)
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='O'
                x="R"
        
        new_turn="black"



    if state.get_turn()=='black':
       
        if (direction=="L"):
            if direction in legal[loc_piece]:
                move=(loc_piece[0]+1, loc_piece[1]-1)
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='X'
                x='L'
        if (direction=="UP"):

            if direction in legal[loc_piece]:

                move=(loc_piece[0]+1, loc_piece[1])
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='X'
                x="UP"

        if (direction=="R"):
            if direction in legal[loc_piece]:
                move=(loc_piece[0]+1, loc_piece[1]+1)
                last_board[loc_piece[0]][loc_piece[1]]="."
                last_board[move[0]][move[1]]='X'
                x="R"
        
        new_turn="white"

    new_state=Env_state(last_board,new_turn)
    new_state.set_direction(x)
    new_state.set_pos(loc_piece)

    return new_state


def da_goal(state):
    
    bb = state.get_board()
    row = state.get_row()
    if "O" in bb[0] :
        return True
    if  "X" in bb[len(bb)-1]:
        return True
    return False
  

def minimax(node, level, utility): # level is 3
    front =[]
    expanded=[]
    turn = node.get_state().get_turn()
  
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
        
    return(calc_utility(expanded, level, utility, turn))
    

    
    
    # for i in expanded:
        
    #     print(i.get_level())
    #     display_state(i.get_state())
    #     print('-------')

def calc_utility(expanded, level, utility, turn):
    for i in expanded:
        if i.get_level()==level:
            if utility=="evasive":
                i.utility_evasive()
            if utility=="conquerer":
                i.utility_conquerer()
            if utility=="kill_and_survive":
                i.utility_kill_and_survive()
            if utility=="forward_move":
                # print(turn)
                i.utility_forward_move(turn)

                #print(i.get_utility())
    for i in range(len(expanded)-1, -1, -1):
        #print(expanded[i].get_level())
        
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
    # print(the_answer)
    d_way=0
    for i in expanded[0].get_child():
        
        if the_answer==i.get_utility():

            d_way=(i.get_state().get_pos(), i.get_state().get_direction())
            break
    return d_way


def play_game(hueristic_white, hueristic_black, board_state, level, pcs):
    turns_played = 0
    black_piece=0
    white_piece=0
    game_node = Node(board_state, 0)
    display_state(game_node.get_state())
    print("--------------------------------")
    while da_goal(game_node.get_state()) == False:
        if game_node.get_state().get_turn() == "white":
            loc, direction = minimax(game_node, level, hueristic_white)
        if game_node.get_state().get_turn() == "black":
            loc, direction = minimax(game_node, level, hueristic_black)

        new_state = transition(game_node.get_state(), direction, loc)
        display_state(new_state)
        turns_played+=1
        print("--------------------------------")
        game_node = Node(new_state,0)

    final_board = game_node.get_state().get_board()
    # print(final_board)
    for i in range(len(final_board)):
        for j in range(len(final_board[0])):
            if final_board[i][j] == "X":
                black_piece +=1
            if final_board[i][j] == "O":
                white_piece +=1
    print(str((pcs- white_piece))+" white pieces captured ")
    print(str((pcs- black_piece))+" black pieces captured ")
    print(str(turns_played)+ " moves played total")



if __name__=="__main__":                

## the order of the terminal command is:  python3 breakthrough.py <no. of rows> <no. of columns> <no of rows of pieces> <hueristic_white> <hueristic_black> <depth for minimax>
    rows = input("number of rows? ")
    columns = input("number of columns? ")
    pcs = input("number of rows of pieces? ")
    hrs_white = input("Hueristic for white, Pick one: evasive/ conquerer/ forward_move/ kill_and_survive: ")
    hrs_black = input("Hueristic for black, Pick one: evasive/ conquerer/ forward_move/ kill_and_survive: ")
    depth = input("how deep do you want minimax to go? ")

    root_state=initial_state(int(rows),int(columns),int(pcs))
    root_node=Node(root_state,0)
    play_game(hrs_white,hrs_black,root_node.get_state(), int(depth), int(pcs)*int(columns))






