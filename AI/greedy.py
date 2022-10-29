"""
This file contains an implementation of a greedy AI with some enhancements to ensure a more complex competition
Originally implemented to test and tune the minimax AI, it can be used as an easy competitor.
"""
from Game.actions import new_position, workerLoc, out_bounds, max_height, get_level_from_board, board


def evaluate_options(highest, start_pos, c_level, friend_index):
    """
    Given a starting position attempt to find the best position and give it a score

    :param highest: A list containing the current highest buildings, if there are no buildings it is an empty list
    :param start_pos: The starting position of the current worker
    :param c_level: The level of the current worker
    :param friend_index: The index representing the friend to the current worker
    :return: A list containing a flag (Move or Build), a score and the new position
    """
    if not highest:  # There are no higher buildings so build one
        return [False, 10, best_build(start_pos, can_reach(start_pos, highest, c_level, "move"), friend_index)]

    # Can move to higher buildings
    elif int(highest[1]) != c_level:
        # There's a few higher buildings so need to find which can be reached
        if len(highest) > 1:
            new_pos = can_build(highest, c_level, start_pos, friend_index)
            if not new_pos[0]:
                return [True, 15, new_pos[1]]
            else:
                return [False, 15, new_pos[1]]

        # Only 1 building that needs to be moved towards
        else:
            direction = get_direction(start_pos, highest[0])  # Move in this direction
            move_pos = new_position(direction, start_pos)

            if move_pos not in workerLoc and int(highest[1]) - 1 == c_level:
                return [True, 25, move_pos]
            else:
                return [False, 20, can_build(highest, c_level, start_pos, friend_index)[1]]

    else:  # Already at the highest level
        new_pos = can_build(highest, c_level, start_pos, friend_index)
        if new_pos[0]:
            return [False, 30, new_pos[1]]
        else:
            return [False, 30, new_pos]


def get_highest():
    """
    Get the highest buildings currently on the board

    :return: A list containing the highest buildings and their level
    """
    highest, build_loc = [], []

    for i in range(5):
        for j in range(5):
            if board[i][j] in ["| L1 |", "| L2 |", "| L3 |"]:
                build_loc.append([i, j])

    if not build_loc:
        return

    for build in build_loc:
        if not max_height(build):  # Not a valid building
            level = get_level_from_board(build)
            if not highest:  # First building to be checked so automatically the highest
                highest = [build, level]
            else:
                for i in range(len(build_loc) - 1):  # Already checked first building
                    if build != highest[0] and highest[1] < level:  # New building higher level so replace
                        highest = [build, level]

                    elif highest[1] == level and highest[0] != build:  # New building same level so append
                        highest.append(build)
    return highest


def std_ref(ref):
    """
    Take either a worker or building reference and only return the level

    :param ref: The reference to the building or worker
    :return: Integer representing the current level
    """
    return ref.replace("|", "").replace(" ", "").replace("L", "").replace("C", "").replace("D", "")


def best_build(start_pos, reach, friend_index):
    """
    Find the best position to be built on

    :param start_pos: The current workers position
    :param reach: The building reach of the worker
    :param friend_index: The index of the current workers friend
    :return: The best position to build in
    """
    for pos in reach:
        if get_level_from_board(pos) > 0 and not max_height(pos):  # First check if a nearby building can be used
            return pos

    # Attempt to build towards friend worker
    friend_pos = friend_loc(friend_index)

    if friend_loc(friend_index) in reach:
        return friend_pos
    else:
        space_around = get_space_around(start_pos, friend_pos, reach)
        if space_around:  # Build near friend
            return space_around
        else:  # Cannot build towards other worker so next available space
            return reach[0]


def can_build(highest, c_level, start_pos, friend_index):
    """
    Evaluate the current buildings around the worker and return the best position to either climb or build on

    :param highest: A list containing the highest buildings
    :param c_level: The current workers level
    :param start_pos: The current workers initial position
    :param friend_index: The index of the workers friend
    :return: A flag (Climb or build) and the new position to perform that action on
    """
    reachable = can_reach(start_pos, highest, c_level, "build")
    build_same = []
    build_new = []

    # Going to climb or build
    for pos in reachable:
        # Know there is a building to check
        pos_level = get_level_from_board(pos)
        if pos_level > 0:
            if pos_level - 1 == c_level:  # Building can be climbed
                return False, new_position(get_direction(start_pos, pos), start_pos)

            # Opportunity for worker to build on top of another building
            elif pos_level == c_level:
                build_same.append(pos)

        # Worker has to build new
        elif pos not in workerLoc:
            build_new.append(pos)

    # Shows priority of opportunities
    if build_same:  # Building same level so building on it
        return True, build_same[0]
    elif build_new:  # No available buildings, so build new one
        return True, best_build(start_pos, can_reach(start_pos, highest, c_level, "build"), friend_index)
    else:  # No position to build or move to
        return True, get_best(highest, reachable)


def can_reach(start_pos, highest, c_level, movement):
    """
    Given a movement type (Climb or build) return a list of all possible positions the given action can be done for

    :param start_pos: The workers initial position
    :param highest: The current highest buildings on the board
    :param c_level: The current workers level
    :param movement: A flag representing either Climb (True) or Build (False)
    :return: The current reach of the worker
    """
    reach, match = [], []
    # Going through all adjacent spaces
    for op in ["W", "A", "S", "D", "WA", "WD", "SA", "SD"]:
        pos = new_position(op, start_pos)

        # Position in bounds, not occupied by worker and not already realised
        if pos not in workerLoc and not out_bounds(pos) and not max_height(pos) and pos not in reach:
            pos_level = get_level_from_board(pos)
            if pos_level > 0 and movement == "climb":
                b_level = get_level_from_board(pos)

                if b_level - 1 == c_level or b_level == c_level or b_level < c_level:
                    reach.append(pos)

                for val in highest:
                    if val[0] in reach:
                        match.append(val[0])

            elif pos_level == 0 and movement == "move":
                match.append(pos)

            else:  # If wanting to build, can build at any level as long as no worker
                match.append(pos)
    if len(match) > 1:
        return match
    else:
        return match[0]


def get_best(highest, reachable):
    """
    A last resort to find the best position to move to given access to buildings

    :param highest: List of the highest buildings on the board
    :param reachable: Current reach of the selected worker
    :return: Either the best position to move to or nothing
    """
    best = []

    for pos in reachable:
        pos_reach = len(can_reach(pos, highest, highest[1], "climb"))  # Each reachable buildings counts as a point
        pos_level = get_level_from_board(pos)

        if pos_level > 0:  # Being able to climb selected pos adds values
            pos_reach += 1

        best.append(pos_reach)

    if len(best) > 1:
        return reachable[best.index(max(best))]


def get_space_around(current_pos, friend_pos, reach):
    """
    If a building cannot be reached via WASD directions attempt to use WA, WD, SA an SD

    :param current_pos: Current position of the worker
    :param friend_pos: Current position of the workers friend
    :param reach: Current move reach of the worker
    :return: The next best position
    """
    if current_pos[0] == friend_pos[0] or current_pos[1] == friend_pos[1]:  # On same row or in same column
        above_pos = [friend_pos[0] + 1, friend_pos[1]]
        below_pos = [friend_pos[0] - 1, friend_pos[1]]

        left_pos = [friend_pos[0], friend_pos[1] + 1]
        right_pos = [friend_pos[0], friend_pos[1] - 1]

    else:  # Do not share a row or column
        above_pos = [current_pos[1] - 1, current_pos[1] - 1]
        below_pos = [current_pos[1] - 1, current_pos[1] + 1]

        left_pos = [current_pos[0] + 1, current_pos[0] - 1]
        right_pos = [current_pos[0] + 1, current_pos[0] + 1]

    # Return applicable position, no preference of order
    if above_pos in reach:
        return above_pos
    elif below_pos in reach:
        return below_pos
    elif left_pos in reach:
        return left_pos
    elif right_pos in reach:
        return right_pos


def get_direction(start_pos, target_pos):
    """
    Given the starting and target positions get the direction required to move to or towards the target

    :param start_pos: The initial position of the worker
    :param target_pos: The desired position of the worker
    :return: A string representing the relevant direction
    """
    start_x, start_y = start_pos[0], start_pos[1]  # Left/Right
    new_x, new_y = target_pos[0], target_pos[1]  # Up/Down

    x_change = start_x - new_x
    y_change = start_y - new_y

    if x_change == 0 and y_change >= 1:
        return "A"
    elif x_change == 0 and y_change <= -1:
        return "D"
    elif y_change == 0 and x_change >= 1:
        return "W"
    elif y_change == 0 and x_change <= -1:
        return "S"
    elif x_change >= 1 and y_change >= 1:
        return "WA"
    elif x_change >= 1 and y_change <= -1:
        return "WD"
    elif x_change <= -1 and y_change <= -1:
        return "SD"
    elif x_change <= -1 and y_change >= 1:
        return "SA"


def friend_loc(index):
    """
    Give the location of the workers friend

    :param index: Current workers index
    :return: The friends location
    """
    if index == 0:
        return workerLoc[3]
    else:
        return workerLoc[2]
