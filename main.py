#!/usr/bin/env python3

from events import Cube2x2x2FewestMoves


test = Cube2x2x2FewestMoves()


scramble = test.gen_scramble()

solution = test.solve_scramble(scramble)

padded_scramble = test.pad_scramble(solution, "R' U' F")

print(scramble)
print(solution)
print(padded_scramble)


event_names = [
    "2FMC"
]


