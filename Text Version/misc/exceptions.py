"""
Contains custom exceptions for clarity within the code
"""


class SpaceTakenError(Exception):
    """Player selecting an occupied space"""
    pass


class BoundsError(Exception):
    """Player attempting to go out of board limit"""
    pass


class SelectionError(Exception):
    """Player inputted invalid coordinates"""
    pass


class BuildLimitError(Exception):
    """Player hit build limit"""
    pass
