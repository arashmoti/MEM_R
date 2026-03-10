""" 
The purpose of this code is to convert a regular gcode that includes tool change commands (Such as T02 and M06)
into a grbl friendly gcode that uses our communication protocol for tool changes.

Instructions: Put the gcode to be converted into a file named "input.txt" and place it in the same file
as this python program. Then run this python program. This should result in the creation of the "output.txt" which
you can feed into the grbl using any gcode sender program.
"""

# Open the input file in read mode and the output file in write mode.
input_file = open("input.txt", "r") 
output_file = open("output.txt", "w")

# Read all lines from the input file into a list.
input_list = input_file.readlines()

# Initialize an empty list to store the modified gcode lines.
output_list = []

# Initialize flags and variables for tool change processing.
M6_flag = False
Tool_number = 1
prev_tool_number = 0
edited_line = ""
pure_command = ""

# Iterate through each line in the input gcode.
for line in input_list:
    # Remove any trailing comments from the line.
    non_comment = line.split(";")[0]
    # Split the line into individual commands based on spaces.
    commands = non_comment.split(" ")
    for command in commands:
        # Remove the newline character from the command if present.
        pure_command = command.replace("\n", "")
        # Check for tool change commands (TXX) and set the new tool number.
        if pure_command.startswith("T") and (47 < ord(pure_command[1]) < 58):
            prev_tool_number = Tool_number
            Tool_number = int(pure_command[1:])
        # Check for tool change command (M06 or M6).
        elif pure_command.startswith("M06") or pure_command.startswith("M6"):
            M6_flag = True
        # Check for program end commands (M02 or M30) and modify the line accordingly.
        elif pure_command.startswith("M02") or pure_command.startswith("M30"):
            edited_line += "M08\nG4 P0.15\nM9\nG4 P" + str(round(((7-Tool_number) % 6)*3, 2)) + "\n" + pure_command + " "
        else:
            edited_line += pure_command + " "

    # Process the tool change commands (M06) and add modified gcode lines to the output list.
    if M6_flag:
        if 7 > Tool_number > 0:
            output_list.append("M08\n")
            output_list.append("G4 P" + str(round(Tool_number*0.1+0.050, 2)) + "\n")
            output_list.append("M09\n")
            output_list.append("G4 P" + str(round(((Tool_number - prev_tool_number + 6) % 6) * 3, 2)) + "\n")
        else:
            print("There are only 6 tools")
            exit()
        M6_flag = False

    # Add the modified gcode line (with tool changes) to the output list.
    output_list.append(edited_line[:-1] + "\n")
    # Reset the temporary edited_line variable for the next iteration.
    edited_line = ""

# Write the modified gcode lines to the output file.
output_file.writelines(output_list)

# Close the input and output files.
output_file.close()
input_file.close()
