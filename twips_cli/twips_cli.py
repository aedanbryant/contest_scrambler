import subprocess

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
		return alg.strip().count(" ") + 1

	def state_scramble(self, puzzle_file: str, state_file: str, min_depth: int, generator_moves: str, min_solutions: int):
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

		output = subprocess.run(command, capture_output=True, text=True)

		return output.stdout

	def solve_scramble(self, puzzle_file: str, scramble: str, generator_moves: str, min_solutions: int, min_depth: int = 0, random_start: bool = False):
		command = [
			self.twips_name,
			"search",
			"--generator-moves", generator_moves,
			"--min-num-solutions", str(min_solutions),
			"--scramble-alg", scramble,
			"--min-depth", str(min_depth),
			puzzle_file
		]

		if random_start == True:
			command.append("--random-start")

		output = subprocess.run(command, capture_output=True, text=True)

		return output.stdout
