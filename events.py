from abc import ABC, abstractmethod
import json

from scramblers import AbstractRandomMoveScrambler, AbstractRandomStateScramblerTwipsCLI, AbstractClockScrambler

cuboid_move_substitutions = {"L": "L2", "F": "F2", "R": "R2", "B": "B2"}
square0_move_substitutions = {"R": "/","UU_DD'": "(6,6)","U_DD'": "(-3,6)","Ui_D'": "(3,-3)","UU_D'": "(6,-3)","U_D'": "(-3,-3)","UU'": "(6,0)","DD'": "(0,6)","U'": "(-3,0)","D'": "(0,-3)","UU_DD": "(6,6)","U_DD": "(3,6)","Ui_D": "(-3,3)","UU_D": "(6,3)","U_D": "(3,3)","UU": "(6,0)","U2": "(6,0)","DD": "(0,6)","D2": "(0,6)","U": "(3,0)","D": "(0,3)"}

def scramble_move_substitution(scramble: str, move_substitutions: dict):
    for move in move_substitutions:
        scramble = scramble.replace(move, move_substitutions[move])
    
    return scramble



class EventScrambleRounds:
    def scramble_rounds(self, num_rounds: int, output_file: str):
        event_scrambles = {}
        
        for i in range(num_rounds):
            round_key = f"Round {i+1}"
            event_scrambles[round_key] = {"Scrambles": {}}        
            
            # Generate main scrambles
            for j in range(self.num_scrambles):
                event_scrambles[round_key]["Scrambles"][str(j+1)] = self.scramble()
            
            # Generate extra scrambles
            for j in range(self.num_extras):
                event_scrambles[round_key]["Scrambles"][f"E{j+1}"] = self.scramble()

        with open(output_file, "w") as f:
            json.dump(event_scrambles, f, indent=4)

        return event_scrambles

class Cube2x2x2FewestMoves(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
    def __init__(self, twips_name: str, state_file: str):

        self.num_scrambles = 5
        self.num_extras = 2

        super().__init__(twips_name, "puzzles/2x2x2.kpuzzle.json", state_file, "U,F,R", min_scramble_length=11, min_optimal_filter=0)

    def gen_random_state(self):
        self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", None, 6)
        self.kpuzzle.state_orientations["CORNERS"] = self.kpuzzle.scramble_orbit_orientation("CORNERS", True, 6)
        self.kpuzzle.construct_state()
        self.kpuzzle.write_state_to_file()
    
    def scramble(self):
        scramble = self.gen_scramble()
        solution = self.solve_scramble(scramble, True, 11)
        return self.pad_scramble(solution, "R' U' F")
    
class Octahedron4x4x4Speedsolving(EventScrambleRounds):
    def __init__(self):

        self.num_scrambles = 3
        self.num_extras = 2

        self.scrambler = AbstractRandomMoveScrambler(45, [[['U','Uw','Uw','D'],['F','Fw','Fw','B'],['R','Rw','Rw','BL'],['L','BRw','BRw','BR']]], [["", "'"]])

    def scramble(self):
        return self.scrambler.generate_scramble()
    

class ClockSpeedsolving(EventScrambleRounds):

    def __init__(self):
        self.num_scrambles = 5
        self.num_extras = 2

        self.scrambler = AbstractClockScrambler(["UR", "DR", "DL", "UL", "U", "R", "D", "L", "ALL", "y2", "U", "R", "D", "L", "ALL"], 12)
    
    def scramble(self):
        return self.scrambler.generate_scramble()

class PyraminxClockSpeedsolving(EventScrambleRounds):

    def __init__(self):
        self.num_scrambles = 5
        self.num_extras = 2

        self.scrambler = AbstractClockScrambler(["U", "DR", "R", "D", "L", "ALL", "y2", "U", "DR", "R"], 12)
    
    def scramble(self):
        return self.scrambler.generate_scramble()
    
class Cuboid1x3x3Speedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
    def __init__(self, twips_name: str, state_file: str):

        self.num_scrambles = 5
        self.num_extras = 2

        super().__init__(twips_name, "puzzles/1x3x3.kpuzzle.json", state_file, "R,L,F,B", min_scramble_length=0, min_optimal_filter=0)

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

        self.num_scrambles = 5
        self.num_extras = 2

        super().__init__(twips_name, "puzzles/2x2x3.kpuzzle.json", state_file, "U,D,R,F", min_scramble_length=0, min_optimal_filter=0)

    def gen_random_state(self):
        self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", parity_constraint=None, fixed_index=None)
        self.kpuzzle.state_pieces["E_EDGES"] = self.kpuzzle.scramble_orbit_pieces("E_EDGES", parity_constraint=None, fixed_index=3)
        self.kpuzzle.construct_state()
        self.kpuzzle.write_state_to_file()
    
    def scramble(self):
        return scramble_move_substitution(self.gen_scramble(), cuboid_move_substitutions)

class Cuboid2x3x3Speedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
    def __init__(self, twips_name: str, state_file: str):

        self.num_scrambles = 5
        self.num_extras = 2

        super().__init__(twips_name, "puzzles/2x3x3.kpuzzle.json", state_file, "U,D,R,L,F,B", min_scramble_length=0, min_optimal_filter=0)

    def gen_random_state(self):
        self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", parity_constraint=None, fixed_index=None)
        self.kpuzzle.state_pieces["EDGES"] = self.kpuzzle.scramble_orbit_pieces("EDGES", parity_constraint=None, fixed_index=None)
        self.kpuzzle.construct_state()
        self.kpuzzle.write_state_to_file()
    
    def scramble(self):
        return scramble_move_substitution(self.gen_scramble(), cuboid_move_substitutions)

class Pentahedron3x2Speedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
    def __init__(self, twips_name: str, state_file: str):

        self.num_scrambles = 5
        self.num_extras = 2

        super().__init__(twips_name, "puzzles/2pentahedron.kpuzzle.json", state_file, "U,R,L,F", min_scramble_length=0, min_optimal_filter=0)

    def gen_random_state(self):
        self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", parity_constraint=None, fixed_index=None)
        self.kpuzzle.state_pieces["EDGES"] = self.kpuzzle.scramble_orbit_pieces("EDGES", parity_constraint=None, fixed_index=None)
        self.kpuzzle.construct_state()
        self.kpuzzle.write_state_to_file()
    
    def scramble(self):
        return scramble_move_substitution(self.gen_scramble(), cuboid_move_substitutions)

class Pentahedron3x3Speedsolving(AbstractRandomStateScramblerTwipsCLI, EventScrambleRounds):
    def __init__(self, twips_name: str, state_file: str):

        self.num_scrambles = 5
        self.num_extras = 2

        super().__init__(twips_name, "puzzles/3pentahedron.kpuzzle.json", state_file, "U,D,R,L,F", min_scramble_length=0, min_optimal_filter=0)

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

        self.num_scrambles = 5
        self.num_extras = 2

        super().__init__(twips_name, "puzzles/square0.kpuzzle.json", state_file, "U,D,R,U_D,Ui_D,U_DD,UU_D,UU_DD,UU,DD", min_scramble_length=0, min_optimal_filter=0)

    def gen_random_state(self):
        self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", parity_constraint=None, fixed_index=None)
        self.kpuzzle.state_orientations["EQUATOR"] = self.kpuzzle.scramble_orbit_orientation("EQUATOR", orientation_constraint=False)
        self.kpuzzle.construct_state()
        self.kpuzzle.write_state_to_file()
    
    def scramble(self):
        # return self.gen_scramble(extra_params=["--metric", "quantum"])
        return scramble_move_substitution(self.gen_scramble(extra_params=["--metric", "quantum"]), square0_move_substitutions)