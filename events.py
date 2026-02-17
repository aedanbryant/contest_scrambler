from scramblers import AbstractRandomMoveScrambler, AbstractRandomStateScramblerTwipsCLI

twips_name = "twips"
state_file = "patterns/scramble-pattern.json"


class Cube2x2x2FewestMoves(AbstractRandomStateScramblerTwipsCLI):
    def __init__(self):

        super().__init__(twips_name, "puzzles/2x2x2.kpuzzle.json", state_file, "U,F,R", 11, 4)

    def gen_random_state(self):
        self.kpuzzle.state_pieces["CORNERS"] = self.kpuzzle.scramble_orbit_pieces("CORNERS", None, 6)
        self.kpuzzle.state_orientations["CORNERS"] = self.kpuzzle.scramble_orbit_orientation("CORNERS", True, 6)
        self.kpuzzle.construct_state()
        self.kpuzzle.write_state_to_file()