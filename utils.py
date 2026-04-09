import re

def cancel_moves(s: str, sym: int):
	"""
	
	Params:
		s: move sequence to cancel
		sym: symmetry of the puzzle
	"""

	move_list = []

	# Format moves into list of tuples with movetype and amount
	for move in s.split():

		suffix = 0

		amount = re.findall(r"\d+$", move)
		amount += re.findall(r"\d+(?=\')", move)

		if len(amount) == 0:
			amount = 1
		else:
			move = move.replace(amount[0], "")
			amount = int(amount[0])
	
		if move[-1] == "'":
			suffix = (sym - amount) % sym
		else:
			suffix = amount % sym

		move = move.replace("'", "")

		move_list.append((move, suffix))

	# Prune scramble alg
	while True:

		repeat = False
		for i in range(len(move_list)):

			if i > 0:
				if move_list[i][1] == 0:
					move_list.pop(i)
					repeat = True
					break

				if move_list[i-1][0] == move_list[i][0]:
					move_list[i - 1] = (move_list[i][0], (move_list[i-1][1] + move_list[i][1]) % sym)
					move_list.pop(i)

					if move_list[i-1][1] == 0:
						move_list.pop(i-1)

					repeat = True
					break
		
		if repeat == False:
			break


	# Convert back to alg
	alg = []

	for move in move_list:
		
		if move[1] > (sym // 2):

			amount = (move[1] - sym) * -1

			if amount == 1:
				suffix = "'"
			else:
				suffix = str(amount) + "'"
		else:

			if (move[1] == 1):
				suffix = ""
			else:
				suffix = str(move[1])
		
		alg.append(move[0] + suffix)
		

	return " ".join(alg)


def clock_movesub(scramble: str):

	front, back = scramble.split(" y2 ")

	back_arr = []
	for move in back.split():
		back_arr.append("B" + move)

	return (front + " " + " ".join(back_arr)).replace("-", "'").replace("+", "")

cuboid_move_substitutions = {"L": "L2", "F": "F2", "R": "R2", "B": "B2"}
inverse_cuboid_move_substitutions = {"L2": "L", "F2": "F", "R2": "R", "B2": "B"}
square0_move_substitutions = {"R": "/","UU_DD'": "(6,6)","U_DD'": "(-3,6)","Ui_D'": "(3,-3)","UU_D'": "(6,-3)","U_D'": "(-3,-3)","UU'": "(6,0)","DD'": "(0,6)","U'": "(-3,0)","D'": "(0,-3)","UU_DD": "(6,6)","U_DD": "(3,6)","Ui_D": "(-3,3)","UU_D": "(6,3)","U_D": "(3,3)","UU": "(6,0)","U2": "(6,0)","DD": "(0,6)","D2": "(0,6)","U": "(3,0)","D": "(0,3)"}
inverse_square0_move_substitutions = {"/": "R", "(6,6)": "UU_DD'", "(-3,6)": "U_DD'", "(3,-3)": "Ui_D'", "(6,-3)": "UU_D'", "(-3,-3)": "U_D'", "(6,0)": "UU'", "(0,6)": "DD'", "(-3,0)": "U'", "(0,-3)": "D'", "(6,6)": "UU_DD", "(3,6)": "U_DD", "(-3,3)": "Ui_D", "(6,3)": "UU_D", "(3,3)": "U_D", "(6,0)": "UU", "(6,0)": "U2", "(0,6)": "DD", "(0,6)": "D2", "(3,0)": "U", "(0,3)": "D"}

def scramble_move_substitution(scramble: str, move_substitutions: dict):
	for move in move_substitutions:
		scramble = scramble.replace(move, move_substitutions[move])
	
	return scramble


# assert cancel_moves("R' U' F R2 D U B D U' L' B2 U' F F2 D' B2 D' L2 D' R2 B2 R2 F2 U' B2 D' R' U' F", 4) == "R' U' F R2 D U B D U' L' B2 U' F' D' B2 D' L2 D' R2 B2 R2 F2 U' B2 D' R' U' F"

# assert cancel_moves("R F F' R", 4) == "R2"

# assert cancel_moves("R F F2 F R", 4) == "R2"

# assert cancel_moves("U D2 R4 D6' U", 4) == "U2"

# assert cancel_moves("R F F2 . F R", 4) == "R F' . F R"

# assert cancel_moves("R F F2 R", 5) == "R F2' R"