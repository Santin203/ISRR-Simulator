# Final Project
# By Santiago Jimenez
# Date: 12/11/2023

"""
Program to simulate the scheduling of instructions into a multi-issue processor. 

The program takes input in the form of instructions, where each instruction is a 
string of the form:

    <destination register>,<source register 1>,<source register 2>,<operation>.
    
    
The program then schedules these instructions into a multi-issue processor.

The program will output the scheduling of the instructions.

The scheduler should check for RAW, WAR and WAW dependencies, and delay instructions
as appropriate.

Instruction latencies:
    o	+, -:  1 cycle
    o	*: 2 cycles
    o	Load, Store: 3 cycles
    
Processor capabilities:
    a.	Single instruction, in-order execution
    b.	Superscalar, in-order execution
    c.	Superscalar, out-of-order issue, in-order retirement
    d.	Superscalar, out-of-order issue and retirement

Input format:
    r3,r0,r1,*
    r4,r0,r2,+
    r5,r0,r1,+
    ...
    
Output format: Is a table with the following columns:
    o	Cycle: The cycle number
    o	Instructions Issued: The instructions issued in that cycle
    o	Retired: The instructions retired in that cycle
    
"""
import pandas as pd

# Registers array (register number, read count, write count)
registers = [[0,0,0],[1,0,0],[2,0,0],[3,0,0],[4,0,0],[5,0,0],[6,0,0],[7,0,0],[8,0,0],[9,0,0],[10,0,0],[11,0,0],[12,0,0],[13,0,0]]

# Function to update the registers
def update_registers(instruction, operation):
    
    #Get the destination register
    destination_register = int(instruction[0][1:])
    
    # Get the source registers
    source_register_1 = int(instruction[1][1:])
    source_register_2 = int(instruction[2][1:])
    
    # Update the registers
    if operation == 0:#allocating
        registers[source_register_1][1] += 1
        registers[source_register_2][1] += 1
        registers[destination_register][2] += 1
    elif operation == 1:#freeing
        registers[source_register_1][1] -= 1
        registers[source_register_2][1] -= 1
        registers[destination_register][2] -= 1
    else:
        print("Invalid operation")
    
# Function to get the number of registers in use
def register_in_use():
    in_use = 0
    
    for i in range(len(registers)):
        
        # If the register is in use, add 1 to the counter
        if registers[i][1] > 0 or registers[i][2] > 0:
            in_use += 1
            
    return in_use

# Function to read the input file and return an array of lists of instructions
def read_instructions_from_file(filename):
    
    # Initialize the instructions array
    instructions = []
    
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                
                # Split each line by comma and remove leading/trailing whitespace
                parts = line.strip().split(',')
                
                # Check if the instruction is valid
                if len(parts) == 4:
                    
                    # Add the instruction to the instructions array
                    instructions.append(parts)
                    
                    # add number of cycles to complete instruction
                    if parts[3] == '*':
                        instructions[-1].append(2)
                    elif parts[3] == '+' or parts[3] == '-':
                        instructions[-1].append(1)
                    elif parts[3] == 'Load' or parts[3] == 'Store':
                        instructions[-1].append(3)
                    else:
                        print(f"Ignoring invalid instruction: {line}")
                        
                else:
                    print(f"Ignoring invalid instruction: {line}")
                
                # Add the retired flag to the instruction
                instructions[-1].append(0)
                
    # Handle file not found error
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        
    # Return the instructions array
    return instructions

# Function to print the instructions in a readable format using pandas
def print_instructions(instructions):
    df = pd.DataFrame(instructions, columns=['Destination', 'Source 1', 'Source 2', 'Operation', 'Cycles', 'Retired'])
    print(df)
    
# Function to check if the next instruction has a dependency with registers in use
def check_dependency(instruction):
    
    #Get the destination register
    destination_register = int(instruction[0][1:])
    
    # Get the source registers
    source_register_1 = int(instruction[1][1:])
    source_register_2 = int(instruction[2][1:])
    
    # Check if there is a dependency
    if registers[source_register_1][2] > 0 or registers[source_register_2][2] > 0 or registers[destination_register][2] > 0 or registers[destination_register][1] > 0:
        return True
    else:
        return False
    
# Check if there is a dependency between two instructions
def check_dependency2(instruction1, instruction2):
    
    #Get the destination register
    destination_register1 = int(instruction1[0][1:])
    
    # Get the source registers
    source_register1_1 = int(instruction1[1][1:])
    source_register1_2 = int(instruction1[2][1:])
    
    #Get the destination register
    destination_register2 = int(instruction2[0][1:])

    # Get the source registers
    source_register2_1 = int(instruction2[1][1:])
    source_register2_2 = int(instruction2[2][1:])

    # Check if there is a dependency
    if destination_register1 == source_register2_1 or destination_register1 == source_register2_2 or destination_register1 == destination_register2 or destination_register2 == source_register1_1 or destination_register2 == source_register1_2:
        return True
    else:
        return False
   
# Function for scheduling instructions with single instruction/superscalar, in-order execution
def in_order_execution(instructions, num_units):
    
    # Initialize variables
    cycle = 0
    num_instructions = len(instructions)
    reg_in_use = 0
    done = False
    
    # Save scheduled instructions in a pandas dataframe
    df = pd.DataFrame(columns=['Cycle', 'Instructions Issued','Retired'])
    df['Cycle'] = df['Cycle'].astype(int)
    df['Instructions Issued'] = df['Instructions Issued'].astype(str)
    df['Retired'] = df['Retired'].astype(str)
    
    # Initialize the instructions issued and retired columns
    df.at[0, 'Instructions Issued'] = ''
    df.at[0, 'Retired'] = ''
    
    # Initialize the instructions issued and retired lists
    instructions_issued = [[0,0,0,0,0,1]]
    instructions_retired = []
    
    # Initialize the instructions issued and retired strings
    instructions_issued_str = ''
    instructions_retired_str = ''
    
    # Start scheduling
    while not done:
        
        # Reset the instructions issued and retired strings
        instructions_retired_str = ''
        instructions_issued_str = ''
        
        # Issue up to num_units instructions per cycle
        for i in range(num_units):
            
            # check if there is a dependency with the next instruction
            bool_dependency = False
            
            if len(instructions_issued) > 0:
                try:
                    bool_dependency = check_dependency(instructions[len(instructions_issued)-1])
                except IndexError:
                    bool_dependency = True
                
            # if there is no dependency, issue the instruction
            if not bool_dependency:
                
                # Add the instruction to the instructions issued list
                instructions_issued.append(instructions[len(instructions_issued)-1])
                
                # Update the instructions issued string
                last_instruction = len(instructions_issued) - 1
                
                # Handle load and store instructions for visual purposes
                if instructions_issued[last_instruction][3] == 'Load':
                    
                    instructions_issued_str += f"{last_instruction}. {instructions_issued[last_instruction][2]} = {instructions_issued[last_instruction][3]} "
                
                elif instructions_issued[last_instruction][3] == 'Store':
                    
                    instructions_issued_str += f"{last_instruction}. {instructions_issued[last_instruction][3]} = {instructions_issued[last_instruction][0]} "
                
                else:
                    
                    instructions_issued_str += f"{last_instruction}. {instructions_issued[last_instruction][0]} = {instructions_issued[last_instruction][1]} {instructions_issued[last_instruction][3]} {instructions_issued[last_instruction][2]} "
                
                # Update registers
                update_registers(instructions_issued[last_instruction],0)
                
        # Check if a instruction can be retired
        for j in range(len(instructions_issued)):
            
            if (instructions_issued[j][4] < 1 and instructions_issued[j][5] == 0 and instructions_issued[j-1][5] == 1 and instructions_issued[j][0] != 0):
                
                # Update variables, arrays and strings
                last_instruction = len(instructions_issued) - 1
                instructions_retired_str += f"{j}. "
                instructions_issued[j][5] = 1
                instructions_retired.append(instructions_issued[j])
                
                # Update registers
                update_registers(instructions_issued[j],1)
                  
        # Update the number of cycles to complete the instruction
        for i in range(len(instructions_issued)):
            
            # If the instruction is not completed, subtract 1 from the number of cycles to complete it
            if instructions_issued[i][4] > 0:
                instructions_issued[i][4] -= 1
            
        # Update the cycle counter
        cycle += 1
        
        # Update the dataframe
        df.at[cycle, 'Cycle'] = cycle
        df.at[cycle, 'Instructions Issued'] = instructions_issued_str
        df.at[cycle, 'Retired'] = instructions_retired_str
        
        # Check if there are instructions running
        reg_in_use = register_in_use()
            
        # If there are no instructions running, and all instructions have been retired, then we are done
        if reg_in_use == 0 and len(instructions_retired) == num_instructions:
            done = True
        
    # Return the dataframe    
    return df
 
# Function for scheduling instructions with superscalar, out-of-order issue, in-order retirement
def out_of_order_issue_in_order_retirement(instructions, num_units):
    
    # Initialize variables
    cycle = 0
    num_instructions = len(instructions)
    reg_in_use = 0
    done = False
    
    # Save scheduled instructions in a pandas dataframe
    df = pd.DataFrame(columns=['Cycle', 'Instructions Issued','Retired'])
    df['Cycle'] = df['Cycle'].astype(int)
    df['Instructions Issued'] = df['Instructions Issued'].astype(str)
    df['Retired'] = df['Retired'].astype(str)
    
    # Initialize the instructions issued and retired columns
    df.at[0, 'Instructions Issued'] = ''
    df.at[0, 'Retired'] = ''
    
    # Initialize the instructions issued and retired lists
    instructions_issued = [[0,0,0,0,0,1,0]]
    instructions_retired = []
    
    # Initialize the instructions issued and retired strings
    instructions_issued_str = ''
    instructions_retired_str = ''
    
    # Start scheduling
    while not done:
        
        # Reset the instructions issued and retired strings
        instructions_retired_str = ''
        instructions_issued_str = ''
        
        # Issue up to num_units instructions per cycle
        for i in range(num_units):

            # Allow instructions to be issued out of order
            for k in range(num_instructions):
                
                # check if there is are dependencies
                bool_dependency1 = False
                bool_dependency2 = False
                
                # check if there is a dependency with the next instruction (check that the required registers are not in use)
                if len(instructions_issued) > 1 and instructions[k][4] > 0:
                    try:
                        bool_dependency1 = check_dependency(instructions[k])
                    except IndexError:
                        bool_dependency1 = True

                # Make sure to not violate RAW dependencies so that the program is correct
                if len(instructions_issued) > 1 and instructions[k][4] > 0:
                    try:
                        
                        #  Check current instruction with all past instructions (issued or not issued) to see if there is a dependency
                        for l in range(k-1, -1, -1):
                            if instructions[l][5] == 1:
                                bool_dependency2 = False
                                break
                            else:
                                bool_dependency2 = check_dependency2(instructions[l], instructions[k])
                            if bool_dependency2:
                                break

                    except IndexError:
                        bool_dependency2 = True
                    
                # if there is no dependency, issue the instruction
                if not bool_dependency1 and not bool_dependency2 and instructions[k][4] > 0:
                    
                    # Add the instruction to the instructions issued list
                    instructions_issued.append(instructions[k])

                    # Add the number of the instruction at the end of the list
                    instructions_issued[-1].append(k+1)
                    
                    # Update the instructions issued string
                    last_instruction = len(instructions_issued) - 1

                    # Handle load and store instructions for visual purposes
                    if instructions_issued[last_instruction][3] == 'Load':
                        
                        instructions_issued_str += f"{k+1}. {instructions_issued[last_instruction][2]} = {instructions_issued[last_instruction][3]} "
                    
                    elif instructions_issued[last_instruction][3] == 'Store':
                        
                        instructions_issued_str += f"{k+1}. {instructions_issued[last_instruction][3]} = {instructions_issued[last_instruction][0]} "
                    
                    else:
                        
                        instructions_issued_str += f"{k+1}. {instructions_issued[last_instruction][0]} = {instructions_issued[last_instruction][1]} {instructions_issued[last_instruction][3]} {instructions_issued[last_instruction][2]} "
                        
                    # Update registers
                    update_registers(instructions_issued[last_instruction],0)
                    
                    break

        # Temporal list with instructions issued in order        
        instructions_issued_temp = instructions_issued.copy()
        instructions_issued_temp.sort(key=lambda x: x[6])

        # Check if a instruction can be retired, only allow in order retirement
        # Use the temporal list to check for in order retirement
        for j in range(len(instructions_issued_temp)):
            
            # Check if the instruction can be retired
            if (instructions_issued_temp[j][4] < 1 and instructions_issued_temp[j][5] == 0 and instructions_issued_temp[j][0] != 0 and instructions_issued_temp[j-1][6] == instructions_issued_temp[j][6] - 1 and instructions_issued_temp[j-1][5] == 1):
                
                # Update variables, arrays and strings
                last_instruction = len(instructions_issued) - 1
                instructions_retired_str += f"{instructions_issued_temp[j][6]}. "
                instructions_issued_temp[j][5] = 1
                instructions_retired.append(instructions_issued_temp[j])
                
                # Update registers
                update_registers(instructions_issued_temp[j],1)
        
        # Update the number of cycles to complete the instruction
        for i in range(len(instructions_issued)):
            if instructions_issued[i][4] > 0:
                instructions_issued[i][4] -= 1
            
        # Update the cycle counter
        cycle += 1
        
        # Update the dataframe
        df.at[cycle, 'Cycle'] = cycle
        df.at[cycle, 'Instructions Issued'] = instructions_issued_str
        df.at[cycle, 'Retired'] = instructions_retired_str
        
        # Check if there are instructions running
        reg_in_use = register_in_use()
        
        # If there are no instructions running, and all instructions have been retired, then we are done
        if reg_in_use == 0 and len(instructions_retired) == num_instructions:
            done = True
        
    # Return the dataframe    
    return df

# Function for scheduling instructions with superscalar, out-of-order issue and retirement
def out_of_order_issue_and_retirement(instructions, num_units):
    
    # Initialize variables
    cycle = 0
    num_instructions = len(instructions)
    reg_in_use = 0
    done = False
    
    # Save scheduled instructions in a pandas dataframe
    df = pd.DataFrame(columns=['Cycle', 'Instructions Issued','Retired'])
    df['Cycle'] = df['Cycle'].astype(int)
    df['Instructions Issued'] = df['Instructions Issued'].astype(str)
    df['Retired'] = df['Retired'].astype(str)
    
    # Initialize the instructions issued and retired columns
    df.at[0, 'Instructions Issued'] = ''
    df.at[0, 'Retired'] = ''
    
    # Initialize the instructions issued and retired lists
    instructions_issued = [[0,0,0,0,0,1,0]]
    instructions_retired = []
    
    # Initialize the instructions issued and retired strings
    instructions_issued_str = ''
    instructions_retired_str = ''
    
    # Start scheduling
    while not done:
        
        # Reset the instructions issued and retired strings
        instructions_retired_str = ''
        instructions_issued_str = ''
        
        # Issue up to num_units instructions per cycle
        for i in range(num_units):

            # Allow instructions to be issued out of order
            for k in range(num_instructions):
                
                # check if there is are dependencies
                bool_dependency1 = False
                bool_dependency2 = False
                
                # check if there is a dependency with the next instruction (check that the required registers are not in use)
                if len(instructions_issued) > 1 and instructions[k][4] > 0:
                    try:
                        bool_dependency1 = check_dependency(instructions[k])
                    except IndexError:
                        bool_dependency1 = True

                # Make sure to not violate RAW dependencies so that the program is correct
                if len(instructions_issued) > 1 and instructions[k][4] > 0:
                    try:
                        
                        # Check current instruction with all past instructions (issued or not issued) to see if there is a dependency
                        for l in range(k-1, -1, -1):
                            if instructions[l][5] == 1:
                                bool_dependency2 = False
                                break
                            else:
                                bool_dependency2 = check_dependency2(instructions[l], instructions[k])
                            if bool_dependency2:
                                break

                    except IndexError:
                        bool_dependency2 = True
                    
                # if there is no dependency, issue the instruction
                if not bool_dependency1 and not bool_dependency2 and instructions[k][4] > 0:
                    
                    # Add the instruction to the instructions issued list
                    instructions_issued.append(instructions[k])

                    # Add the number of the instruction at the end of the list
                    instructions_issued[-1].append(k+1)
                    
                    # Update the instructions issued string
                    last_instruction = len(instructions_issued) - 1
                    
                    # Handle load and store instructions for visual purposes
                    if instructions_issued[last_instruction][3] == 'Load':
                        
                        instructions_issued_str += f"{k+1}. {instructions_issued[last_instruction][2]} = {instructions_issued[last_instruction][3]} "
                    
                    elif instructions_issued[last_instruction][3] == 'Store':
                        
                        instructions_issued_str += f"{k+1}. {instructions_issued[last_instruction][3]} = {instructions_issued[last_instruction][0]} "
                    
                    else:
                        
                        instructions_issued_str += f"{k+1}. {instructions_issued[last_instruction][0]} = {instructions_issued[last_instruction][1]} {instructions_issued[last_instruction][3]} {instructions_issued[last_instruction][2]} "
                             
                    # Update registers
                    update_registers(instructions_issued[last_instruction],0)
                    
                    break
                
        # Check if a instruction can be retired
        for j in range(len(instructions_issued)):
            
            if (instructions_issued[j][4] < 1 and instructions_issued[j][5] == 0 and instructions_issued[j][0] != 0):
                
                # Update variables, arrays and strings
                last_instruction = len(instructions_issued) - 1
                instructions_retired_str += f"{instructions_issued[j][6]}. "
                instructions_issued[j][5] = 1
                instructions_retired.append(instructions_issued[j])
                
                # Update registers
                update_registers(instructions_issued[j],1)
            

            
        # Update the number of cycles to complete the instruction
        for i in range(len(instructions_issued)):
            if instructions_issued[i][4] > 0:
                instructions_issued[i][4] -= 1
            
        # Update the cycle counter
        cycle += 1
        
        # Update the dataframe
        df.at[cycle, 'Cycle'] = cycle
        df.at[cycle, 'Instructions Issued'] = instructions_issued_str
        df.at[cycle, 'Retired'] = instructions_retired_str
        
        # Check if there are instructions running
        reg_in_use = register_in_use()
            
        # If there are no instructions running, and all instructions have been retired, then we are done
        if reg_in_use == 0 and len(instructions_retired) == num_instructions:
            done = True
        
    # Return the dataframe    
    return df            

#############################################################################################################################       
        
# Start of program
print("Multi-Issue Processor Simulator\n")

print("Select input file: \n")
print("1. input_1")
print("2. input_2")
print("3. input_1 (with_register renaming)")
print("4. input_2 (with_register renaming)")
print("\n")

# Ask for input file
input_file = 0

while input_file <= 0 or input_file > 4:
    try:
        input_file = int(input("Enter input file: "))
    except ValueError:
        print("Invalid input. Please enter a positive integer.")

# Initialize the instructions array
instructions = []

# Switch to select input file
match input_file:
    
    # Read the instructions from the input file 1
    case 1:
        print("input_1")
        instructions = read_instructions_from_file('input_1.txt')
    
    # Read the instructions from the input file 2
    case 2:
        print("input_2")
        instructions = read_instructions_from_file('input_2.txt')
    
    # Read the instructions from the input file 3
    case 3:
        print("input_1 (with_register renaming)")
        instructions = read_instructions_from_file('input_3.txt')
    
    # Read the instructions from the input file 4    
    case 4:
        print("input_2 (with_register renaming)")
        instructions = read_instructions_from_file('input_4.txt')
        
    case _:
        print("Invalid input. Please enter a positive integer.")
        
# Print the instructions
if len(instructions) > 0:
    print_instructions(instructions)
        
# Ask for processor setting
print("\nSelect processor setting: \n")
print("1. Single instruction, in-order execution")
print("2. Superscalar, in-order execution")
print("3. Superscalar, out-of-order issue, in-order retirement")
print("4. Superscalar, out-of-order issue and retirement")
print("\n")

processor_setting = 0

while processor_setting <= 0 or processor_setting > 4:
    try:
        processor_setting = int(input("Enter processor setting: \n"))
    except ValueError:
        print("Invalid input. Please enter a positive integer.")

# Switch to select processor setting
match processor_setting:
    
    # Call function for single instruction, in-order execution
    case 1:
        
        print("Single instruction, in-order execution\n")
        
        # Call function
        df=in_order_execution(instructions, 1)
        
        # Print results
        print(df)
    
    # Call function for superscalar, in-order execution        
    case 2:
        
        print("Superscalar, in-order execution\n")
        
        # Ask for number of parallel functional units
        num_units = 0
        
        while num_units <= 0:
            try:
                num_units = int(input("Enter the number of parallel functional units: "))
            except ValueError:
                print("Invalid input. Please enter a positive integer.")

        print("\n")
        
        # Call function
        df=in_order_execution(instructions, num_units)
        
        # Print results
        print(df)
        
    # Call function for superscalar, out-of-order issue, in-order retirement
    case 3:
        
        print("Superscalar, out-of-order issue, in-order retirement")
        
        # Ask for number of parallel functional units
        num_units = 0
        
        while num_units <= 0:
            try:
                num_units = int(input("Enter the number of parallel functional units: "))
            except ValueError:
                print("Invalid input. Please enter a positive integer.")

        print("\n")
        
        # Call function
        df = out_of_order_issue_in_order_retirement(instructions, num_units)
        
        # Print results
        print(df)
        
    # Call function for superscalar, out-of-order issue and retirement
    case 4:
        
        print("Superscalar, out-of-order issue and retirement")
        
        # Ask for number of parallel functional units
        num_units = 0
        
        while num_units <= 0:
            try:
                num_units = int(input("Enter the number of parallel functional units: "))
            except ValueError:
                print("Invalid input. Please enter a positive integer.")

        print("\n")
        
        # Call function
        df = out_of_order_issue_and_retirement(instructions, num_units)
        
        # Print results
        print(df)
        
    case _:
        
        print("Invalid input. Please enter a positive integer.")