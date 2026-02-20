#!/usr/bin/env python3
import optparse

from events import *


def main():
    twips_name = "./twips_cli/twips"
    state_file = "patterns/scramble-pattern.json"

    event_names = [
        "clock",
        "222fm",
        "mfto",
        "pyra_clock"
    ]


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


    if not (options.event in event_names):
        print(f"Invalid EventID: \"{options.event}\"")
        return


    match(options.event):
        case "clock":
            event_scrambler = ClockSpeedsolving()
        case "222fm":
            event_scrambler = Cube2x2x2FewestMoves(twips_name, state_file)
        case "mfto":
            event_scrambler = Octahedron4x4x4Speedsolving()
        case "pyra_clock":
            event_scrambler = PyraminxClockSpeedsolving()


    event_scrambler.scramble_rounds(options.rounds, options.output_file)
    # event_scrambler.scramble_rounds(options.rounds, )


if __name__ == "__main__":
    main()



