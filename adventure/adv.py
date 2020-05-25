############################################################
#   Adventure
############################################################

import ast
import random

from .room import Room
from .player import Player
from .world import World

############################################################


class Adventure:

    def __init__(self, world_file):

        # load world
        self.world = World()

        # load the map into a dictionary
        self.world_info = ast.literal_eval(open(world_file, "r").read())
        self.world.load_graph(self.world_info)

        # print an ASCII map of the world
        self.world.print_rooms()

        # initialize the player
        self.player = Player(self.world.starting_room)

        return

    def explore(self):

        player = self.player

        player.current_room.print_room_description(player)

        while True:
            cmds = input("-> ").lower().split(" ")
            if cmds[0] in ["n", "s", "e", "w"]:
                player.travel(cmds[0], True)
            elif cmds[0] == "q":
                break
            else:
                print("I did not understand that command.")

        return

    def test_traversal(self):

        world = self.world
        world_info = self.world_info
        player = self.player

        # Fill this out with directions to walk
        # traversal_path = ['n', 'n']
        traversal_path = []

        # TRAVERSAL TEST - DO NOT MODIFY
        visited_rooms = set()
        player.current_room = world.starting_room
        visited_rooms.add(player.current_room)

        for move in traversal_path:
            player.travel(move)
            visited_rooms.add(player.current_room)

        if len(visited_rooms) == len(world_info):
            print(
                f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
            )
        else:
            print("TESTS FAILED: INCOMPLETE TRAVERSAL")
            print(f"{len(world_info) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
