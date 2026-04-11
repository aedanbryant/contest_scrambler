from abc import ABC, abstractmethod
import json
from string import Template
import random
import asyncio

from twips_cli.twips_cli import Twips
from scramblers import AbstractRandomMoveScrambler, AbstractRandomStateScramblerTwipsCLI, AbstractClockScrambler, abstract_tip_scrambler
from utils import clock_movesub, scramble_move_substitution, html2pdf, cuboid_move_substitutions, square0_move_substitutions


STANDARD    = 0
FMC         = 1
NO_IMAGE    = 2
template_paths = ["images/standard.html", "images/FMC.html", "images/no_image.html"]


class EventScrambleRounds:
	def image_move_sub(self, scrambles):
		return scrambles

	def scramble_rounds(self, groups: list[int], comp_name: str, comp_dir: str, num_scrambles: int = None, num_extras: int = None, gen_pdf = True):

		# event_scrambles = {"competition_name": comp_name, "event_id": self.event_id, "generation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
		event_scrambles = {"event_id": self.event_id, "rounds": []}
  
		num_rounds = len(groups)

		num_scrambles = self.num_scrambles if num_scrambles == None else num_scrambles
		num_extras = self.num_extras if num_extras == None else num_extras

		for i in range(num_rounds):

			event_scrambles["rounds"].append({"groups": []})

			for j in range(groups[i]):

				event_scrambles["rounds"][i]["groups"].append({"scrambles": [], "extras": []})
				
				# Generate main scrambles
				for _ in range(num_scrambles):
					event_scrambles["rounds"][i]["groups"][j]["scrambles"].append(self.scramble())
				
				# Generate extra scrambles
				for _ in range(num_extras):
					event_scrambles["rounds"][i]["groups"][j]["extras"].append(self.scramble())

		# pdf
		with open(template_paths[self.pdf_type], "r") as f:
			html_template = f.read()

		template = Template(html_template)

		if (self.pdf_type == STANDARD) or (self.pdf_type == NO_IMAGE):
			for i in range(num_rounds):
				for j in range(groups[i]):
					output_html = template.substitute({"comp_name": comp_name, "event_name": self.event_name, "puzzle_id": self.puzzle_id, 
											"round": i+1, "group": j+1, "num_scrambles": num_scrambles, "num_extras": num_extras,
											"stickering_mask": self.stickering_mask,
											"scrambles": event_scrambles["rounds"][i]["groups"][j]["scrambles"], "extras": event_scrambles["rounds"][i]["groups"][j]["extras"],
											"image_scrambles": self.image_move_sub(event_scrambles["rounds"][i]["groups"][j]["scrambles"]), "image_extras": self.image_move_sub(event_scrambles["rounds"][i]["groups"][j]["extras"])})
				
					html_filepath = f"{comp_dir}/html/{comp_name}_{self.event_id}_r{i+1}_g{j+1}.html"
					with open(html_filepath, "w") as f:
						f.write(output_html)
					
					if gen_pdf: asyncio.run(html2pdf(html_filepath, f"{comp_dir}/pdf/{comp_name}_{self.event_id}_r{i+1}_g{j+1}.pdf"))
					


		if self.pdf_type == FMC:

			for i in range(num_rounds):
				for j in range(groups[i]):
					for k in range(num_scrambles):
						output_html = template.substitute({"comp_name": comp_name, "event_name": self.event_name, "puzzle_id": f"{self.puzzle_id}",
											"round": i+1, "group": j+1, "attempt": k+1, "num_attempts": num_scrambles,
											"scramble": event_scrambles["rounds"][i]["groups"][j]["scrambles"][k]})
						
						html_filepath = f"{comp_dir}/html/{comp_name}_{self.event_id}_r{i+1}_g{j+1}_a{k+1}.html"
						with open(html_filepath, "w") as f:
							f.write(output_html)
						if gen_pdf:  asyncio.run(html2pdf(html_filepath, f"{comp_dir}/pdf/{comp_name}_{self.event_id}_r{i+1}_g{j+1}_a{k+1}.pdf"))

					for k in range(num_extras):
						output_html = template.substitute({"comp_name": comp_name, "event_name": self.event_name, "puzzle_id": f"{self.puzzle_id}",
											"round": i+1, "group": j+1, "attempt": f"E{k+1}", "num_attempts": num_extras,
											"scramble": event_scrambles["rounds"][i]["groups"][j]["extras"][k]})
						
						html_filepath = f"{comp_dir}/html/{comp_name}_{self.event_id}_r{i+1}_g{j+1}_e{k+1}.html"
						with open(html_filepath, "w") as f:
							f.write(output_html)
						if gen_pdf:  asyncio.run(html2pdf(html_filepath, f"{comp_dir}/pdf/{comp_name}_{self.event_id}_r{i+1}_g{j+1}_e{k+1}.pdf"))



		return event_scrambles

### Random Move
class Octahedron4x4x4Speedsolving(EventScrambleRounds):
	def __init__(self):

		self.event_name = "Master Face-Turning Octahedron"
		self.event_id = "mfto"
		self.pdf_type = NO_IMAGE
		self.puzzle_id = None
		self.stickering_mask = ""

		self.num_scrambles = 3
		self.num_extras = 2

		self.scrambler = AbstractRandomMoveScrambler(45, [[['U','Uw','Uw','D'],['F','Fw','Fw','B'],['R','Rw','Rw','BL'],['L','BRw','BRw','BR']]], [["", "'"]])

	def scramble(self):
		return self.scrambler.generate_scramble()

class Cube4x4x4FewestMoves(EventScrambleRounds):
	def __init__(self):

		self.event_name = "4x4 Fewest Moves"
		self.event_id = "444fm"
		self.pdf_type = FMC
		self.puzzle_id = "4x4x4"
		self.stickering_mask = ""

		self.num_scrambles = 3
		self.num_extras = 0

		self.scrambler = AbstractRandomMoveScrambler(45, [[['U','Uw','D'],['F','Fw','B'],['R','Rw','L']]], [["", "'"]])

	def scramble(self):

		# Make sure scramble doesn't cancel with padding
		while True:
			scramble = self.scrambler.generate_scramble()
			moves = scramble.split()
			if (moves[0][0] == "F") or (moves[0][0] == "B" and moves[1][0] == "F") or \
				(moves[-1][0] == "R") or (moves[-1][0] == "L" and moves[-2][0] == "R"):
				continue
			break

		return "R' U' F " + scramble + " R' U' F"


### Random State
class Cube2x2x2FewestMoves(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "2x2x2 Fewest Moves"
		self.event_id = "222fm"
		self.pdf_type = FMC
		self.puzzle_id = "2x2x2"
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 0

		super().__init__(twips_name, "puzzles/2x2x2.kpuzzle.json", state_file, "U,F,R", min_scramble_length=11, min_optimal_filter=7)

	def gen_random_state(self):
		self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", None, 6)
		self.kpuzzle.state_orientations["CORNERS"] = self.kpuzzle.scramble_orbit_orientation("CORNERS", True, 6)
		self.kpuzzle.construct_state()
		self.kpuzzle.write_state_to_file()
	
	def scramble(self):
		scramble = self.gen_scramble()
		solution = self.solve_scramble(scramble, True, 11)
		return self.pad_scramble(solution, "R' U' F")
	

class ClockSpeedsolving(EventScrambleRounds):

	def __init__(self):

		self.event_name = "Clock"
		self.event_id = "clock"
		self.pdf_type = STANDARD
		self.puzzle_id = "clock"
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		self.scrambler = AbstractClockScrambler(["UR", "DR", "DL", "UL", "U", "R", "D", "L", "ALL", "y2", "U", "R", "D", "L", "ALL"], 12)
	
	def scramble(self):
		return self.scrambler.generate_scramble()

class PyraminxClockSpeedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):

	def __init__(self, twips_name: str, state_file: str):
		self.event_name = "Triangle Clock"
		self.event_id = "pyra_clock"
		self.pdf_type = NO_IMAGE
		self.puzzle_id = None
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		self.scrambler = AbstractClockScrambler(["U", "DR", "R", "D", "L", "ALL", "y2", "U", "DR", "R"], 12)

		super().__init__(twips_name, "puzzles/pyraclock.kpuzzle.json", state_file, "U,R,ALL,BU,BR,BALL,DR,DL,D,L,BDR,BDL,BD,BL", min_scramble_length=0, min_optimal_filter=6)
	
	def gen_random_state(self):
		pass

	def scramble(self):

		while True:
			original_scramble = self.scrambler.generate_scramble()
			scramble = clock_movesub(original_scramble)
			if self.check_optimal_geq(scramble, depth=self.min_optimal_filter, QTM=False) == True:
				break

		return original_scramble


class PentagonalClockSpeedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):

	def __init__(self, twips_name: str, state_file: str):
		self.event_name = "Pentagonal Clock"
		self.event_id = "penta_clock"
		self.pdf_type = NO_IMAGE
		self.puzzle_id = None
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		self.scrambler = AbstractClockScrambler(["UR", "DR", "DL", "UL", "URw", "DRw", "D", "DLw", "ULw", "ALL", "y2", "URw", "DRw", "D", "DLw", "ULw", "ALL"], 12)

		# super().__init__(twips_name, "puzzles/pyraclock.kpuzzle.json", state_file, "U,R,ALL,BU,BR,BALL,DR,DL,D,L,BDR,BDL,BD,BL", min_scramble_length=0, min_optimal_filter=0)
	
	def gen_random_state(self):
		pass

	def scramble(self):
		return self.scrambler.generate_scramble()

class NewPentagonalClockSpeedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):

	def __init__(self, twips_name: str, state_file: str):
		self.event_name = "Pentagonal Clock"
		self.event_id = "penta_clock"
		self.pdf_type = NO_IMAGE
		self.puzzle_id = None
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		self.scrambler = AbstractClockScrambler(["UR", "DR", "DL", "UL", "URw", "DRw", "D", "DLw", "ULw", "ALL", "y2", "UR", "DR", "D", "DL", "UL"], 12)

		# super().__init__(twips_name, "puzzles/pyraclock.kpuzzle.json", state_file, "U,R,ALL,BU,BR,BALL,DR,DL,D,L,BDR,BDL,BD,BL", min_scramble_length=0, min_optimal_filter=0)
	
	def gen_random_state(self):
		pass

	def scramble(self):
		return self.scrambler.generate_scramble()


class Cuboid1x3x3Speedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "1x3x3"
		self.event_id = "133_cuboid"
		self.pdf_type = STANDARD
		self.puzzle_id = "3x3x3"
		# self.stickering_mask = "EDGES:--------IIII,CENTERS:-IIII-"
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		super().__init__(twips_name, "puzzles/1x3x3.kpuzzle.json", state_file, "R,L,F,B", min_scramble_length=8, min_optimal_filter=3)

	def gen_random_state(self):
		self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", parity_constraint=None, fixed_index=None)
		corner_parity = self.kpuzzle.get_orbit_parity(self.kpuzzle.state_pieces["CORNERS"])
		self.kpuzzle.state_orientations["EDGES"] = self.kpuzzle.scramble_orbit_orientation("EDGES", orientation_constraint=True, fixed_index=None, custom_orientation_constraint=corner_parity)
		self.kpuzzle.construct_state()
		self.kpuzzle.write_state_to_file()
	
	def scramble(self):
		return scramble_move_substitution(self.gen_scramble(), cuboid_move_substitutions)
	
class Cuboid2x2x3Speedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "2x3x3"
		self.event_id = "223_cuboid"
		self.pdf_type = STANDARD
		# self.puzzle_id = "3x3x3"
		# self.stickering_mask = "EDGES:IIIIIIII----,CENTERS:IIIIII"
		self.puzzle_id = "4x4x4"
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		super().__init__(twips_name, "puzzles/2x2x3.kpuzzle.json", state_file, "U,D,R,F", min_scramble_length=11, min_optimal_filter=7)

	def gen_random_state(self):
		self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", parity_constraint=None, fixed_index=None)
		self.kpuzzle.state_pieces["E_EDGES"] = self.kpuzzle.scramble_orbit_pieces("E_EDGES", parity_constraint=None, fixed_index=3)
		self.kpuzzle.construct_state()
		self.kpuzzle.write_state_to_file()
	
	def scramble(self):
		return scramble_move_substitution(self.gen_scramble(), cuboid_move_substitutions)

	def image_move_sub(self, scrambles):
		return [scramble_move_substitution(s, {"R": "Rw", "F": "Fw"}) for s in scrambles]

class Cuboid2x3x3Speedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "2x3x3"
		self.event_id = "233_cuboid"
		self.pdf_type = STANDARD
		# self.puzzle_id = "3x3x3"
		# self.stickering_mask = "EDGES:--------IIII,CENTERS:-IIII-"
		self.puzzle_id = "4x4x4"
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		super().__init__(twips_name, "puzzles/2x3x3.kpuzzle.json", state_file, "U,D,R,L,F,B", min_scramble_length=2, min_optimal_filter=0)

	def gen_random_state(self):
		self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", parity_constraint=None, fixed_index=None)
		self.kpuzzle.state_pieces["EDGES"] = self.kpuzzle.scramble_orbit_pieces("EDGES", parity_constraint=None, fixed_index=None)
		self.kpuzzle.construct_state()
		self.kpuzzle.write_state_to_file()
	
	def scramble(self):
		return scramble_move_substitution(self.gen_scramble(), cuboid_move_substitutions)

	def image_move_sub(self, scrambles):
		return [scramble_move_substitution(s, {"U": "Uw"}) for s in scrambles]

class Pentahedron3x2Speedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "2-Pentahedron"
		self.event_id = "2pentahedron"
		self.pdf_type = NO_IMAGE
		self.puzzle_id = None
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		super().__init__(twips_name, "puzzles/2pentahedron.kpuzzle.json", state_file, "U,R,L,F", min_scramble_length=11, min_optimal_filter=7)

	def gen_random_state(self):
		self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", parity_constraint=None, fixed_index=None)
		self.kpuzzle.state_pieces["EDGES"] = self.kpuzzle.scramble_orbit_pieces("EDGES", parity_constraint=None, fixed_index=None)
		self.kpuzzle.construct_state()
		self.kpuzzle.write_state_to_file()
	
	def scramble(self):
		return scramble_move_substitution(self.gen_scramble(), cuboid_move_substitutions)

class Pentahedron3x3Speedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "3-Pentahedron"
		self.event_id = "3pentahedron"
		self.pdf_type = NO_IMAGE
		self.puzzle_id = None
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		super().__init__(twips_name, "puzzles/3pentahedron.kpuzzle.json", state_file, "U,D,R,L,F", min_scramble_length=11, min_optimal_filter=8)

	def gen_random_state(self):
		self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", parity_constraint=None, fixed_index=None)
		self.kpuzzle.state_pieces["EDGES"] = self.kpuzzle.scramble_orbit_pieces("EDGES", parity_constraint=None, fixed_index=None)

		corner_parity = self.kpuzzle.get_orbit_parity(self.kpuzzle.state_pieces["CORNERS"])
		edge_parity = self.kpuzzle.get_orbit_parity(self.kpuzzle.state_pieces["EDGES"])

		self.kpuzzle.state_pieces["SQUARES"] = self.kpuzzle.scramble_orbit_pieces("SQUARES", parity_constraint=corner_parity, fixed_index=None)
		self.kpuzzle.state_pieces["CENTERS"] = self.kpuzzle.scramble_orbit_pieces("CENTERS", parity_constraint=edge_parity, fixed_index=None)
		self.kpuzzle.state_orientations["CENTERS"] = self.kpuzzle.scramble_orbit_orientation("CENTERS", orientation_constraint=True, fixed_index=None, custom_orientation_constraint=corner_parity)

		self.kpuzzle.construct_state()
		self.kpuzzle.write_state_to_file()
	
	def scramble(self):
		return scramble_move_substitution(self.gen_scramble(), cuboid_move_substitutions)

class Square0Speedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "Square-0"
		self.event_id = "sq0"
		self.pdf_type = STANDARD
		self.puzzle_id = "square1"
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		super().__init__(twips_name, "puzzles/square0.kpuzzle.json", state_file, "U,D,R,U_D,Ui_D,U_DD,UU_D,UU_DD,UU,DD", min_scramble_length=0, min_optimal_filter=6)

	def gen_random_state(self):
		self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", parity_constraint=None, fixed_index=None)
		self.kpuzzle.state_orientations["EQUATOR"] = self.kpuzzle.scramble_orbit_orientation("EQUATOR", orientation_constraint=False)
		self.kpuzzle.construct_state()
		self.kpuzzle.write_state_to_file()
	
	def scramble(self):
		# return self.gen_scramble(extra_params=["--metric", "quantum"])
		return scramble_move_substitution(self.gen_scramble(extra_params=["--metric", "quantum"]), square0_move_substitutions)

class SuperFloppySpeedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "Super Floppy Cube"
		self.event_id = "super_133"
		self.pdf_type = STANDARD
		self.puzzle_id = "3x3x3"
		self.stickering_mask = "EDGES:IIIIIIII----,CORNERS:IIIIIIII,CENTERS:------"

		self.num_scrambles = 5
		self.num_extras = 2

		super().__init__(twips_name, "puzzles/super_floppy.kpuzzle.json", state_file, "L,F,R,B", min_scramble_length=11 , min_optimal_filter=7)

	def gen_random_state(self):
		self.kpuzzle.state_pieces["EDGES"] = self.kpuzzle.scramble_orbit_pieces("EDGES", parity_constraint=None, fixed_index=None)
		self.kpuzzle.state_orientations["CENTERS"] = self.kpuzzle.scramble_orbit_orientation("CENTERS", orientation_constraint=False)
		self.kpuzzle.construct_state()
		self.kpuzzle.write_state_to_file()
	
	def scramble(self):
		return self.gen_scramble()
	

# TODO Takes a while
class CornerTurningOctahedronSpeedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "Corner-Turning Octahedron"
		self.event_id = "cto"
		self.pdf_type = NO_IMAGE
		self.puzzle_id = None
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		super().__init__(twips_name, "puzzles/cto.kpuzzle.json", state_file, "U,D,L,F,R,B", min_scramble_length=0, min_optimal_filter=0)

	def gen_random_state(self):
		self.kpuzzle.state_pieces["EDGES"] = self.kpuzzle.scramble_orbit_pieces("EDGES", parity_constraint=None, fixed_index=None)
		ep = self.kpuzzle.get_orbit_parity(self.kpuzzle.state_pieces["EDGES"])
		self.kpuzzle.state_orientations["CENTERS"] = self.kpuzzle.scramble_orbit_orientation("CENTERS", orientation_constraint=True, custom_orientation_constraint_mod=2, custom_orientation_constraint=ep)
		self.kpuzzle.construct_state()
		self.kpuzzle.write_state_to_file()
	
	def scramble(self):
		return f"{self.gen_scramble()} {abstract_tip_scrambler(4, ["u", "d", "r", "l", "f", "b"], ["", "", "2", "'"])}"


class IvyCubeSpeedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "Ivy Cube"
		self.event_id = "ivy_cube"
		self.pdf_type = NO_IMAGE
		self.puzzle_id = None
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		super().__init__(twips_name, "puzzles/ivycube.kpuzzle.json", state_file, "L,D,R,B", min_scramble_length=8, min_optimal_filter=4)


	def gen_random_state(self):
		self.kpuzzle.state_orientations["CORNERS"] = self.kpuzzle.scramble_orbit_orientation("CORNERS", orientation_constraint=False)
		self.kpuzzle.state_pieces["EDGES"] = self.kpuzzle.scramble_orbit_pieces("EDGES", parity_constraint=0)
		self.kpuzzle.construct_state()
		self.kpuzzle.write_state_to_file()
	
	def scramble(self):
		return self.gen_scramble()

class PyraminxDuoSpeedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "Pyraminx Duo"
		self.event_id = "pyram_duo"
		self.pdf_type = STANDARD
		self.puzzle_id = "master_tetraminx"
		self.stickering_mask = "EDGES:IIIIIIIIIIIIIIIIIIIIIIII,EDGES2:IIIIIIIIIIII"

		self.num_scrambles = 5
		self.num_extras = 2

		super().__init__(twips_name, "puzzles/pyraduo.kpuzzle.json", state_file, "U,R,L,B", min_scramble_length=4, min_optimal_filter=2)

		self.center_permutations = [[[1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0], [0, 1, 2, 3]], [[0, 3, 1, 2], [2, 1, 3, 0], [3, 0, 2, 1], [1, 2, 0, 3]], [[0, 2, 3, 1], [3, 1, 0, 2], [1, 3, 2, 0], [2, 0, 1, 3]]]

	def gen_random_state(self):
		self.kpuzzle.state_orientations["CORNERS"] = self.kpuzzle.scramble_orbit_orientation("CORNERS", orientation_constraint=False)
		self.kpuzzle.state_pieces["CENTERS"] = random.choice(self.center_permutations[sum(self.kpuzzle.state_orientations["CORNERS"]) % 3])

		self.kpuzzle.construct_state()
		self.kpuzzle.write_state_to_file()
	
	def scramble(self):
		return self.gen_scramble()
	
	def image_move_sub(self, scrambles):
		return [s.lower() for s in scrambles]


class DinoCubeSpeedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "Dino Cube"
		self.event_id = "dino"
		self.pdf_type = STANDARD
		self.puzzle_id = "redi_cube"
		self.stickering_mask = "CORNERS:IIIIIIII"

		self.num_scrambles = 5
		self.num_extras = 2

		super().__init__(twips_name, "puzzles/dino.kpuzzle.json", state_file, "F,U,UR,UL,R,D", min_scramble_length=11, min_optimal_filter=7)


	def gen_random_state(self):
		self.kpuzzle.state_pieces["EDGES"] = self.kpuzzle.scramble_orbit_pieces("EDGES", parity_constraint=0, fixed_index=7)
		self.kpuzzle.construct_state()
		self.kpuzzle.write_state_to_file()
	
	def scramble(self):

		# Check other solution
		while True:
			original_scramble = self.gen_scramble()
			scramble = "U UL' U UL' U R D' R D' R " + original_scramble
			if self.check_optimal_geq(scramble, depth=self.min_optimal_filter, QTM=False) == True:
				break
			
		return original_scramble

class PyramorphixSpeedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "Pyramorphix"
		self.event_id = "pyramorphix"
		self.pdf_type = NO_IMAGE
		self.puzzle_id = None
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		super().__init__(twips_name, "puzzles/pyramorphix.kpuzzle.json", state_file, "B,R,L", min_scramble_length=9, min_optimal_filter=5)

	def gen_random_state(self):
		self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", None, 6)
		self.kpuzzle.state_orientations["CORNERS"] = self.kpuzzle.scramble_orbit_orientation("CORNERS", True, 6)

		# Set orientations to ignore (Hard coded)
		orientation_mods = []
		for i, piece in enumerate(self.kpuzzle.state_pieces["CORNERS"]):

			if piece in [0, 2, 5, 7]:
				orientation_mods.append(1)
				self.kpuzzle.state_orientations["CORNERS"][i] = 0
			else:
				orientation_mods.append(0)
			
		self.kpuzzle.state_orientation_mods["CORNERS"] = orientation_mods

		self.kpuzzle.construct_state()
		self.kpuzzle.write_state_to_file()
	
	def scramble(self):
		return self.gen_scramble()

class SuperGearCubeSpeedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "Super Gear Cube"
		self.event_id = "super_gear_cube"
		self.pdf_type = STANDARD
		self.puzzle_id = "3x3x3"
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		self.random_move = AbstractRandomMoveScrambler(1000, [["R", "F", "U"]], [["", "2", "3", "4", "5", "6", "5'", "4'", "3'", "2'", "'"]])

		super().__init__(twips_name, "puzzles/super_gear_cube.kpuzzle.json", state_file, "U,R,F", min_scramble_length=8, min_optimal_filter=4)
	
	# TODO This is wrong, kinda a pain...
	def gen_random_state(self):
		pass
		
		# self.kpuzzle.state_pieces["CORNERS_2"] = self.kpuzzle.scramble_orbit_pieces("CORNERS_2", None, 3)

		# if self.kpuzzle.state_pieces["CORNERS_2"].index(0) in [0, 2]:
		# 	self.kpuzzle.state_pieces["CORNERS_1"] = random.choice([[0, 1, 1, 1], [1, 1, 1, 0]])
		# else:
		# 	self.kpuzzle.state_pieces["CORNERS_1"] = random.choice([[1, 0, 1, 1], [1, 1, 0, 1]])

		
		# self.kpuzzle.state_pieces["EDGES_1"] = self.kpuzzle.scramble_orbit_pieces("EDGES_1", None)
		# self.kpuzzle.state_pieces["EDGES_2"] = self.kpuzzle.scramble_orbit_pieces("EDGES_2", None)
		# self.kpuzzle.state_pieces["EDGES_3"] = self.kpuzzle.scramble_orbit_pieces("EDGES_3", None)

		# if self.kpuzzle.get_orbit_parity(self.kpuzzle.state_pieces["CORNERS_2"]) == 1:
		# 	self.kpuzzle.state_orientations["EDGES_1"] = [1, 1, 1, 1]

		# self.kpuzzle.construct_state()
		# self.kpuzzle.write_state_to_file()
	
	def scramble(self):

		while True:
			rm_scramble = self.random_move.generate_scramble()
			if self.check_optimal_geq(rm_scramble, depth=self.min_optimal_filter, QTM=False) == True:
				break

		return self.solve_scramble(rm_scramble, self.min_scramble_length)

		# return self.gen_scramble()
	
	def image_move_sub(self, scrambles):

		new_scrambles = []
		for scramble in scrambles:
			new_scramble = ""

			for move in scramble.split():
				base_move, modifier = [move[0], move[1:]]
				new_scramble += f"{base_move}{modifier} {base_move}w{modifier} "
			
			new_scrambles.append(new_scramble.strip())
		
		return new_scrambles


		

class GearCubeSpeedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "Gear Cube"
		self.event_id = "gear_cube"
		self.pdf_type = STANDARD
		self.puzzle_id = "3x3x3"
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		self.random_move = AbstractRandomMoveScrambler(1000, [["R", "F", "U"]], [["", "2", "3", "4", "5", "6", "5'", "4'", "3'", "2'", "'"]])

		super().__init__(twips_name, "puzzles/gear_cube.kpuzzle.json", state_file, "U,R,F", min_scramble_length=6, min_optimal_filter=3)
	
	# TODO This is wrong, kinda a pain...
	def gen_random_state(self):
		pass
		
		# self.kpuzzle.state_pieces["CORNERS_2"] = self.kpuzzle.scramble_orbit_pieces("CORNERS_2", None, 3)

		# if self.kpuzzle.state_pieces["CORNERS_2"].index(0) in [0, 2]:
		# 	self.kpuzzle.state_pieces["CORNERS_1"] = random.choice([[0, 1, 1, 1], [1, 1, 1, 0]])
		# else:
		# 	self.kpuzzle.state_pieces["CORNERS_1"] = random.choice([[1, 0, 1, 1], [1, 1, 0, 1]])

		
		# self.kpuzzle.state_pieces["EDGES_1"] = self.kpuzzle.scramble_orbit_pieces("EDGES_1", None)
		# self.kpuzzle.state_pieces["EDGES_2"] = self.kpuzzle.scramble_orbit_pieces("EDGES_2", None)
		# self.kpuzzle.state_pieces["EDGES_3"] = self.kpuzzle.scramble_orbit_pieces("EDGES_3", None)

		# if self.kpuzzle.get_orbit_parity(self.kpuzzle.state_pieces["CORNERS_2"]) == 1:
		# 	self.kpuzzle.state_orientations["EDGES_1"] = [1, 1, 1, 1]

		# self.kpuzzle.construct_state()
		# self.kpuzzle.write_state_to_file()
	
	def scramble(self):
		while True:
			rm_scramble = self.random_move.generate_scramble()
			if self.check_optimal_geq(rm_scramble, depth=self.min_optimal_filter, QTM=False) == True:
				break

		return self.solve_scramble(rm_scramble, self.min_scramble_length)

		# return self.gen_scramble()

	def image_move_sub(self, scrambles):

		new_scrambles = []
		for scramble in scrambles:
			new_scramble = ""

			for move in scramble.split():
				base_move, modifier = [move[0], move[1:]]
				new_scramble += f"{base_move}{modifier} {base_move}w{modifier} "
			
			new_scrambles.append(new_scramble.strip())
		
		return new_scrambles

#### Multi-Phase Scrambles
class CornerTurningOctahedronSpeedsolvingTwoPhase(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
	def __init__(self, twips_name: str, state_file: str):

		self.event_name = "Corner-Turning Octahedron"
		self.event_id = "cto"
		self.pdf_type = NO_IMAGE
		self.puzzle_id = None
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		self.random_move = AbstractRandomMoveScrambler(1000, [[['U','D'],['F','B'],['R','L']]], [["", "'", "2"]])

		self.phase_1_definition = "puzzles/cto_p1.kpuzzle.json"
		self.phase_1_generator_moves = "U,D,L,F,R,B"

		self.phase_2_generator_moves = "U,R"

		super().__init__(twips_name, "puzzles/cto.kpuzzle.json", state_file, "U,D,L,F,R,B", min_scramble_length=0, min_optimal_filter=2)
	
	def gen_random_state(self):
		pass

	def scramble(self):

		while True:

			rm_scramble = self.random_move.generate_scramble()
			if self.check_optimal_geq(rm_scramble, depth=self.min_optimal_filter, QTM=False) == True:
				break

		p1 = self.twips.parse_search_moves(self.twips.solve_scramble(self.phase_1_definition, rm_scramble, self.phase_1_generator_moves, 1))

		p2 = self.twips.parse_search_moves(self.twips.solve_scramble(self.puzzle_file, f"{rm_scramble} {p1}", self.phase_2_generator_moves, 1))

		scramble =  f"{p1} {p2}"

		return f"{scramble} {abstract_tip_scrambler(4, ["u", "d", "r", "l", "f", "b"], ["", "", "2", "'"])}"


### Twips built-in scrambles
class BabyFTOSpeedsolving(EventScrambleRounds):
	def __init__(self, twips_name):
		self.event_name = "Baby FTO"
		self.event_id = "baby_fto"
		self.pdf_type = STANDARD
		self.puzzle_id = "baby_fto"
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		self.twips = Twips(twips_name)
	
	def scramble(self):
		return self.twips.twip_scramble_builtin(self.puzzle_id)

class KilominxSpeedsolving(EventScrambleRounds):
	def __init__(self, twips_name):
		self.event_name = "Kilominx"
		self.event_id = "kilominx"
		self.pdf_type = STANDARD
		self.puzzle_id = "kilominx"
		self.stickering_mask = ""

		self.num_scrambles = 5
		self.num_extras = 2

		self.twips = Twips(twips_name)
	
	def scramble(self):
		return self.twips.twip_scramble_builtin(self.puzzle_id)