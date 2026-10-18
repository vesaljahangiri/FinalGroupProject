MAP = [
    "###############",
    "#@....#.......#",
    "#.###.#.F.....#",
    "#...#.#.......#",
    "###.#.#########",
    "#...#....M....#",
    "#.#####.#####.#",
    "#.....#.......#",
    "#####.#.#####.#",
    "#.....#.S.....#",
    "#.#####.#####.#",
    "#.....#.......#",
    "#####.#.#####.#",
    "#.....#.B.....#",
    "#.....#######E#",
    "###############",
]
TILE_TO_ENEMY = {
    "F": "forgotten",
    "M": "mutant",
    "S": "sentinel",
    "B": "barachiel",
}
STORY = {
    (1, 5): "The stone bears Uriel's warning: 'The prison was built to hold a traitor, not to keep intruders out.'",
    (5, 7): "A cold voice whispers through the walls: 'Barachiel was once Heaven's brightest blade.'",
    (11, 7): "Uriel's voice returns: 'Find the fallen one. End his vigil, and I shall be free.'",
}
LOCATIONS = {
    (1, 1): {
        "name": "The Entrance",
        "desc": "A narrow passage leads into the sealed prison.",
        "item": None,
    },
    (5, 2): {
        "name": "The Surgeon's Cache",
        "desc": "A bloodstained workbench sits beneath a broken lamp.",
        "item": None,
    },
    (13, 9): {
        "name": "Barachiel's Sanctum",
        "desc": "The air trembles with the weight of an ancient presence.",
        "item": None,
    },
}
TREASURES = {
    (5, 2): ["Scalpel"],
    (5, 10): ["Bone Shield"],
}
def print_map():
    """Print the full dungeon map and its legend."""
    for row in MAP:
        print(row)
    print("\n@ You  # Wall  F Forgotten  M Mutant  S Sentinel")
    print("B Barachiel  T Treasure  E Exit")
if __name__ == "__main__":
    print_map()
