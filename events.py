from abc import ABC, abstractmethod
import json

from scramblers import AbstractRandomMoveScrambler, AbstractRandomStateScramblerTwipsCLI, AbstractClockScrambler



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

        super().__init__(twips_name, "puzzles/2x2x2.kpuzzle.json", state_file, "U,F,R", 11, 7)

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