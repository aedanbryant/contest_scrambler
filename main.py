#!/usr/bin/env python3
import optparse

from events import *


def main():
    twips_name = "./twips_cli/twips"
    state_file = "patterns/scramble-pattern.json"

    # event_names = [
    #     "clock",
    #     "222fm",
    #     "mfto",
    #     "pyra_clock",
    #     "133_cuboid",
    #     "223_cuboid",
    #     "233_cuboid",
    #     "2pentahedron",
    #     "3pentahedron",
    #     "sq0"
    # ]


    parser = optparse.OptionParser()

    parser.add_option("-e", "--event", 
                    dest="event",
                    type="string",
                    help="Event ID to generate scrambles for")
    parser.add_option("-r", "--rounds",
                    dest="rounds",
                    type="int")
    parser.add_option("-o", "--out",
                    dest="output_file")

    (options, args) = parser.parse_args()


    # if not (options.event in event_names):
    #     print(f"Invalid EventID: \"{options.event}\"")
    #     return


    match(options.event):
        case "clock":
            event_scrambler = ClockSpeedsolving()
        case "222fm":
            event_scrambler = Cube2x2x2FewestMoves(twips_name, state_file)
        case "mfto":
            event_scrambler = Octahedron4x4x4Speedsolving()
        case "pyra_clock":
            event_scrambler = PyraminxClockSpeedsolving()
        case "133_cuboid":
            event_scrambler = Cuboid1x3x3Speedsolving(twips_name, state_file)
        case "223_cuboid":
            event_scrambler = Cuboid2x2x3Speedsolving(twips_name, state_file)
        case "233_cuboid":
            event_scrambler = Cuboid2x3x3Speedsolving(twips_name, state_file)
        case "2pentahedron":
            event_scrambler = Pentahedron3x2Speedsolving(twips_name, state_file)
        case "3pentahedron":
            event_scrambler = Pentahedron3x3Speedsolving(twips_name, state_file)
        case "sq0":
            event_scrambler = Square0Speedsolving(twips_name, state_file)
        case _:
            print(f"Invalid EventID: \"{options.event}\"")
            return

    event_scrambler.scramble_rounds(options.rounds, options.output_file)


if __name__ == "__main__":
    main()



