############################################################
#   Adventure
############################################################

import argparse
import sys
import os
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

    def walk(self):

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


############################################################
#   COMMAND LINE INTERFACE
############################################################

adventure_cli = argparse.ArgumentParser(
    prog="adventure",
    description="Let's go on an adventure!",
    epilog="Have fun!",
)

adventure_cli__world_file = adventure_cli.add_mutually_exclusive_group(required=False)

adventure_cli__world_file.add_argument(
    "--path",
    "-p",
    default=None,
    action="store",
)

adventure_cli__world_file.add_argument(
    "--example",
    "-e",
    nargs="?",
    default=None,
    action="store",
)

adventure_cli.add_argument(
    "--test",
    "-t",
    default=True,
    action="store_true",
)

adventure_cli.add_argument(
    "--walk",
    "-w",
    default=None,
    action="store_true",
)

adventure_cli.add_argument(
    "--walk-before-test",
    "--walk-before",
    "-wbt",
    "-wb",
    default=None,
    action="store_true",
)

adventure_cli.add_argument(
    "--walk-after-test",
    "--walk-after",
    "-wat",
    "-wa",
    default=None,
    action="store_true",
)


def normpath_join(*args):
    return os.path.normpath(os.path.join(*args))


############################################################
#   MAIN
############################################################

if __name__ == "__main__":

    args = sys.argv
    # print(args)
    kwargs = adventure_cli.parse_args(args[1:])
    print(kwargs)

    current_dir = os.getcwd()
    # print(current_dir)
    project_dir = normpath_join(args[0], "../")
    # print(project_dir)
    examples_dir = normpath_join(project_dir, "../maps")
    # print(examples_dir)
    examples_ext = ".txt"
    # print(examples_ext)
    world_file = None
    # print(world_file)

    if kwargs.path:

        world_file = normpath_join(project_dir, kwargs.path)

    else:

        # world_file = "./maps/test_line.txt"
        # world_file = "./maps/test_cross.txt"
        # world_file = "./maps/test_loop.txt"
        # world_file = "./maps/test_loop_fork.txt"
        # world_file = "./maps/main_maze.txt"
        example_name = kwargs.example or "main_maze"

        if example_name.endswith(examples_ext):
            example_name = example_name[:-len(examples_ext)]

        world_file = normpath_join(examples_dir, example_name + examples_ext)

    # print(world_file)

    walk_before_test = False
    walk_after_test = False

    if kwargs.walk is True:

        if kwargs.walk_before_test is None and kwargs.walk_after_test is None:

            walk_before_test = True

    if kwargs.walk is not False:

        if kwargs.walk_before_test:
            walk_before_test = True

        if kwargs.walk_after_test:
            walk_after_test = True

    #-----------------------------------------------------------

    adventure = Adventure(world_file)

    if walk_before_test:

        adventure.walk()

    if kwargs.test:

        adventure.test_traversal()

    if walk_after_test:

        adventure.walk()
