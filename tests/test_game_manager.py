import pytest

from lib.game_manager import GameManager


def test_check_win_horizontal():
    """This tests if the grid has 4 in a horizontal direction"""
    grid = [[0,0,0,0,0],
            [0,1,1,1,1],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
            ]
    game_manager = GameManager()
    assert game_manager.check_win(grid) == 1

    grid = [[0,0,0,0,0],
            [1,1,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
            ]
    game_manager = GameManager()
    assert game_manager.check_win(grid) == 1

    grid = [[0,0,0,0,0],
            [1,0,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
            ]
    game_manager = GameManager()
    assert game_manager.check_win(grid) == 0

    grid = [[0,0,0,0,0],
            [1,0,1,1,0],
            [0,2,0,0,0],
            [0,1,0,1,1],
            [1,2,2,2,0]
            ]
    game_manager = GameManager()
    assert game_manager.check_win(grid) == 0

    grid = [[0,0,0,0,0],
            [1,0,1,1,0],
            [0,2,0,0,0],
            [0,1,0,1,1],
            [2,2,2,2,0]
            ]
    game_manager = GameManager()
    assert game_manager.check_win(grid) == 2

def test_check_win_vertical():
    """This tests if the grid has 4 in a vertical direction"""
    grid = [[0,0,0,0,0],
            [0,1,1,0,1],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
            ]
    game_manager = GameManager()
    assert game_manager.check_win(grid) == 0

    grid = [[0,0,0,0,0],
            [0,1,1,0,1],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0]
            ]
    game_manager = GameManager()
    assert game_manager.check_win(grid) == 1

    grid = [[0,0,1,0,0],
            [0,1,1,0,1],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0]
            ]
    game_manager = GameManager()
    assert game_manager.check_win(grid) == 1

    grid = [[0, 0, 1, 0, 0],
            [0, 1, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
            ]
    game_manager = GameManager()
    assert game_manager.check_win(grid) == 0

def test_check_win_diagonal():
    """This tests if the grid has 4 in a diagonal direction"""
    grid = [[0,0,0,0,0],
            [0,1,0,0,0],
            [0,0,1,0,0],
            [0,0,0,1,0],
            [0,0,0,0,1]
            ]
    game_manager = GameManager()
    assert game_manager.check_win(grid) == 1

    grid = [[0,0,0,0,0],
            [0,1,0,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,1]
            ]
    game_manager = GameManager()
    assert game_manager.check_win(grid) == 0

    grid = [[0,0,0,0,0],
            [0,0,0,1,0],
            [0,0,1,0,0],
            [0,1,0,0,0],
            [1,0,0,0,1]
            ]
    game_manager = GameManager()
    assert game_manager.check_win(grid) == 1