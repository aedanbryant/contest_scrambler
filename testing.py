# %% Imports
import matplotlib.pyplot as plt
import numpy as np
import re

from utils import clock_movesub, scramble_move_substitution, inverse_cuboid_move_substitutions, inverse_square0_move_substitutions

from events import *
twips_name = "twips"
state_file = "patterns/scramble-pattern.json"

# %% 2x2 FMC
print("2x2 FMC")
event_scrambler = Cube2x2x2FewestMoves(twips_name, state_file)

movecounts = []
movecount_dict = {}

print(event_scrambler.scramble())

for i in range(1000):
	scramble = event_scrambler.scramble()
	solution = event_scrambler.solve_scramble(scramble, False)
	movecount = event_scrambler.twips.parse_movecount(solution)
	movecounts.append(movecount)

	if (i % 100) == 0:
		print(i, end="\r")

for i in range(max(movecounts) + 1):
	movecount_dict[i] = movecounts.count(i)

print(movecount_dict)
assert movecount_dict[event_scrambler.min_optimal_filter - 1] == 0
assert event_scrambler.check_optimal_geq("R U R' U'", depth=7, QTM=False)			== False
assert event_scrambler.check_optimal_geq("R U R' U' R U", depth=7, QTM=False)		== False
assert event_scrambler.check_optimal_geq("R U R' U' R' F R", depth=7, QTM=False)	== True

# %% Pyra Clock
print("Pyra Clock")
event_scrambler = PyraminxClockSpeedsolving(twips_name, state_file)

movecounts = []
movecount_dict = {}

print(event_scrambler.scramble())

for i in range(100):
	original_scramble = event_scrambler.scramble()
	scramble = clock_movesub(original_scramble)
	solution = event_scrambler.solve_scramble(scramble)
	movecount = event_scrambler.twips.parse_movecount(solution)
	movecounts.append(movecount)

	if (i % 10) == 0:
		print(i, end="\r")

for i in range(max(movecounts) + 1):
	movecount_dict[i] = movecounts.count(i)

print(movecount_dict)
assert movecount_dict[event_scrambler.min_optimal_filter - 1] == 0
assert event_scrambler.check_optimal_geq("U5 R3' BALL2", depth=6, QTM=False)					== False
assert event_scrambler.check_optimal_geq("U2 DR2 DL2 R2' D2' L2'", depth=2, QTM=False)			== False
assert event_scrambler.check_optimal_geq("U2 DR2 DL2 BALL2 R2' D2' L2'", depth=3, QTM=False)	== False


# %% 1x3x3
print("1x3x3")
event_scrambler = Cuboid1x3x3Speedsolving(twips_name, state_file)

movecounts = []
movecount_dict = {}

print(event_scrambler.scramble())

for i in range(1000):
	scramble = scramble_move_substitution(event_scrambler.scramble(), inverse_cuboid_move_substitutions)
	solution = event_scrambler.solve_scramble(scramble, False)
	movecount = event_scrambler.twips.parse_movecount(solution)
	movecounts.append(movecount)

	if (i % 100) == 0:
		print(i, end="\r")

for i in range(max(movecounts) + 1):
	movecount_dict[i] = movecounts.count(i)

print(movecount_dict)
assert movecount_dict[event_scrambler.min_optimal_filter - 1] == 0
assert event_scrambler.check_optimal_geq("R F R", depth=4, QTM=False)				== False
assert event_scrambler.check_optimal_geq("R F R F R F R F", depth=5, QTM=False)		== False

# %% 2x2x3
print("2x2x3")
event_scrambler = Cuboid2x2x3Speedsolving(twips_name, state_file)

movecounts = []
movecount_dict = {}

print(event_scrambler.scramble())

for i in range(1000):
	scramble = scramble_move_substitution(event_scrambler.scramble(), inverse_cuboid_move_substitutions)
	solution = event_scrambler.solve_scramble(scramble, False)
	movecount = event_scrambler.twips.parse_movecount(solution)
	movecounts.append(movecount)

	if (i % 100) == 0:
		print(i, end="\r")

for i in range(max(movecounts) + 1):
	movecount_dict[i] = movecounts.count(i)

print(movecount_dict)
assert movecount_dict[event_scrambler.min_optimal_filter - 1] == 0
assert event_scrambler.check_optimal_geq("R F R", depth=4, QTM=False)			== False
assert event_scrambler.check_optimal_geq("R F R U R F", depth=3, QTM=False)		== False

# %% 2x3x3
print("2x3x3")
event_scrambler = Cuboid2x3x3Speedsolving(twips_name, state_file)

print(event_scrambler.scramble())
assert event_scrambler.check_optimal_geq("R F U R U2 R U2 R U' F", depth=5, QTM=False)			== False

# %% Sqaure-0
print("Sqaure-0")
event_scrambler = Square0Speedsolving(twips_name, state_file)

movecounts = []
movecount_dict = {}

print(event_scrambler.scramble())

for i in range(100):
	scramble = scramble_move_substitution(event_scrambler.scramble(), inverse_square0_move_substitutions)
	solution = event_scrambler.solve_scramble(scramble, False)
	movecount = event_scrambler.twips.parse_movecount(solution)
	movecounts.append(movecount)

	if (i % 10) == 0:
		print(i, end="\r")

for i in range(max(movecounts) + 1):
	movecount_dict[i] = movecounts.count(i)

print(movecount_dict)
assert movecount_dict[event_scrambler.min_optimal_filter - 1] == 0
assert event_scrambler.check_optimal_geq("R U' R D U R D' R", depth=8, QTM=False)			== False

# %% Super floppy cube
print("Super Floppy")
event_scrambler = SuperFloppySpeedsolving(twips_name, state_file)

movecounts = []
movecount_dict = {}

print(event_scrambler.scramble())

for i in range(1000):
	scramble = event_scrambler.scramble()
	solution = event_scrambler.solve_scramble(scramble, False)
	movecount = event_scrambler.twips.parse_movecount(solution)
	movecounts.append(movecount)

	if (i % 100) == 0:
		print(i, end="\r")

for i in range(max(movecounts) + 1):
	movecount_dict[i] = movecounts.count(i)

print(movecount_dict)
assert movecount_dict[event_scrambler.min_optimal_filter - 1] == 0
assert event_scrambler.check_optimal_geq("R F R B2 R' F' R", depth=3, QTM=False)			== False

# %% Ivy Cube
print("Ivy Cube")
event_scrambler = IvyCubeSpeedsolving(twips_name, state_file)

movecounts = []
movecount_dict = {}

print(event_scrambler.scramble())

for i in range(1000):
	scramble = event_scrambler.scramble()
	solution = event_scrambler.solve_scramble(scramble, False)
	movecount = event_scrambler.twips.parse_movecount(solution)
	movecounts.append(movecount)

	if (i % 100) == 0:
		print(i, end="\r")

for i in range(max(movecounts) + 1):
	movecount_dict[i] = movecounts.count(i)

print(movecount_dict)
assert movecount_dict[event_scrambler.min_optimal_filter - 1] == 0
assert event_scrambler.check_optimal_geq("R L R' L'", depth=5, QTM=False)			== False
assert event_scrambler.check_optimal_geq("R L R L' B' R B", depth=5, QTM=False)			== False

# %% Pyraminx Duo
print("Pyraminx Duo")
event_scrambler = PyraminxDuoSpeedsolving(twips_name, state_file)

movecounts = []
movecount_dict = {}

print(event_scrambler.scramble())

for i in range(1000):
	scramble = event_scrambler.scramble()
	solution = event_scrambler.solve_scramble(scramble, False)
	movecount = event_scrambler.twips.parse_movecount(solution)
	movecounts.append(movecount)

	if (i % 100) == 0:
		print(i, end="\r")

for i in range(max(movecounts) + 1):
	movecount_dict[i] = movecounts.count(i)

print(movecount_dict)
assert movecount_dict[event_scrambler.min_optimal_filter - 1] == 0
assert event_scrambler.check_optimal_geq("R' L R L' R'", depth=4, QTM=False)	== False
assert event_scrambler.check_optimal_geq("R U", depth=3, QTM=False)				== False
assert event_scrambler.check_optimal_geq("U' B U B' U", depth=4, QTM=False)		== False

# %% 2-Pentahedron
print("2 Pentahedron")
event_scrambler = Pentahedron3x2Speedsolving(twips_name, state_file)

movecounts = []
movecount_dict = {}

print(event_scrambler.scramble())

for i in range(1000):
	scramble = scramble_move_substitution(event_scrambler.scramble(), inverse_cuboid_move_substitutions)
	solution = event_scrambler.solve_scramble(scramble, False)
	movecount = event_scrambler.twips.parse_movecount(solution)
	movecounts.append(movecount)

	if (i % 100) == 0:
		print(i, end="\r")

for i in range(max(movecounts) + 1):
	movecount_dict[i] = movecounts.count(i)

print(movecount_dict)
assert movecount_dict[event_scrambler.min_optimal_filter - 1] == 0
assert event_scrambler.check_optimal_geq("R L R F L R", depth=3, QTM=False)	== False
assert event_scrambler.check_optimal_geq("R U R L R F L R L F", depth=3, QTM=False)	== False

# %% 3-Pentahedron
print("3 Pentahedron")
event_scrambler = Pentahedron3x3Speedsolving(twips_name, state_file)

movecounts = []
movecount_dict = {}

print(event_scrambler.scramble())

for i in range(1000):
	scramble = scramble_move_substitution(event_scrambler.scramble(), inverse_cuboid_move_substitutions)
	solution = event_scrambler.solve_scramble(scramble, False)
	movecount = event_scrambler.twips.parse_movecount(solution)
	movecounts.append(movecount)

	if (i % 100) == 0:
		print(i, end="\r")

for i in range(max(movecounts) + 1):
	movecount_dict[i] = movecounts.count(i)

print(movecount_dict)
assert movecount_dict[event_scrambler.min_optimal_filter - 1] == 0
assert event_scrambler.check_optimal_geq("R L R F L R", depth=3, QTM=False)	== False
assert event_scrambler.check_optimal_geq("R U R L R F L R L F", depth=3, QTM=False)	== False

# %% Pyramorphix
print("Pyramorphix")
event_scrambler = PyramorphixSpeedsolving(twips_name, state_file)

movecounts = []
movecount_dict = {}

print(event_scrambler.scramble())

for i in range(1000):
	scramble = event_scrambler.scramble()
	solution = event_scrambler.solve_scramble(scramble, False)
	movecount = event_scrambler.twips.parse_movecount(solution)
	movecounts.append(movecount)

	if (i % 100) == 0:
		print(i, end="\r")

for i in range(max(movecounts) + 1):
	movecount_dict[i] = movecounts.count(i)

print(movecount_dict)
assert movecount_dict[event_scrambler.min_optimal_filter - 1] == 0
assert event_scrambler.check_optimal_geq("R2 B2 R2 L2 R2", depth=4, QTM=False)	== False


# %% Dino Cube
print("Dino Cube")
event_scrambler = DinoCubeSpeedsolving(twips_name, state_file)

movecounts = []
movecount_dict = {}

print(event_scrambler.scramble())

for i in range(100):
	scramble = event_scrambler.scramble()
	solution = event_scrambler.solve_scramble(scramble, False)
	movecount = event_scrambler.twips.parse_movecount(solution)
	solution2 = event_scrambler.solve_scramble("U UL' U UL' U R D' R D' R " + scramble)
	movecount2 = event_scrambler.twips.parse_movecount(solution2)
	movecounts.append(min(movecount, movecount2))

	if (i % 10) == 0:
		print(i, end="\r")

for i in range(max(movecounts) + 1):
	movecount_dict[i] = movecounts.count(i)

print(movecount_dict)
assert movecount_dict[event_scrambler.min_optimal_filter - 1] == 0
assert event_scrambler.check_optimal_geq("UL D R' U R U' D' UL'", depth=5, QTM=False)	== False


# %% Super gear cube
print("Super Gear Cube")
event_scrambler = SuperGearCubeSpeedsolving(twips_name, state_file)

movecounts = []
movecount_dict = {}

print(event_scrambler.scramble())

for i in range(1000):
	scramble = event_scrambler.scramble()
	solution = event_scrambler.solve_scramble(scramble, False)
	movecount = event_scrambler.twips.parse_movecount(solution)
	movecounts.append(movecount)

	if (i % 100) == 0:
		print(i, end="\r")

for i in range(max(movecounts) + 1):
	movecount_dict[i] = movecounts.count(i)

print(movecount_dict)
assert movecount_dict[event_scrambler.min_optimal_filter - 1] == 0
assert event_scrambler.check_optimal_geq("R' F R U R' F R U", depth=3, QTM=False)	== False

# %% gear cube
print("Gear Cube")
event_scrambler = GearCubeSpeedsolving(twips_name, state_file)

movecounts = []
movecount_dict = {}

print(event_scrambler.scramble())

for i in range(1000):
	scramble = event_scrambler.scramble()
	solution = event_scrambler.solve_scramble(scramble, False)
	movecount = event_scrambler.twips.parse_movecount(solution)
	movecounts.append(movecount)

	if (i % 100) == 0:
		print(i, end="\r")

for i in range(max(movecounts) + 1):
	movecount_dict[i] = movecounts.count(i)

print(movecount_dict)
assert movecount_dict[event_scrambler.min_optimal_filter - 1] == 0
assert event_scrambler.check_optimal_geq("R' F R U R' F R U", depth=3, QTM=False)	== False

# %% CTO
event_scrambler = CornerTurningOctahedronSpeedsolvingTwoPhase(twips_name, state_file)

print(event_scrambler.scramble())

assert event_scrambler.check_optimal_geq("L R' U R U' D R' U R U' D' L'", depth=5, QTM=False)	== False