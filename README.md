
Options:

```
--events <Event ID 1>:<Event ID 2> (repeat for as many events as necessary)
--groups <Number of rounds for event 1 round 1>,<Number of rounds for event 1 round 2>:<Number of rounds for event 2 round 1> (repeat for as many events & rounds as necessary)
--name <Competition Name>
--scrambles <number of scrambles>
--extras <number of extras>
--pdf <generate PDF>
```

Events currently supported:

| Event Name | Event ID | Random State | Min Optimal | Scramble Length | Padding |
| -----------|----------|--------------|-------------|-----------------|---------|
| 2x2x2 Fewest Moves | 222fm | Yes | 7 | 17 | R' U' F |
| Master Face-Turning Octahedron | mfto | No | N/A | N/A | None |
| Super Floppy Cube | super_133 | Yes | 7 | 11 | None |
| 1x3x3 | 133_cuboid | Yes | 3 | 8 | None |
| 2x2x3 | 223_cuboid | Yes | 7 | 11 | None |
| 2x3x3 | 233_cuboid | Yes | 2 | None | None |
| 2-layer Pentahedron | 2pentahedron | Yes | 7 | 11 | None |
| 3-layer Pentahedron | 3pentahedron | Yes | 8 | 11 | None |
| Square-0 | sq0 | Yes | 6 | 11 | None |
| CTO | cto | Pseudo | 2 | None | None |
| Ivy Cube | ivy_cube | Yes | 4 | 8 | None |
| Pyraminx Duo | pyram_duo | Yes | 2 | 4 | None |
| Dino Cube | dino | Yes | 7 | 11 | None |
| Pyramorphix | pyramorphix | Yes | 5 | 9 | None |
| Super Gear Cube | super_gear_cube | Pseudo | 4 | 8 | None |
| Gear Cube | gear_cube | Pseudo | 3 | 6 | None |
| Baby FTO | baby_fto | Yes | 5 | 10 | None |
| Kilominx | kilominx | Yes | 2 | None | None |


Possible additions to add:
- 3x3 with supercube centers
- 8x8+
- Master Kilominx+
- 3x3x4
- Rainbow Ball (IDK how to make kpuzzle def for this)

Example command to generate all rounds:
uv run main.py --events 444fm:mfto:clock:pyra_clock:penta_clock:new_penta_clock:222fm:133_cuboid:223_cuboid:233_cuboid:2pentahedron:3pentahedron:sq0:super_133:ivy_cube:pyram_duo:dino:cto:pyramorphix:super_gear_cube:gear_cube:baby_fto:kilominx --groups 1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1 --name "Test Open 2026" --pdf
