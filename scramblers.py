import random
from abc import ABC, abstractmethod

from twips_cli.twips_cli import Twips
from twips_cli.kpuzzle import KPuzzle



class AbstractRandomStateScramblerTwipsCLI():
	def __init__(self, twips_name: str, puzzle_file: str, state_file: str, generator_moves: str, min_scramble_length: int, min_optimal_filter: int):

		self.puzzle_file = puzzle_file
		self.state_file = state_file
		self.min_scramble_length = min_scramble_length
		self.min_optimal_filter = min_optimal_filter
		self.generator_moves = generator_moves


		self.twips = Twips(twips_name)
		self.kpuzzle = KPuzzle(puzzle_file, state_file)


	@abstractmethod
	def gen_random_state(self):
		pass

	def gen_scramble(self):
		while True:
			self.gen_random_state()

			scramble = self.twips.state_scramble(self.puzzle_file, self.state_file, self.min_scramble_length, self.generator_moves, 1)
			scramble = self.twips.parse_search_moves(scramble)

			solutions = self.twips.solve_scramble(self.puzzle_file, scramble, self.generator_moves, 1)
			solution = self.twips.parse_search_moves(solutions)

			if self.twips.parse_movecount(solution) >= self.min_optimal_filter:
				break
		
		return scramble

	def solve_scramble(self, scramble: str):
		solution = self.twips.solve_scramble(self.puzzle_file, scramble, self.generator_moves, 1, 0, False)
		return self.twips.parse_search_moves(solution)

	def pad_scramble(self, solution, padding):

		padded_solution = f"{padding} {solution} {padding}"

		loop_count = 0
		scramble_length = self.min_scramble_length

		while True:
			
			# Increase scramble length if all solutions found cancel with padding
			if loop_count > 10:
				scramble_length += 1
				loop_count = 0

			scrambles = self.twips.solve_scramble(self.puzzle_file, padded_solution, self.generator_moves, 20, scramble_length, True)
			scrambles = self.twips.parse_search_algs(scrambles)

			for scramble in scrambles:
				if scramble[0] == "F" or scramble[-1] == "R" or scramble[-2] == "R":
					continue
				else:
					return f"R' U' F {scramble} R' U' F"

			loop_count += 1


class AbstractRandomMoveScrambler():
	"""
	Parameters
	------------
	scramble_length : number of moves in the generated scramble

	move_types : outermost list separates movetypes with different modifers, next list separates moves along different axis, innermost list contains movenames
	"""

	def __init__(self, scramble_length : int, move_types : list[list[str]], modifers : list[str]):
		
		if len(move_types) != len(modifers):
			raise ValueError("Movetypes list should be the same length as modifiers list")
		
		self.scramble_length = scramble_length
		self.move_types = move_types
		self.modifiers = modifers

	def generate_scramble(self):
		"""
		Docstring for generate_scramble
		
		Generates random move scramble for event
		"""
		
		scramble = ""
		last_axis_moves = []
		last_axis = None

		for i in range(self.scramble_length):

			modifier_type_index = random.randint(0, len(self.modifiers) - 1)

			# Get random axis and ensure that axis' moves haven't been exhausted
			while True:
				axis_index = random.randint(0, len(self.move_types[modifier_type_index]) - 1)

				if (axis_index != last_axis) or (len(last_axis_moves) < len(set(self.move_types[modifier_type_index][axis_index]))):
					break

			if last_axis != axis_index:
				last_axis = axis_index
				last_axis_moves = []

			# Get random move and ensure it doesn't cancel with previous move
			while True:
				move_index = random.randint(0, len(self.move_types[modifier_type_index][axis_index]) - 1)
				if move_index not in last_axis_moves:
					break
			
			last_axis_moves.append(move_index)

			modifier_index = random.randint(0, len(self.modifiers[modifier_type_index]) - 1)

			scramble += f"{self.move_types[modifier_type_index][axis_index][move_index]}{self.modifiers[modifier_type_index][modifier_index]} "
		
		return scramble[:-1]
