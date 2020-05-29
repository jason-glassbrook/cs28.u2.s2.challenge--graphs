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
from .memory_graph import MemoryGraph

############################################################


class Adventure:

    def __init__(self, world_file):

        # Load world.
        self.world = World()

        # Load the map into a dictionary.
        self.world_info = ast.literal_eval(open(world_file, "r").read())
        self.world.load_graph(self.world_info)

        # Initialize the player.
        self.player = Player(self.world.starting_room)

        return

    def show_map(self):

        # Print an ASCII map of the world.
        self.world.print_rooms()

        return

    def walk(self):

        player = self.player

        player.current_room.print_room_description(player)

        while True:
            cmds = input("-> ").lower().strip().split(" ")
            if cmds[0] in ["n", "s", "e", "w"]:
                player.travel(cmds[0], True)
            elif cmds[0] == "q":
                break
            else:
                print("I did not understand that command.")

        return

    def traverse_world(self):

        #===========================================================
        #   HELPERS
        #-----------------------------------------------------------

        UNKNOWN = "?"

        def get_unknown_directions(memory, room_id):
            return tuple(
                direction for (direction, to_room_id) in memory.map[room_id].items()
                if to_room_id == UNKNOWN
            )

        def has_unknown_directions(memory, room_id):
            return (UNKNOWN in memory.map[room_id].values())

        def path_to_edge_of_unknown(memory, room_id):

            def found_edge_of_unknown(curr_room_id, *rest):
                # Returns `True` when `curr_room_id` points to `UNKNOWN`.
                return has_unknown_directions(memory, curr_room_id)

            return memory.bfs(found_edge_of_unknown, room_id)

        def record_room(memory, player):

            room = player.current_room

            if room.id not in memory:
                # Add node to memory.
                memory.add_node(room.id)

                for direction in room.get_exits():
                    # Record a "blank" edge.
                    memory.add_edge(room.id, direction, UNKNOWN)

            else:
                # Record any missing connections.
                for direction in room.get_exits():
                    if direction not in memory.map[room.id]:
                        memory.add_edge(room.id, direction, UNKNOWN)

            return memory.map[room.id]

        def choose_direction(memory, player):

            room = player.current_room
            unknown_directions = get_unknown_directions(memory, room.id)

            if unknown_directions:
                # Randomly choose a direction.
                return random.choice(unknown_directions)

            else:
                # There's nowhere new to go.
                return None

        def move_to(memory, player, direction):

            from_room = player.current_room
            player.travel(direction)
            to_room = player.current_room

            # Remember this connection!
            memory.add_both_edges(from_room.id, direction, to_room.id)

            return (direction, to_room.id)

        def move_from(memory, player, direction):

            inverse_direction = memory.inverse_labels[direction]

            from_room = player.current_room
            player.travel(inverse_direction)
            to_room = player.current_room

            # Remember this connection!
            memory.add_both_edges(from_room.id, inverse_direction, to_room.id)

            return (direction, to_room.id)

        #===========================================================

        # World:
        world = self.world
        room_count = len(self.world.rooms)

        # Player:
        player = self.player
        player.current_room = world.starting_room

        # Player "Memory":
        memory = MemoryGraph(inverse_edge_label_pairs=(
            ("n", "s"),
            ("e", "w"),
        ))

        # Traversed Path: a list of `(move, to_node)`
        traversed_path = [(None, player.current_room)]

        while len(memory.map) < room_count:
            break

        return traversed_path

    def test_traverse_world(self):

        world = self.world
        world_info = self.world_info
        player = self.player

        # Run and unpack results.
        traversed_path = self.traverse_world()
        traversed_moves = tuple(
            move for (move, *rest) in traversed_path[1:]
        )    # -- this takes all moves except the first (which is None).

        # TRAVERSAL TEST - DO NOT MODIFY
        visited_rooms = set()
        player.current_room = world.starting_room
        visited_rooms.add(player.current_room)

        for move in traversed_moves:
            player.travel(move)
            visited_rooms.add(player.current_room)

        if len(visited_rooms) == len(world_info):
            print(
                f"TESTS PASSED: {len(traversed_moves)} moves, {len(visited_rooms)} rooms visited"
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
    # print(kwargs)

    current_dir = os.getcwd()
    # print(current_dir)
    project_dir = normpath_join(os.path.dirname(args[0]), "../")
    # print(project_dir)
    examples_dir = normpath_join(project_dir, "./maps")
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

        adventure.test_traverse_world()

        if walk_after_test:
            adventure.walk()

    else:

        if walk:
            adventure.walk()
