# test_toRobot.py
import os
import pytest
from toyRobot import place_robot, move_robot, read_commands_from_file, rotate_left, rotate_right, report_position, process_command

@pytest.fixture
def initial_state():
    return {}


def test_place_robot():
    state = place_robot(1, 2, "NORTH")
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "NORTH"
    
    result = place_robot(6, 6, "NORTH")
    assert result == "Invalid X or Y value, X and Y must be between 0 and 5"

def test_move_robot():
    state = place_robot(1, 2, "NORTH")
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "NORTH"

    state = move_robot()
    assert state['X'] == 1
    assert state['Y'] == 3
    assert state['dir'] == "NORTH"


    state = place_robot(1, 2, "SOUTH")
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "SOUTH"
    
    state = move_robot()
    assert state['X'] == 1
    assert state['Y'] == 1
    assert state['dir'] == "SOUTH"

    state = place_robot(1, 2, "EAST")
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "EAST"
    
    state = move_robot()
    assert state['X'] == 2
    assert state['Y'] == 2
    assert state['dir'] == "EAST"

    state = place_robot(1, 2, "WEST")
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "WEST"
    
    state = move_robot()
    assert state['X'] == 0
    assert state['Y'] == 2
    assert state['dir'] == "WEST"

def test_rotate_left():
    state = place_robot(1, 2, "NORTH")
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "NORTH"

    state = rotate_left()
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "WEST"

    state = rotate_left()
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "SOUTH"

    state = rotate_left()
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "EAST"

    state = rotate_left()
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "NORTH"

def test_rotate_right():
    state = place_robot(1, 2, "NORTH")
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "NORTH"

    state = rotate_right()
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "EAST"

    state = rotate_right()
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "SOUTH"

    state = rotate_right()
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "WEST"

    state = rotate_right()
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "NORTH"

def test_report_position():
    state = place_robot(1, 2, "NORTH")
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "NORTH"
    
    assert report_position() == "1,2,NORTH"

    move_robot()
    assert report_position() == "1,3,NORTH"

    rotate_right()
    assert report_position() == "1,3,EAST"

    move_robot()
    assert report_position() == "2,3,EAST"

def test_process_command():
    state = process_command("PLACE 1,2,NORTH")
    assert state['X'] == 1
    assert state['Y'] == 2
    assert state['dir'] == "NORTH"

    state = process_command("MOVE")
    assert state['X'] == 1
    assert state['Y'] == 3
    assert state['dir'] == "NORTH"

    state = process_command("LEFT")
    assert state['X'] == 1
    assert state['Y'] == 3
    assert state['dir'] == "WEST"

    result = process_command("REPORT")
    assert result == "1,3,WEST"

    result = process_command("EXIT")
    assert result == False

    result = process_command("INVALID")
    assert result == "Unknown command: INVALID"

def test_invalid_place():
    result = process_command("PLACE 6,6,NORTH")
    assert result == "Invalid X or Y value, X and Y must be between 0 and 5"

def test_boundary_conditions():
    process_command("PLACE 0,0,SOUTH")
    process_command("MOVE")
    assert report_position() == "0,0,SOUTH"

    process_command("PLACE 0,0,WEST")
    process_command("MOVE")
    assert report_position() == "0,0,WEST"

    process_command("PLACE 5,5,NORTH")
    process_command("MOVE")
    assert report_position() == "5,5,NORTH"

    process_command("PLACE 5,5,EAST")
    process_command("MOVE")
    assert report_position() == "5,5,EAST"

def test_sequential_commands():
    process_command("PLACE 0,0,NORTH")
    process_command("MOVE")
    assert report_position() == "0,1,NORTH"

    process_command("MOVE")
    assert report_position() == "0,2,NORTH"

    process_command("LEFT")
    assert report_position() == "0,2,WEST"

    process_command("MOVE")
    assert report_position() == "0,2,WEST"  

    process_command("RIGHT")
    assert report_position() == "0,2,NORTH"

    process_command("RIGHT")
    assert report_position() == "0,2,EAST"

    process_command("MOVE")
    assert report_position() == "1,2,EAST"

def test_process_multiple_commands():
    commands = [
        "PLACE 1,2,NORTH\nMOVE\nLEFT\nREPORT",
        "PLACE 0,0,NORTH\nMOVE\nRIGHT\nMOVE\nREPORT",
        "PLACE 3,4,EAST\nLEFT\nMOVE\nMOVE\nREPORT",
        "PLACE 2,2,SOUTH\nMOVE\nRIGHT\nMOVE\nMOVE\nREPORT"
    ]

    expected_results = [
        "1,3,WEST",
        "1,1,EAST",
        "3,5,NORTH",  
        "0,1,WEST"   
    ]

    for i, command in enumerate(commands):
        inputs = command.split("\n")
        for input_command in inputs:
            result = process_command(input_command)
        assert result == expected_results[i]


if __name__ == "__main__":
    pytest.main()
