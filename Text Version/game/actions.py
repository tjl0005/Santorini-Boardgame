"""
This file enables players to perform actions (moving, climbing and building) with their workers.
"""
from ..misc.exceptions import BoundsError, SelectionError, SpaceTakenError

board = [["|    |" for a in range(5)] for b in range(5)]  # Build the board
workerLoc = []  # Track the worker locations

# Dictionary to get the label for a specified build level
buildCode = {
    1: "| L1 |",
    2: "| L2 |",
    3: "| L3 |",
    4: "| {} |"
}


def worker_move(player, start_pos, ref_index, new_pos):
    """
    Given a new position move the selected worker to that position. This movement will be validated before the board is
    updated.

    :param player: The player to perform the action for
    :param start_pos: A list containing the starting positions of players workers in format of [[0, 0], [1, 1]]
    :param ref_index The workers reference index
    :param new_pos The position to move to
    :return: A list containing the new current positions
    """
    if new_pos in [5, -1]:  # Player attempting to go out of bounds
        print("Fault 3")
        raise BoundsError
    elif new_pos in workerLoc:  # Space in use by another player
        print("Fault 4")
        raise SpaceTakenError
    else:  # Standard movement
        p_ref, level_index = find_level_index(player[ref_index])

        if get_level_from_board(new_pos) > 0:  # If space needs to be climbed
            building_level = get_level_from_board(new_pos)
            worker_level = player[level_index]

            if 0 < worker_level > building_level:
                player[level_index] -= 1
                update_ref(p_ref, player, ref_index, level_index)
                board[start_pos[0]][start_pos[1]] = buildCode[get_level_from_board(start_pos)]

            elif building_level == worker_level:  # Traversing same level buildings
                board[start_pos[0]][start_pos[1]] = buildCode[int(building_level)]

            elif (building_level - 1) == worker_level:  # Going up a level
                # Updating worker level
                player[level_index] += 1
                update_ref(p_ref, player, ref_index, level_index)

                if building_level > 1:  # If higher than L1 need to replace old building
                    board[start_pos[0]][start_pos[1]] = buildCode[building_level - 1]
                else:  # No building occupied so old space needs to be cleared
                    clear_pos(start_pos)
            else:
                raise BoundsError

        elif get_level_from_board(start_pos) > 0:  # Player descending
            board[start_pos[0]][start_pos[1]] = buildCode[player[level_index]]  # Update the board
            player[level_index] -= 1

            if get_level_from_board(start_pos) > 1:
                player[level_index] = 0

            # Update the worker details and icon
            update_ref(p_ref, player, ref_index, level_index)

        else:
            clear_pos(start_pos)

        workerLoc[workerLoc.index(start_pos)] = new_pos  # Update worker location in location tracker
        board[new_pos[0]][new_pos[1]] = player[ref_index]  # Update player position on the board

        return [new_pos[0], new_pos[1]]


def worker_build(build_pos):
    """
    Given a position either register a new building or increase the height of the present building

    :param build_pos: The position in which the building is being built
    """
    if build_pos in workerLoc:  # Space is taken by a worker
        raise SelectionError
    elif get_level_from_board(build_pos) == 0:  # Space not built on so know it's the first level
        new_level = buildCode[1]

    else:  # Building higher than l1
        if max_height(build_pos):
            raise SelectionError

        new_level = buildCode[get_level_from_board(build_pos) + 1]

    board[build_pos[0]][build_pos[1]] = new_level  # Update the board with new building position


def new_position(direction, pos):
    """
    Calculate a new position on the board using the desired direction and the initial position

    :param direction: The direction to move in (W, A, S, D, WA, WD, SA and SD)
    :param pos: The initial position
    :return: The new position
    """
    new_pos = pos[:]  # Making a copy

    match direction:
        case "W":
            new_pos[0] -= 1
        case "A":
            new_pos[1] -= 1
        case "S":
            new_pos[0] += 1
        case "D":
            new_pos[1] += 1
        case "WA":
            new_pos[0] -= 1
            new_pos[1] -= 1
        case "WD":
            new_pos[0] -= 1
            new_pos[1] += 1
        case "SA":
            new_pos[0] += 1
            new_pos[1] -= 1
        case "SD":
            new_pos[0] += 1
            new_pos[1] += 1
        case _:
            print("Fault 8")
            raise SelectionError()

    return new_pos


def find_level_index(p_ref):
    """
    Given a player reference return the worker tag and level index, as wll as the standardised reference

    :param p_ref: The worker reference
    :return: Standardised worker reference and the level index
    """
    p_ref = std_ref(p_ref)
    p_ref = remove_level(p_ref)

    if p_ref in ["A", "C"]:
        return p_ref, 3
    else:
        return p_ref, 4


def update_ref(p_ref, player, ref_index, level_index):
    """
    Standardise a player reference

    :param p_ref: The worker reference
    :param player: The current player
    :param ref_index: The workers index reference
    :param level_index: The workers level reference
    """
    player[ref_index] = "| {}{} |".format(remove_level(std_ref(p_ref)), player[level_index])  # Update worker reference
    if player[level_index] == 3:
        print("\nWow! Player {}, has won!".format(player[2]))
        exit()


def std_ref(ref):
    """
    Standardise a worker reference

    :param ref: The reference to be standardised
    :return: The single character reference
    """
    return ref.replace("|", "").replace(" ", "").replace("L", "")


def remove_level(ref):
    """
    Return the given reference without numbers

    :param ref: The worker reference
    :return: Worker reference without a number
    """
    return ''.join([i for i in ref if not i.isdigit()])


def clear_pos(start_pos):
    """
    Clear the given position from the board

    :param start_pos: The position which is now blank
    """
    board[start_pos[0]][start_pos[1]] = "|    |"  # Clear icon from old position


def max_height(build_pos):
    """
    Check if a building is already at the max height (Dome, {})

    :param build_pos: The tested buildings position
    :return: True if the building is at the max height, otherwise nothing
    """
    if board[build_pos[0]][build_pos[1]] == "| {} |":
        return True


def out_bounds(pos):
    """
    Check if a given position is within bounds of the board (0,0 to 4,4)

    :param pos: The tested position
    :return: True if within bounds, otherwise nothing
    """
    if any(0 > val for val in pos) or any(val > 4 for val in pos):
        return True


def get_level_from_board(pos):
    """
    Get the level of a given position

    :param pos: Position to retrieve the level of
    :return: The level of the position
    """
    board_value = board[pos[0]][pos[1]]
    if board_value[3].isdigit():
        return int(board_value[3])
    else:
        return 0
