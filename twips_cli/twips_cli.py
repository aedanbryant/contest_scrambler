import subprocess


def print_command_debug(command: str):
	print_command = ""
	print_command += " ".join(command[:2]) + " "
	for c in command[2:-1]:
		if type(c) == str and c != "" and c[0] == "-":
			print_command += c + " "
		else:
			print_command += f"\"{c}\" "
	print(print_command + " " + command[-1])

class Twips():
	def __init__(self, twips_name: str):
		self.twips_name = twips_name
	

	def parse_search_moves(self, search_result):
		return search_result.split(" //")[0].strip()

	def parse_search_algs(self, search_result):
		solutions = search_result.split("\n")[:-1]
		solutions = [s.split(" //")[0] for s in solutions]

		return solutions

	def parse_movecount(self, alg: str):
		if alg.strip() == "":
			return 0
		return alg.strip().count(" ") + 1

	def state_scramble(self, puzzle_file: str, state_file: str, min_depth: int, generator_moves: str, min_solutions: int, max_depth = None, extra_params = None):
		command = [
			self.twips_name,
			"search",
			"--experimental-target-pattern", state_file,
			"--generator-moves", generator_moves,
			"--min-num-solutions", str(min_solutions),
			"--min-depth", str(min_depth),
			"--scramble-alg", "",
			puzzle_file
		]

		if extra_params != None:
			command += extra_params

		if max_depth != None:
			command.append("--max-depth")
			command.append(str(max_depth + 1))

		# print_command_debug(command)

		output = subprocess.run(command, capture_output=True, text=True)

		return output.stdout

	def solve_scramble(self, puzzle_file: str, scramble: str, generator_moves: str, min_solutions: int, min_depth: int = 0, random_start: bool = False, max_depth = None):
		command = [
			self.twips_name,
			"search",
			"--generator-moves", generator_moves,
			"--min-num-solutions", str(min_solutions),
			"--scramble-alg", scramble,
			"--min-depth", str(min_depth),
			puzzle_file
		]

		if max_depth != None:
			command.append("--max-depth")
			command.append(str(max_depth + 1))

		# Doesn't work in current version
		# if random_start == True:
		# 	command.append("--random-start")

		output = subprocess.run(command, capture_output=True, text=True)

		return output.stdout
