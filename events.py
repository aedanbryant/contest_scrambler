from abc import ABC, abstractmethod
import json

from scramblers import AbstractRandomMoveScrambler, AbstractRandomStateScramblerTwipsCLI


class AbstractRandomStateEvent(AbstractRandomStateScramblerTwipsCLI):
    def __init__(self, twips_name: str, puzzle_file: str, state_file: str, generator_moves: str, min_scramble_length: int, min_optimal_filter: int, event_name: str, num_scrambles: int, num_extras: int):

        super().__init__(twips_name, puzzle_file, state_file, generator_moves, min_scramble_length, min_optimal_filter)
        
        self.num_scrambles = num_scrambles
        self.num_extras = num_extras


    @abstractmethod
    def scramble(self):
        pass

    def scramble_rounds(self, comp_name: str, num_rounds: int, output_file):

        event_scrambles = {}
        
        for i in range(num_rounds):
            event_scrambles[f"Round {i+1}"] = {"Scrambles": {}, "Extras": {}}        
            
            for j in range(self.num_scrambles):
                event_scrambles[f"Round {i+1}"]["Scrambles"][j+1] = self.scramble()
            
            for j in range(self.num_extras):
                event_scrambles[f"Round {i+1}"]["Extras"][j+1] = self.scramble()

        with open(output_file, "w") as f:
            json.dump(event_scrambles, f, indent=4)

        return event_scrambles


class AbstractRandomMoveEvent():
    def __init__(self, event_name: str, num_scrambles: int, num_extras: int):
        self.event_name = event_name
        self.num_scrambles = num_scrambles
        self.num_extras = num_extras

    @abstractmethod
    def scramble(self):
        pass

    def scramble_rounds(self, comp_name: str, num_rounds: int, output_file):

        event_scrambles = {}
        
        for i in range(num_rounds):
            event_scrambles[f"Round {i+1}"] = {"Scrambles": {}, "Extras": {}}        
            
            for j in range(self.num_scrambles):
                event_scrambles[f"Round {i+1}"]["Scrambles"][j+1] = self.scramble()
            
            for j in range(self.num_extras):
                event_scrambles[f"Round {i+1}"]["Extras"][j+1] = self.scramble()

        with open(output_file, "w") as f:
            json.dump(event_scrambles, f, indent=4)

        return event_scrambles


class Cube2x2x2FewestMoves(AbstractRandomStateEvent):
    def __init__(self, twips_name: str, state_file: str):

        super().__init__(twips_name, "puzzles/2x2x2.kpuzzle.json", state_file, "U,F,R", 11, 4, "222fm", 5, 2)

    def gen_random_state(self):
        self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", None, 6)
        self.kpuzzle.state_orientations["CORNERS"] = self.kpuzzle.scramble_orbit_orientation("CORNERS", True, 6)
        self.kpuzzle.construct_state()
        self.kpuzzle.write_state_to_file()
    
    def scramble(self):
        scramble = self.gen_scramble()
        solution = self.solve_scramble(scramble, True, 11)
        return self.pad_scramble(solution, "R' U' F")
    
class Octahedron4x4x4Speedsolving(AbstractRandomMoveEvent):
    def __init__(self):

        super().__init__("Master FTO", 3, 2)

        self.scrambler = AbstractRandomMoveScrambler(45, [[['U','Uw','Uw','D'],['F','Fw','Fw','B'],['R','Rw','Rw','BL'],['L','BRw','BRw','BR']]], [["", "'"]])
    
    def scramble(self):
        return self.scrambler.generate_scramble()