# -*- coding: utf-8 -*-
"""
Created on Sun May 16 18:03:22 2021
IA - CHALLENGE       ESILV S2-A3
@author: Alix PETITCOL, Constance RAIMBAULT, Elodie RIPAUD, Glory RAFALIMANANA
"""
from math import inf as infinity
import copy
import time


HUMAN = -1 #'X'
COMP = +1 #'O'


def Actions(state):
    """
    This function return all the empty cells of the current board
    :para state: the state of the current plate
    :return: the list of all the valid moves
    """
    actions=[] #contient les actions possibles 
    for i in range(12): #on parcourt l'ensemble des colonnes et lignes
        for j in range(12):
            if(state[i][j]==' '): #si la case est vide, celà signifie que l'on peut encore placer jeton dedans
                actions.append((i,j)) #on ajoute la case aux actions possibles
    return actions


def Result(state, action, player):
	"""
    This function changes the state of the board with the player's action 
    :para state: the state of the current plate
    :para action: list that contains the coordinates of the player's action 
    :para player: the current player (+1 : COMP  -1: HUMAN)
    :return: the new state of the game board
    """
	new_state = copy.copy(state)
	i, j = action
	if(new_state[i][j] == 0):
		new_state[i][j] = player
	return new_state


def Win(state, player):
	"""
 	This function enumerates the winning states
 	:param state: the state of the current plate
 	:param player: the current player
 	:return: return if (True) or not (False) the player wins 
	"""
	win = False
	check = []
    
    # alignement sur colonne
	for x in range(9): # 0 -> 8 + 3 = 11 -> fin plateau
		for y in range(12):
			check = [state[x][y], state[x + 1][y], state[x + 2][y], state[x + 3][y]]
			if [player, player, player, player] == check:
				win = True
				break
		if win:
			break
    	
	if not win:
        # alignement sur ligne
		for x in range(12):
			for y in range(9): # 0 -> 8 + 3 = 11 -> fin plateau
				check =  [state[x][y], state[x][y + 1], state[x][y + 2], state[x][y + 3]]
				if [player, player, player, player] == check:
					win = True
					break
			if win:
				break
    	
	if not win:
        # alignement sur diagonale montante et descendante
		for x in range(9): # 0 -> 8 + 3 = 11 -> fin plateau
			for y in range(9):
				check = [state[x][y], state[x + 1][y + 1], state[x + 2][y + 2], state[x + 3][y + 3]]
				if [player, player, player, player] == check:
					win = True
					break
				check = [state[x][y + 3], state[x + 1][y + 2], state[x + 2][y + 1], state[x + 3][y]]
				if [player, player, player, player] == check:
					win = True
					break
			if win:
				break
            
	return win


def Evaluate(state):
	"""
	This function evaluates the state
	:param state: the state of the current plate
	:return: +1 if Computer, -1 if Human, 0 if draw
	"""
	if Win(state, HUMAN):
		score = -1
	elif Win(state, COMP):
		score = +1
	else:
		score = 0
	return score


def GameOver(state):
	"""
	This is used to tell if this is game over or not
	:param state: the current state of the board
	:return: True if the computer or the player win
	"""
	return Win(state, HUMAN) or Win(state, COMP)


def MaxValue(state, alpha, beta, k): 
	"""
	Evaluate the utility of a state (part I)
	:param state: the current state of the board
	:param alpha: minimal score that the Maximizer player will obtain
	:param beta: maximum score that the Minimazer player will obtain
	:return: an utility value of a state
	"""
	k += 1
	if k == 4 or GameOver(state):
		return Evaluate(state)

	value = -infinity

	for cell in Actions(state):
		value = max(value, MinValue(Result(state, cell, HUMAN), alpha, beta, k))
		if value >= beta:
			return value
        
		alpha = max(alpha,value)
        
	return value


def MinValue(state,alpha,beta,k): 
	"""
	Evaluate the utility of a state (part II)
	:param state: the current state of the board
	:param alpha: minimal score that the Maximizer player will insure
	:param beta: maximum score that the Minimazer player will insure
	:return: an utility value of a state
	"""
	k += 1
	if k == 4 or GameOver(state):
		return Evaluate(state)

	value = +infinity

	for cell in Actions(state):
		value = min(value, MaxValue(Result(state, cell, COMP), alpha, beta, k))
		if value <= alpha:
			return value
        
		beta = min(beta,value)

	return value


def AlphaBeta(state, turn, AI_start):
	"""
    Evaluation of all the potencial moves that a player could make for the current state of the board
    :param state: the current state of the board
    :param turn: the number of times that the game has changed (number of actions made on the plate)
    :param AI_start: True if AI has started the game first, else false
    :return: the best action that the AI player will make to win the game
    """
	action = [0,0]
	v = -infinity
	for cell in WidthPruning(state, turn, AI_start):
		temp = Result(state, cell, HUMAN)
		value = MinValue(temp, -infinity, +infinity, 0)
		if value > v:
			v = value
			action = cell
	return action


def WidthPruning(state, turn, AI_Start):
    """
    This function identify, select and return the best potential actions to make, according to the current state
    :param state: the current state of the board
    :param turn: the number of times that the game has changed (number of actions made on the plate)
    :param AI_Start: True if AI has started the game first, else false
    :return: the best potential actions that the AI player should make to win the game
    """
    
    busy_cell = []   
    busy_cell_AI = []
     
    #order by priority :            
    ultimate = set()            #offensive alignment of 3 COMP tokens IA_Start= True 
    A_best_cell = set()        #both 3 tokens  Class A  => return A_best_cell
    B_best_cell = set()         #find alignment of 2 COMP tokens and AI started first ! Class B => return B_best_cell
    C_best_cell = set()         #find alignment of 2 random tokens Class C => return C_best_cell
    D_best_cell = set()         #find one busy COMP cell to continue game Class D => return D_best_cell
    E_best_cell = set()         #find one random busy cell to continue the game Class E => return E_best_cell

                        
    B_prioritaire = set()
   
    L = [HUMAN, COMP]
    for player in L:
        if turn > 4: #3 tokens ULTIMATE AND BEST_CELL car le premier tour est fixé à 0
            #si c'est lui qui en a 3 il doit mettre le 4e plutôt que de bloquer ! => ultimate prioritaire
            
            #  3 TOKEN ALIGNED ? :
                
                        # alignment of 3 COMP tokens Class ULTIMATE : ultimate
                        # alignment of 3 HUMAN or COMP tokens Class A : A_best_cell
                            
            #3 alignés sur colonne
            for x in range(9): # 0 -> 8 + 3 = 11 -> fin plateau
                for y in range(12):
                    if [player, player, player, 0] == [state[x][y], state[x + 1][y], state[x + 2][y], state[x + 3][y]]: 
                        A_best_cell.add((x+3,y))
                        if player == COMP:
                            ultimate.add((x+3,y))
                    if [0, player, player, player] == [state[x][y], state[x + 1][y], state[x + 2][y], state[x + 3][y]]: 
                        A_best_cell.add((x,y))
                        if player == COMP:
                            ultimate.add((x,y))
                    if [player, player, 0, player] == [state[x][y], state[x + 1][y], state[x + 2][y], state[x + 3][y]]: 
                        A_best_cell.add((x+2,y))
                        if player == COMP:
                            ultimate.add((x+2,y))
                    if [player, 0, player, player] == [state[x][y], state[x + 1][y], state[x + 2][y], state[x + 3][y]]: 
                        A_best_cell.add((x+1,y))
                        if player == COMP:
                            ultimate.add((x+1,y))
	
    
            #3 alignés sur ligne
            for x in range(12):
                for y in range(9): # 0 -> 8 + 3 = 11 -> fin plateau
                    if [player, player, player, 0] == [state[x][y], state[x][y + 1], state[x][y + 2], state[x][y + 3]]:
                        A_best_cell.add((x,y+3))
                        if player == COMP:
                            ultimate.add((x,y+3))
                    if [player, player, 0, player] == [state[x][y], state[x][y + 1], state[x][y + 2], state[x][y + 3]]:
                        A_best_cell.add((x,y+2))
                        if player == COMP:
                            ultimate.add((x,y+2))
                    if [player, 0, player, player] == [state[x][y], state[x][y + 1], state[x][y + 2], state[x][y + 3]]: 
                        A_best_cell.add((x,y+1))
                        if player == COMP:
                            ultimate.add((x,y+1))
                    if [0, player, player, player] == [state[x][y], state[x][y + 1], state[x][y + 2], state[x][y + 3]]:
                        A_best_cell.add((x,y))
                        if player == COMP:
                            ultimate.add((x,y))


        	#3 alignés sur diagonale montante ou descendante
            for x in range(9): # 0 -> 8 + 3 = 11 -> fin plateau
                for y in range(9):
                    if [0, player, player, player] == [state[x][y], state[x + 1][y + 1], state[x + 2][y + 2], state[x + 3][y + 3]]:
                        A_best_cell.add((x,y))
                        if player == COMP:
                            ultimate.add((x,y))
                    if [player, 0, player, player] == [state[x][y], state[x + 1][y + 1], state[x + 2][y + 2], state[x + 3][y + 3]]:
                        A_best_cell.add((x+1,y+1))
                        if player == COMP:
                            ultimate.add((x+1,y+1))
                    if [player, player, 0, player] == [state[x][y], state[x + 1][y + 1], state[x + 2][y + 2], state[x + 3][y + 3]]:#diagonale montante
                        A_best_cell.add((x+2,y+2))
                        if player == COMP:
                            ultimate.add((x+2,y+2))
                    if [player, player, player, 0] == [state[x][y], state[x + 1][y + 1], state[x + 2][y + 2], state[x + 3][y + 3]]:#diagonale montante
                        A_best_cell.add((x+3,y+3))
                        if player == COMP:
                            ultimate.add((x+3,y+3))
                    if [0, player, player, player] == [state[x][y + 3], state[x + 1][y + 2], state[x + 2][y + 1], state[x + 3][y]]:
                        A_best_cell.add((x,y+3))
                        if player == COMP:
                            ultimate.add((x,y+3))
                    if [player, 0, player, player] ==[state[x][y + 3], state[x + 1][y + 2], state[x + 2][y + 1], state[x + 3][y]]:
                        A_best_cell.add((x+1,y+2))
                        if player == COMP:
                            ultimate.add((x+1,y+2))
                    if [player, player, 0, player] == [state[x][y + 3], state[x + 1][y + 2], state[x + 2][y + 1], state[x + 3][y]]:#diagonale descendante
                        A_best_cell.add((x+2,y+1))
                        if player == COMP:
                            ultimate.add((x+2,y+1))
                    if [player, player, player, 0] == [state[x][y + 3], state[x + 1][y + 2], state[x + 2][y + 1], state[x + 3][y]]:#diagonale montante
                        A_best_cell.add((x+3,y))
                        if player == COMP:
                            ultimate.add((x+3,y))
                   
        #  2 TOKENS ALIGNED ? :
            
                # alignment of 2 COMP tokens Class B : B_best_cell
                # alignment of 2 random tokens Class C : C_best_cell
            
    
        for x in range(9): # 0 -> 8 + 3 = 11 -> fin plateau #colonne
            for y in range(12):
                if [0, player, player, 0] == [state[x][y], state[x + 1][y], state[x + 2][y], state[x + 3][y]] : 
                    C_best_cell.add((x+3,y))
                    C_best_cell.add((x,y))
                    if AI_Start and player == COMP:
                        B_best_cell.add((x+3,y))
                        B_best_cell.add((x,y))
                if [0, player, player, -player] == [state[x][y], state[x + 1][y], state[x + 2][y], state[x + 3][y]] : 
                    C_best_cell.add((x,y))
                    if AI_Start and player == COMP:
                        B_best_cell.add((x,y))
                if [-player, player, player, 0] == [state[x][y], state[x + 1][y], state[x + 2][y], state[x + 3][y]] : 
                    C_best_cell.add((x+3,y))
                    if AI_Start and player == COMP:
                        B_best_cell.add((x+3,y))
                if [0, player, 0, player] == [state[x][y], state[x + 1][y], state[x + 2][y], state[x + 3][y]] : 
                    B_prioritaire.add((x+2,y))
                if [player, 0, player] == [state[x][y], state[x + 1][y], state[x + 2][y]] : 
                    C_best_cell.add((x+1,y))
                    
                    
        for x in range(12): # 0 -> 8 + 3 = 11 -> fin plateau #ligne
            for y in range(9):
                if [0, player, player, 0] == [state[x][y], state[x][y + 1], state[x][y + 2], state[x][y + 3]] : 
                    C_best_cell.add((x,y+3))
                    C_best_cell.add((x,y))
                    if AI_Start and player == COMP:
                        B_best_cell.add((x,y+3))
                        B_best_cell.add((x,y))
                if [0, player, player, -player] == [state[x][y], state[x][y + 1], state[x][y + 2], state[x][y + 3]] : 
                    C_best_cell.add((x,y))
                    if AI_Start and player == COMP:
                        B_best_cell.add((x,y))
                if [-player, player, player, 0] == [state[x][y], state[x][y + 1], state[x][y + 2], state[x][y + 3]] : 
                    C_best_cell.add((x,y+3))
                    if AI_Start and player == COMP:
                        B_best_cell.add((x,y+3))
                if [0, player, 0, player] == [state[x][y], state[x][y + 1], state[x][y + 2], state[x][y + 3]] : 
                    B_prioritaire.add((x,y+2))
                if [player, 0, player] == [state[x][y], state[x][y + 1], state[x][y + 2]] : 
                    C_best_cell.add((x,y+1))
                    
                    
        for x in range(9):#9 0->8  + 3= 11 = fin plateau #diagonales
            for y in range(9):
                if [0, player, player, 0] == [state[x][y], state[x + 1][y + 1], state[x + 2][y + 2], state[x + 3][y + 3]] : 
                    C_best_cell.add((x+3,y+3))
                    C_best_cell.add((x,y))
                    if AI_Start and player == COMP:
                        B_best_cell.add((x+3,y+3))
                        B_best_cell.add((x,y))
                if [0, player, player, -player] == [state[x][y], state[x + 1][y + 1], state[x + 2][y + 2], state[x + 3][y + 3]] : 
                    C_best_cell.add((x,y))
                    if AI_Start and player == COMP:
                        B_best_cell.add((x,y))
                if [-player, player, player, 0] == [state[x][y], state[x + 1][y + 1], state[x + 2][y + 2], state[x + 3][y + 3]] : 
                    C_best_cell.add((x+3,y+3))
                    if AI_Start and player == COMP:
                        B_best_cell.add((x+3,y+3))
                if [0, player, 0, player] == [state[x][y], state[x + 1][y + 1], state[x + 2][y + 2], state[x + 3][y + 3]] :
                    B_prioritaire.add((x+2,y+2))
                if [player, 0, player] == [state[x][y], state[x + 1][y + 1], state[x + 2][y + 2]] : 
                    C_best_cell.add((x+1,y+1))
                    
                if [0, player, player, 0] == [state[x][y + 3], state[x + 1][y + 2], state[x + 2][y + 1], state[x + 3][y]] : 
                     C_best_cell.add((x,y+3))
                     C_best_cell.add((x+3,y))
                     if AI_Start and player == COMP:
                        B_best_cell.add((x,y+3))
                        B_best_cell.add((x+3,y))
                if [-player, player, player, 0] == [state[x][y + 3], state[x + 1][y + 2], state[x + 2][y + 1], state[x + 3][y]] : 
                     C_best_cell.add((x+3,y))
                     if AI_Start and player == COMP:
                        B_best_cell.add((x+3,y))
                if [0, player, player, -player] == [state[x][y + 3], state[x + 1][y + 2], state[x + 2][y + 1], state[x + 3][y]] : 
                     C_best_cell.add((x,y+3))
                     if AI_Start and player == COMP:
                        B_best_cell.add((x,y+3))
                if [0, player, 0, player] == [state[x][y + 3], state[x + 1][y + 2], state[x + 2][y + 1], state[x + 3][y]] :
                    B_prioritaire.add((x+2,y+1))
                if [player, 0, player] == [state[x][y + 3], state[x + 1][y + 2], state[x + 2][y + 1]] : 
                    C_best_cell.add((x+1,y+2))
     
    B_prioritaire = B_best_cell.intersection(C_best_cell)
    #  NO ALIGNMENT ON PLATE :
            
                # Find one busy COMP cell to continue game Class D : D_best_cell
                # Find one random busy cell to continue the game Class E : E_best_cell   
                     
    for i in range(12):
        for j in range(12):
            if state[i][j] != 0 :
                busy_cell.append([i,j])
            
                
    for cell in busy_cell:
        
        if cell[0] < 11:
            if state[cell[0]+1][cell[1]] == 0: # si la case en dessous est libre
                E_best_cell.add((cell[0]+1,cell[1]))
                if state[cell[0]][cell[1]] == COMP:  
                    D_best_cell.add((cell[0]+1,cell[1]))
                    
        if cell[1] < 11:
            if state[cell[0]][cell[1]+1] == 0:
                E_best_cell.add((cell[0],cell[1]+1))
                if state[cell[0]][cell[1]] == COMP:
                    D_best_cell.add((cell[0],cell[1]+1))
                    
        if cell[0] < 11 and cell[1] < 11:
            if state[cell[0]+1][cell[1]+1] == 0:
                E_best_cell.add((cell[0]+1,cell[1]+1))
                if state[cell[0]][cell[1]] == COMP:
                    D_best_cell.add((cell[0]+1,cell[1]+1))
                    
        if cell[0] > 0:
            if state[cell[0]-1][cell[1]] == 0:
               E_best_cell.add((cell[0]-1,cell[1]))
               if state[cell[0]][cell[1]] == COMP:
                    D_best_cell.add((cell[0]-1,cell[1]))
                    
        if cell[1] > 0:
            if state[cell[0]][cell[1]-1] == 0:
                E_best_cell.add((cell[0],cell[1]-1))
                if state[cell[0]][cell[1]] == COMP:
                    D_best_cell.add((cell[0],cell[1]-1))
                    
        if cell[0] > 0 and cell[1] > 0:
            if state[cell[0]-1][cell[1]-1] == 0:
                E_best_cell.add((cell[0]-1,cell[1]-1))
                if state[cell[0]][cell[1]] == COMP:
                    D_best_cell.add((cell[0]-1,cell[1]-1))
                    
        if cell[0] < 11 and cell[1] > 0:
            if state[cell[0]+1][cell[1]-1] == 0:
                E_best_cell.add((cell[0]+1,cell[1]-1))
                if state[cell[0]][cell[1]] == COMP:
                    D_best_cell.add((cell[0]+1,cell[1]-1))
                    
        if cell[0] > 0 and cell[1] < 11:
            if state[cell[0]-1][cell[1]+1] == 0:
                E_best_cell.add((cell[0]-1,cell[1]+1))
                if state[cell[0]][cell[1]] == COMP:
                    D_best_cell.add((cell[0]-1,cell[1]+1))
      
    D_prioritaire = set()
    D_prioritaire = D_best_cell.intersection(E_best_cell)
    
    C_prioritaire = set()
    C_prioritaire = C_best_cell.intersection(D_prioritaire)
   
    print(f'ultimate : {ultimate}')
    print(f'A_best_cell : {A_best_cell}')
    print(f'B_prioritaire : {B_prioritaire}')
    print(f'B_best_cell : {B_best_cell}')
    print(f'C_best_cell : {C_best_cell}')
    print(f'D_prioritaire : {D_prioritaire}')
    print(f'D_best_cell : {D_best_cell}')
    print(f'E_best_cell : {E_best_cell}')


    if len(ultimate)!= 0:
        return list(ultimate)
    
    elif len(A_best_cell)!= 0:
        return list(A_best_cell)
    
    elif len(B_prioritaire)!= 0:
        return list(B_prioritaire)
    
    elif len(B_best_cell) !=0:
        return list(B_best_cell)
    
    elif len(C_prioritaire) != 0:
        return list(C_prioritaire)
    
    elif len(C_best_cell) !=0:
        return list(C_best_cell)
    
    elif len(D_prioritaire) !=0:
        return list(D_prioritaire)
    
    elif len(D_best_cell) !=0:
        return list(D_best_cell)
    else : 
        return list( E_best_cell)


def Show(state):
	"""
	This is used to display the grid
	:param state: the current state of the board
	:return: nothing
	"""
	chars = { -1: 'X', +1: 'O', 0: ' '}

	str_line = '  -------------------------------------------------'
	print('\n    1   2   3   4   5   6   7   8   9  10  11  12 \n' + str_line)
	for k, i in enumerate(state):
		if k + 1 < 10:
			print(str(k + 1), end = ' ')
		else:
			print(str(k + 1), end = '')
		for l, j in enumerate(i):
			symbol = chars[j]
			print(f'| {symbol} ', end = '')
			if l == len(i) - 1:
				print('|', end = '')
		print('\n' + str_line)


def main():
    """
    this is the main method
    :return: nothing
    """
    player = ''
    IA_Start = False

    while player != 'Y' and player != 'N':
        player = input('Human start first (Y/N): ').upper()
        
    
    plate = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    Show(plate)
    
    if player == 'Y':
        tour = 0
        
    else:
        tour = 1
        IA_Start = True
        
    while(not GameOver(plate)):
        i, j = 0, 0
        s = copy.deepcopy(plate)
        if(tour % 2 == 0):
            print("Tour de l'HUMAIN")
            while(i<1 or i>12) or (j<1 or j>12):
                try :
                    print("Quelle est la COLONNE choisie ?")
                    j = int(input())
                    print("Quelle est la LIGNE choisie ?")
                    i = int(input())
                    print(f"l'HUMAIN a choisi la COLONNE {j} et la LIGNE {i}")
                    print('\n\n')
                except (KeyError, ValueError):
                    print('try again')
                    
            while(plate[i-1][j-1] != 0):
                print("La case est déjà remplie ! Veuillez saisir une autre COLONNE")
                j = int(input())
                print("Saisir la LIGNE choisie")
                i = int(input())
                print(f"l'HUMAIN a choisi la COLONNE {j} et la LIGNE {i}")
            plate[i-1][j-1] = HUMAN
            
        else:
            if(tour == 1 and IA_Start == True): # l'IA démarre au milieu du plateau si c'est lui qui commence la partie
                action = (5,5) # à la colonne 6 et ligne 6
            else:
                print("Tour de l'IA")
                start = time.perf_counter()
                action = AlphaBeta(s, tour, IA_Start)
                end = time.perf_counter()
                z = float(end-start)
                print(f"Temps de réponse de l'IA : {z}")
            print(f"l'IA a choisi la COLONNE {action[1]+1} et la LIGNE {action[0]+1}")
            plate = Result(plate, action, COMP)
        tour += 1
        Show(plate)
    if Win(plate, HUMAN):
        print('HUMAN Win!')
    elif Win(plate, COMP):
        print('AI Win!')
    else:
        print('Draw')
        



if __name__ == '__main__':
	main()
