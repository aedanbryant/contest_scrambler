import random
import json

class KPuzzle():
	def __init__(self, kpuzzle_filepath: str, kpattern_filepath: str):
		
		self.kpuzzle_filepath = kpuzzle_filepath
		self.kpattern_filepath = kpattern_filepath

		self.orbit_names = []
		self.num_orientations = {}

		self.default_pieces = {}
		self.default_orientations = {}
		self.default_orientation_mods = {}
		
		self.state_pieces = {}
		self.state_orientations = {}
		self.state = {}

		self.set_default_state()

		self.state_pieces = self.default_pieces.copy()
		self.state_orientations = self.default_orientations.copy()

	def write_state_to_file(self):
		with open(self.kpattern_filepath, "w") as f:
			json.dump(self.state, f, indent=4)

	def construct_state(self):
		for piecetype in self.orbit_names:
			self.state[piecetype] = {"pieces": self.state_pieces[piecetype], "orientation": self.state_orientations[piecetype]}


	def get_orbit_parity(self, orbit: list[int]):
		"""
		Gets parity of orbit pieces
		"""
		parity = 0

		for i in range(len(orbit)):
			for p2 in orbit[i+1:]:
				if orbit[i] > p2:
					parity += 1
		
		return parity % 2

	def swap_orbit_parity(self, orbit: list[int]):
		"""
		Swaps the parity of orbit pieces by swapping last two pieces
		"""
		temp = orbit[-1]
		orbit[-1] = orbit[-2]
		orbit[-2] = temp

	def scramble_orbit_pieces(self, orbit_name: str, parity_constraint = None, fixed_index=None):
		pieces = self.default_pieces[orbit_name].copy()

		if fixed_index != None:
			pieces = pieces[0:fixed_index] + pieces[fixed_index + 1:]
		
		random.shuffle(pieces)

		if parity_constraint != None:
			if self.get_orbit_parity(pieces) != parity_constraint:
				self.swap_orbit_parity(pieces)

		if fixed_index != None:	
			pieces.insert(fixed_index, fixed_index)

		return pieces

	def scramble_orbit_orientation(self, orbit_name: str, orientation_constraint: bool, fixed_index=None, custom_orientation_constraint=None):
		orientation = self.default_orientations[orbit_name].copy()
		num_orientations = self.num_orientations[orbit_name]
		max_orientation = num_orientations - 1

		if fixed_index != None:
			orientation = orientation[0:fixed_index] + orientation[fixed_index + 1:]

		last_piece_index = len(orientation) - 1
		orientation_count = 0

		for i in range(last_piece_index):

			piece_orientation = random.randint(0, max_orientation)
			orientation_count += piece_orientation
			orientation[i] = piece_orientation

		if orientation_constraint == False:
			orientation[last_piece_index] = random.randint(0, max_orientation)
		elif custom_orientation_constraint != None:
			orientation[last_piece_index] = (num_orientations - ((orientation_count + custom_orientation_constraint) % num_orientations)) % num_orientations
		else:
			orientation[last_piece_index] = (num_orientations - (orientation_count % num_orientations)) % num_orientations

		if fixed_index != None:
			orientation.insert(fixed_index, self.default_orientations[orbit_name][fixed_index])

		return orientation

	def set_default_state(self):
		with open(self.kpuzzle_filepath, "r") as f:
			kpuzzle = json.load(f)
		
		for piecetype in kpuzzle["defaultPattern"].keys():
			self.default_pieces[piecetype] = kpuzzle["defaultPattern"][piecetype]['pieces']
			self.default_orientations[piecetype] = kpuzzle["defaultPattern"][piecetype]['orientation']

			try:
				self.default_orientation_mods[piecetype] = kpuzzle["defaultPattern"][piecetype]['orientationMod']
			except:
				self.default_orientation_mods[piecetype] = None

		for piecetype in kpuzzle["orbits"]:
			self.orbit_names.append(piecetype["orbitName"])
			self.num_orientations[piecetype["orbitName"]] = piecetype["numOrientations"]