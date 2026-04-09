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



assert cancel_moves("R' U' F R2 D U B D U' L' B2 U' F F2 D' B2 D' L2 D' R2 B2 R2 F2 U' B2 D' R' U' F", 4) == "R' U' F R2 D U B D U' L' B2 U' F' D' B2 D' L2 D' R2 B2 R2 F2 U' B2 D' R' U' F"

assert cancel_moves("R F F' R", 4) == "R2"

assert cancel_moves("R F F2 F R", 4) == "R2"

assert cancel_moves("U D2 R4 D6' U", 4) == "U2"

assert cancel_moves("R F F2 . F R", 4) == "R F' . F R"

assert cancel_moves("R F F2 R", 5) == "R F2' R"