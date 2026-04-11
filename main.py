#!/usr/bin/env python3
import optparse
from datetime import datetime
import os

from events import *



def main():
    twips_name = "./twips_cli/twips"
    state_file = "patterns/scramble-pattern.json"


    parser = optparse.OptionParser()

    parser.add_option("-e", "--events", 
                    dest="events",
                    type="string",
                    help="Event ID to generate scrambles for")
    parser.add_option("-g", "--groups",
                    dest="groups",
                    type="string")
    parser.add_option("-n", "--name",
                    dest="name",
                    type="string")
    parser.add_option("-s", "--scrambles",
                    dest="num_scrambles",
                    type="int")
    parser.add_option("-x", "--extras",
                    dest="num_extras",
                    type="int")
    parser.add_option("-p", "--pdf",
                      action="store_true",
                      dest="pdf",
                      default=False)
    
    

    (options, args) = parser.parse_args()

    timestamp = datetime.now()

    competition_scrambles = {"competition_name": options.name, "generation_time": timestamp.strftime("%Y-%m-%d %H:%M:%S"), "events": []}

    try:
        events = options.events.split(":")
    except:
        print("Invalid format, use e1:e2:...,en")
        return

    try:
        event_groups = options.groups.split(":")
    except:
        print("Invalid event group format, use e1_r1,e1_r2...:e2_r1,e2_r1:...:en_gn")
        return
    
    if len(events) != len(event_groups):
        print("Number of events must match number of event groups")
        return

    # Create competition folder
    comp_dir = f"output/{options.name}_{timestamp.strftime("%Y%m%d%H%M%S")}"
    
    os.mkdir(comp_dir)
    os.mkdir(f"{comp_dir}/html")
    if options.pdf: os.mkdir(f"{comp_dir}/pdf")

    for i, event in enumerate(events):

        match(event):
            case "444fm":
                event_scrambler = Cube4x4x4FewestMoves()
            case "mfto":
                event_scrambler = Octahedron4x4x4Speedsolving()
            case "clock":
                event_scrambler = ClockSpeedsolving()
            case "pyra_clock":
                event_scrambler = PyraminxClockSpeedsolving(twips_name, state_file)
            case "penta_clock":
                event_scrambler = PentagonalClockSpeedsolving(twips_name, state_file)
            case "new_penta_clock":
                event_scrambler = NewPentagonalClockSpeedsolving(twips_name, state_file)
            case "222fm":
                event_scrambler = Cube2x2x2FewestMoves(twips_name, state_file)
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
            case "super_133":
                event_scrambler = SuperFloppySpeedsolving(twips_name, state_file)
            case "ivy_cube":
                event_scrambler = IvyCubeSpeedsolving(twips_name, state_file)
            case "pyram_duo":
                event_scrambler = PyraminxDuoSpeedsolving(twips_name, state_file)
            case "dino":
                event_scrambler = DinoCubeSpeedsolving(twips_name, state_file)
            case "cto":
                event_scrambler = CornerTurningOctahedronSpeedsolvingTwoPhase(twips_name, state_file)
            case "pyramorphix":
                event_scrambler = PyramorphixSpeedsolving(twips_name, state_file)
            case "super_gear_cube":
                event_scrambler = SuperGearCubeSpeedsolving(twips_name, state_file)
            case "gear_cube":
                event_scrambler = GearCubeSpeedsolving(twips_name, state_file)
            case "baby_fto":
                event_scrambler = BabyFTOSpeedsolving(twips_name)
            case "kilominx":
                event_scrambler = KilominxSpeedsolving(twips_name)
            case _:
                print(f"Invalid EventID: \"{options.event}\"")
                return

        try:
            groups = [int(x) for x in event_groups[i].split(",")]
        except:
            print("Invalid group format, use r1,r2,...,rn")
            return

        # event_scrambler.scramble_rounds(options.rounds, options.output_file)
        competition_scrambles["events"].append(event_scrambler.scramble_rounds(groups, options.name, comp_dir, options.num_scrambles, options.num_extras, options.pdf))


    with open(f"{comp_dir}/{options.name}_{timestamp.strftime("%Y%m%d%H%M%S")}_.json", "w") as f:
        json.dump(competition_scrambles, f, indent=4)


if __name__ == "__main__":
    main()



