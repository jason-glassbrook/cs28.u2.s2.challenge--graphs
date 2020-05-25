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

        # initialize the player
        self.player = Player(self.world.starting_room)

        return

    def show_map(self):

        # print an ASCII map of the world
        self.world.print_rooms()

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

#-----------------------------------------------------------
#   World File
#-----------------------------------------------------------

adventure_cli__world_file = adventure_cli.add_mutually_exclusive_group(required=False)

adventure_cli__world_file.add_argument(
    "--path",
    "-p",
    action="store",
)

adventure_cli__world_file.add_argument(
    "--example",
    "-e",
    nargs="?",
    action="store",
)

#-----------------------------------------------------------
#   Show Map
#-----------------------------------------------------------

adventure_cli__show_map = adventure_cli.add_mutually_exclusive_group(required=False)

adventure_cli__show_map.add_argument(
    "--map",
    "-m",
    "--yes-map",
    "-ym",
    default=None,
    action="store_true",
)

adventure_cli__show_map.add_argument(
    "--no-map",
    "-nm",
    default=None,
    action="store_true",
)

#-----------------------------------------------------------
#   Run Test
#-----------------------------------------------------------

adventure_cli__run_test = adventure_cli.add_mutually_exclusive_group(required=False)

adventure_cli__run_test.add_argument(
    "--test",
    "-t",
    "--yes-test",
    "-yt",
    default=None,
    action="store_true",
)

adventure_cli__run_test.add_argument(
    "--no-test",
    "-nt",
    default=None,
    action="store_true",
)

#-----------------------------------------------------------
#   Walk Modes
#-----------------------------------------------------------

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

#-----------------------------------------------------------


def normpath_join(*args):
    return os.path.normpath(os.path.join(*args))


############################################################
#   MAIN
############################################################

DEFAULT__EXAMPLE = "main_maze"
# "test_line"
# "test_cross"
# "test_loop"
# "test_loop_fork"
# "main_maze"
DEFAULT__SHOW_MAP = True
DEFAULT__RUN_TEST = True
DEFAULT__WALK = False
DEFAULT__WALK_BEFORE_TEST = False
DEFAULT__WALK_AFTER_TEST = False

#-----------------------------------------------------------

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

    #-----------------------------------------------------------
    #   World File
    #-----------------------------------------------------------

    if kwargs.path:

        world_file = normpath_join(project_dir, kwargs.path)

    else:

        example_name = kwargs.example or DEFAULT__EXAMPLE

        if example_name.endswith(examples_ext):
            example_name = example_name[:-len(examples_ext)]

        world_file = normpath_join(examples_dir, example_name + examples_ext)

    # print("world file:", world_file)

    #-----------------------------------------------------------
    #   Show Map
    #-----------------------------------------------------------

    show_map = DEFAULT__SHOW_MAP

    if kwargs.map is not None:
        show_map = True

    if kwargs.no_map is not None:
        show_map = False

    #-----------------------------------------------------------
    #   Run Test
    #-----------------------------------------------------------

    run_test = DEFAULT__RUN_TEST

    if kwargs.test is not None:
        run_test = True

    if kwargs.no_test is not None:
        run_test = False

    #-----------------------------------------------------------
    #   Walk Modes
    #-----------------------------------------------------------

    walk = DEFAULT__WALK
    walk_before_test = DEFAULT__WALK_BEFORE_TEST
    walk_after_test = DEFAULT__WALK_AFTER_TEST

    if kwargs.walk is not None:
        walk = kwargs.walk

    if kwargs.walk is True:

        if kwargs.walk_before_test is None and kwargs.walk_after_test is None:
            walk_before_test = True

    if kwargs.walk is not False:

        if kwargs.walk_before_test:
            walk_before_test = True

        if kwargs.walk_after_test:
            walk_after_test = True

    # print("test:", test)
    # print("walk before test:", walk_before_test)
    # print("walk after test:", walk_after_test)

    #-----------------------------------------------------------

    adventure = Adventure(world_file)

    if show_map:
        adventure.show_map()

    if run_test:

        if walk_before_test:
            adventure.walk()

        adventure.test_traversal()

        if walk_after_test:
            adventure.walk()

    else:

        if walk:
            adventure.walk()
