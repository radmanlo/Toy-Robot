import re

# Define patterns
PATTERN_PLACE = r"^PLACE (\d+),(\d+),(NORTH|SOUTH|EAST|WEST)$"

# Initial state of the robot
state = None


"""
    Place Robot Function
    Place the robot in a (x, y) possition

    x
    y
    direction => face of robot

    @RETURN state object
    @RETURN str (error)
"""
def place_robot(x, y, direction):

    # State of the robot
    global state

    if 0 <= x <= 5 and 0 <= y <= 5:
        state = {
            'X': x,
            'Y': y,
            'dir': direction
        }
        return state
    else:
        return "Invalid X or Y value, X and Y must be between 0 and 5"


"""
    Move the Robot Function
    Move the robot one unit forward in the direction it is currently facing.

    @RETURN state object
"""
def move_robot():

    # State of the robot
    global state

    if state is None:
        return
    
    x, y = state["X"], state['Y']

    if state['dir'] == "NORTH" and y + 1 <= 5:
        y += 1
    elif state['dir'] == "SOUTH" and y - 1 >= 0:
        y -= 1
    elif state['dir'] == "EAST" and x + 1 <= 5:
        x += 1
    elif state['dir'] == "WEST" and x - 1 >= 0:
        x -= 1
    
    # Update position of the robot
    state['X'] = x
    state['Y'] = y

    return state


"""
    Rotate the Robot to the Left Function
    Rotate the robot 90 degrees in the left direction without
    changing the position of the robot.

    @RETURN state object
"""
def rotate_left():

    # Direction of the robot
    global state

    if state is None:
        return
    
    directions = ["NORTH", "WEST", "SOUTH", "EAST"]
    index = directions.index(state['dir'])

    # Update direction of the robot
    state['dir'] = directions[(index + 1) % 4]

    return state


"""
    Rotate the Robot to the Right Function
    Rotate the robot 90 degrees in the right direction without
    changing the position of the robot.

    @RETURN state object
"""
def rotate_right():

    # Direction of the robot
    global state

    if state is None:
        return
    
    directions = ["NORTH", "EAST", "SOUTH", "WEST"]
    index = directions.index(state['dir'])

    # Update direction of the robot
    state['dir'] = directions[(index + 1) % 4]

    return state


"""
    Report the State of the Robot Function
    Announce the X,Y and F of the robot.

    @RETURN str (current state)
"""
def report_position():
    if state is None:
        return
    return f"{state['X']},{state['Y']},{state['dir']}"


"""
    Process the Command Function
    Process the command from user and call the approprite module

    @RETURN state object
    @RETURN FALSE
    @RETURN str (error)
"""
def process_command(command):
    match = re.match(PATTERN_PLACE, command)
    if match:
        x = int(match.group(1))
        y = int(match.group(2))
        direction = match.group(3)
        return place_robot(x, y, direction)
    elif command == "MOVE":
        return move_robot()
    elif command == "LEFT":
        return rotate_left()
    elif command == "RIGHT":
        return rotate_right()
    elif command == "REPORT":
        return report_position()
    elif command == "EXIT":
        return False
    else:
        return f"Unknown command: {command}"


"""
    Read Commands from file function
    Open and read the file from the path which is specified.

    file_path => path of file

    @RETURN array of commands in the file
"""
def read_commands_from_file(file_path):
    with open(file_path, 'r') as file:
        commands = [line.strip() for line in file.readlines()]
    return commands

def main():
    
    # Ask the user how they want to provide input
    input_method = input("Do you want to provide input from a file or manually? (file/manual): ").strip().lower()
    
    # Get commands from a file
    if input_method == 'file':

        file_path = input("Enter the path to the input file: ").strip()

        try:
            commands = read_commands_from_file(file_path)
            
            for command in commands:
                result = process_command(command)
                if result == False:
                    break
                if isinstance(result, str):
                    print(result)

        except Exception as e:
            print(f"Error reading file: {e}")
    # Get commands from the user directly
    elif input_method == 'manual':

        print("Enter commands (type 'EXIT' to end):")

        while True:
            try:
                user_input = input().strip()
                result = process_command(user_input)

                if result == False:
                    print("Thank You! See you soon :)")
                    break
                if isinstance(result, str):
                    print("\n",result)

            except EOFError:
                break
    else:
        print("Invalid input method. Please enter 'file' or 'manual'.")

if __name__ == "__main__":
    main()
