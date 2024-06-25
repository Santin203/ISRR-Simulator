# Multi-Issue Processor Instruction Scheduling and Register Renaming Simulation

## Project Description

The project consists of two main parts:

1. **Instruction Scheduling Simulation**: Develop a Python program to simulate instruction scheduling in a multi-issue processor. The program takes an assembly input with specified formats and accounts for instruction latencies and processor capabilities. The simulation includes dependency checking and evaluates the program's performance under various scenarios, including single instruction, in-order execution, and superscalar execution (both in-order and out-of-order issue and retirement).

2. **Register Renaming Simulation**: Manually adjust the assembly programs from Part 1 to simulate register renaming. The impact of register renaming on performance is evaluated by rerunning the examples in the same configurations as in Part 1.

## Simple Example

### Configuration
- **Instruction latencies**:
  - `+`, `-`: 1 cycle
  - `*`: 2 cycles
  - `Load`, `Store`: 3 cycles
- **Number of functional units**: 1
- **Execution order**: In-order

### Instructions
1. `R3 = R0 * R1`
2. `R4 = R0 + R2`
3. `R5 = R0 + R1`
4. `R6 = R1 + R4`
5. `R7 = R1 * R2`
6. `R1 = R0 - R2`
7. `R3 = R3 * R1`
8. `R1 = R4 + R4`

### Expected Result
| Cycle | Instructions Issued         | Retired Instructions |
|-------|------------------------------|----------------------|
| 1     | 1. R3 = R0 * R1              |                      |
| 2     | 2. R4 = R0 + R2              |                      |
| 3     | 3. R5 = R0 + R1              | 1, 2                |
| 4     | 4. R6 = R1 + R4              | 3                    |
| 5     | 5. R7 = R1 * R2              | 4                    |
| 6     |                              |                      |
| 7     |                              | 5                    |
| 8     | 6. R1 = R0 - R2              |                      |
| 9     |                              | 6                    |
| 10    | 7. R3 = R3 * R1              |                      |
| 11    |                              |                      |
| 12    |                              | 7                    |
| 13    | 8. R1 = R4 + R4              |                      |
| 14    |                              | 8                    |

## Design Description

The program simulates instruction scheduling in a multi-issue processor. Users input a sequence of assembly instructions along with parameters such as the number of parallel functional units and processor capabilities. The simulation includes different processor settings and checks for dependencies among instructions. The primary functions used in the program include:

### Functions for Register Update
- **`update_registers`**: Updates register usage based on the current instruction and operation.
- **`register_in_use`**: Counts the number of registers being used for reading or writing.

### Input Reading Functions
- **`read_instructions_from_file`**: Reads instructions from a file.
- **`print_instructions`**: Prints instructions in a readable format using pandas.

### Dependency Checking Functions
- **`check_dependency`**: Checks if the next instruction has a dependency with registers in use.
- **`check_dependency2`**: Checks for dependencies between two instructions.

### Scheduling Functions
- **`in_order_execution`**: Simulates scheduling for single instruction, in-order execution.
- **`out_of_order_issue_in_order_retirement`**: Simulates scheduling for superscalar, out-of-order issue, in-order retirement.
- **`out_of_order_issue_and_retirement`**: Simulates scheduling for superscalar, out-of-order issue, and retirement.

### General Aspects
- **Input Handling**: Prompts user to select an input file and processor setting.
- **Instruction Representation**: Instructions are represented as strings and stored in a list of lists.
- **Processor Capabilities**: Supports different processor settings, including single instruction and superscalar executions.
- **Instruction Scheduling**: Produces a schedule for each cycle, checks dependencies, and allows parallel issuance of instructions.
- **Results Presentation**: Uses pandas DataFrames to display scheduling results.
- **User Interaction**: Involves the user in selecting input files and processor settings.

## Part 1

### Test Cases Table

#### Input 1

### Instructions
1. `R3 = R0 * R1`
2. `R4 = R0 + R2`
3. `R5 = R0 + R1`
4. `R6 = R1 + R4`
5. `R7 = R1 * R2`
6. `R1 = R0 - R2`
7. `R3 = R3 * R1`
8. `R1 = R4 + R4`

| Configuration                              | Results                          |
|---------------------------------------------|----------------------------------|
| 1 issue slot, in-order                      | ![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/68e29d7e-ed87-4588-9161-d9426be6efa2) |
| 1 issue slot, out-of-order issue, in-order retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/eaf0313e-845b-431c-8a6c-4c3f6df1b289) |
| 1 issue slot, out-of-order issue and retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/f4eef9c3-7c11-4cd1-9e3e-975f42f5ffd4) |
| 2 issue slots, in-order                     |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/555dfb9b-91f0-4b12-af7b-2bfc6ee6674e) |
| 2 issue slots, out-of-order issue, in-order retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/1fd76c85-bf4a-4016-94ff-b7d3d77f5374) |
| 2 issue slots, out-of-order issue and retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/62d1f099-19dd-4b78-a26b-937ac6ff95d4) |
| 3 issue slots, in-order                     |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/a54202ac-b227-4921-b3ff-07a40c7e93ab) |
| 3 issue slots, out-of-order issue, in-order retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/bb3458a5-71df-4154-9cda-ab193afd53a0) |
| 3 issue slots, out-of-order issue and retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/76ca7351-c888-47b1-a1af-90c2189ab7bf) |

#### Input 2

### Instructions
1. `R3 = R0 * R1`
2. `R4 = R0 + R2`
3. `R5 = R0 + R1`
4. `R6 = R1 + R4`
5. `R7 = R1 * R2`
6. `R1 = R0 - R2`
7. `R3 = R3 * R1`
8. `R1 = R4 + R4`
9. `R3 = R0 * R1`
10. `R4 = R0 + R2`
11. `R5 = R0 + R1`
12. `R6 = R1 + R4`
13. `R7 = R1 * R2`
14. `R1 = R0 - R2`
15. `R3 = R3 * R1`
16. `R1 = R4 + R4`
17. `R3 = R0 * R1`
18. `R4 = R0 + R2`
19. `R5 = R0 + R1`
20. `R6 = R1 + R4`
21. `R7 = R1 * R2`
22. `R1 = R0 - R2`
23. `R3 = R3 * R1`
24. `R1 = R4 + R4`
25. `R3 = R0 * R1`
26. `R4 = R0 + R2`
27. `R11 = Load`
28. `R8 = R0 + R1`
29. `R6 = R1 + R4`
30. `Store = R13`

| Configuration                              | Results                          |
|---------------------------------------------|----------------------------------|
| 1 issue slot, in-order                      |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/f2a8543f-fea5-4621-9b91-bcf1630cbf84) ![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/01b72b51-5c9d-4a9c-9714-029c3ede17f0) |
| 1 issue slot, out-of-order issue, in-order retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/2989c896-493a-47ca-9679-238dd93361e1) ![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/59993926-e730-4f3d-86e4-209aa176d13d) |
| 1 issue slot, out-of-order issue and retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/5fc0d62a-b35d-4b33-88d3-3675266ddc3d) ![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/4b9a845e-4b71-447c-bbc9-f9b0cddfe680) |
| 2 issue slots, in-order                     |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/9226becb-fe6f-4ff6-b432-1f45c4add57c) ![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/b96ca331-4097-4ef8-9a19-225d2081008b) |
| 2 issue slots, out-of-order issue, in-order retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/01e57229-bf76-4419-b889-54b258ffdad2) ![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/a21bfdaa-d611-47ee-a76a-e3ec39960b1f) |
| 2 issue slots, out-of-order issue and retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/78dcb482-4d7f-4c3f-ae82-1f3ca151fbac) ![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/c1a1ec85-c3e6-4d91-8ae4-ecb67518d549) |
| 3 issue slots, in-order                     |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/bac79e35-4ab1-4132-a0c9-4050423fd764) ![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/fce89e22-9ff6-47dc-b680-7a4b4bb4e462) |
| 3 issue slots, out-of-order issue, in-order retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/3986ff32-c08a-40bb-881b-c018f0001074) ![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/274a9278-6b20-4092-8037-ed8282185fc9)|
| 3 issue slots, out-of-order issue and retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/c4b1e5c4-59b4-474f-b58c-549cef504fd7) ![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/edbedaa4-2fac-46b7-ae8d-0412bf6d53fd) |

### Analysis and Out-of-Order Effectiveness
- **In-Order Execution**: Longer execution times due to dependencies.
- **Out-of-Order Execution**: Better performance with increased parallelism.
- **Full Out-of-Order Execution**: Best outcomes with reduced execution cycles.
- **Comparison**: Out-of-order architectures exhibit enhanced performance with reduced execution cycles. The optimal outcome occurs with full out-of-order issue and retirement, highlighting the effectiveness of parallel execution. Dependencies limit the potential for parallel execution, especially when there are more issue slots available.

## Part 2

### Input 1

#### Register Renaming
| INSTRUCTIONS      | WITH REGISTER RENAMING   | CHANGES           |
|-------------------|--------------------------|-------------------|
| 1. R3 = R0 * R1   | R3 = R0 * R1             |                   |
| 2. R4 = R0 + R2   | R4 = R0 + R2             |                   |
| 3. R5 = R0 + R1   | R5 = R0 + R1             |                   |
| 4. R6 = R1 + R4   | R6 = R1 + R4             |                   |
| 5. R7 = R1 * R2   | R7 = R1 * R2             |                   |
| 6. R1 = R0 - R2   | R8 = R0 - R2             | R1 = R8           |
| 7. R3 = R3 * R1   | R3 = R3 * R8             |                   |
| 8. R1 = R4 + R4   | R1 = R4 + R4             | R1 = R1           |

#### Results
| Configuration                              | Results                          |
|--------------------------------------------|----------------------------------|
| 1 issue slot, in-order                     |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/3187285e-98fd-4a05-8852-c461bdb0e646) |
| 1 issue slot, out-of-order issue, in-order retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/a87e3df4-d377-45fb-8dfc-736cd22be98b) |
| 1 issue slot, out-of-order issue and retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/d2abcad0-f92e-4b86-9f63-2443a1519715) |
| 2 issue slots, in-order                    |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/de607913-ed60-46a4-be7e-d47ca47c5b66) |
| 2 issue slots, out-of-order issue, in-order retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/a24e14cd-ea82-4800-a95d-dd0b04098eee) |
| 2 issue slots, out-of-order issue and retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/103483da-7fad-45f3-9c49-81c628b2a67b) |
| 3 issue slots, in-order                    |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/21979717-b096-43ba-8943-718c4cc83eb7) |
| 3 issue slots, out-of-order issue, in-order retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/f19618e7-31b7-4b0d-8815-8a00eddebd90) |
| 3 issue slots, out-of-order issue and retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/60c5e7a9-6425-4c13-91ff-8f24a33e69de) |

### Input 2

## Register Renaming
| INSTRUCTIONS | WITH REGISTER RENAMING | CHANGES |
|---|---|---|
| 1-5 | No change (registers not reused) | |
| 6 | R1 = R0 - R2 (becomes) R9 = R0 - R2 <br> R1 = R9 | R1 renamed to R9 to avoid overwriting previous value |
| 7 | R3 = R3 * R1 (becomes) R3 = R3 * R9 | No change (R9 holds new value for R1) |
| 8 | R1 = R4 + R4 (becomes) R1 = R4 + R4 | R1 renamed to itself (redundant instruction) |
| 9 | R3 = R0 * R1 (becomes) R9 = R0 * R1 <br> R3 = R9 | R1 renamed to R9 to avoid overwriting previous value |
| 10-13 | Similar to 1-5 (registers not reused) | |
| 14 | R1 = R0 - R2 (becomes) R11 = R0 - R2 <br> R1 = R11 | R1 renamed to R11 to avoid overwriting previous value |
| 15 | R3 = R3 * R1 (becomes) R3 = R3 * R11 | No change (R11 holds new value for R1) |
| 16 | R1 = R4 + R4 (becomes) R1 = R10 + R10 | R1 renamed to R10 (redundant instruction) |
| 17-21 | Similar to 9-13 (registers reused with renaming) | |
| 22 | R1 = R0 - R2 (becomes) R10 = R0 + R2 <br> R1 = R10 | R1 renamed to R10 (opposite operation due to typo?) | 
| 23 | R3 = R3 * R1 (becomes) R3 = R3 * R10 | No change (R10 holds new value for R1) |
| 24 | R1 = R4 + R4 (becomes) R1 = R1 + R1 | R1 renamed to itself (redundant instruction) |
| 25 | R3 = R0 * R1 (becomes) R9 = R0 + R1 <br> R3 = R9 | R1 renamed to R9 to avoid overwriting previous value (possible typo in instruction) |
| 26-30 | Similar to 10-13 with additional Load and Store instructions | |


#### Results
| Configuration                              | Results                          |
|--------------------------------------------|----------------------------------|
| 1 issue slot, in-order                     |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/0ae887bd-935f-4088-be57-c0f032519b3f) ![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/8ad6c0a6-4673-4850-87a0-996561aa9a1a) |
| 1 issue slot, out-of-order issue, in-order retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/0af894f4-6a18-4232-bc30-4202b82f8a74) |
| 1 issue slot, out-of-order issue and retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/21427f76-81ca-4be7-8a4e-fa3ab033135d) |
| 2 issue slots, in-order                    |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/c57a4b71-fd8f-4f20-8189-7230aab92c9e) |
| 2 issue slots, out-of-order issue, in-order retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/6fb7a4c8-373f-4073-9a29-0e6a991a4108) |
| 2 issue slots, out-of-order issue and retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/f4bfcdc6-d19f-47a3-8f89-81dd22a7e09f) |
| 3 issue slots, in-order                    |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/46300e44-59d7-439a-bdfe-a97ec1895503) |
| 3 issue slots, out-of-order issue, in-order retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/267f98aa-bcd7-4470-ab76-fd7b7ba49543) |
| 3 issue slots, out-of-order issue and retirement |![image](https://github.com/Santin203/ISRR-Simulator/assets/83292351/42c3b632-6134-4cf7-ab41-ec2f755dd0c0) |

### Analysis of Results
- **Register Renaming**: Resolves WAR and WAW dependencies, leading to improved parallel execution.
- **Performance Improvement**: Observed in all configurations with significant gains in superscalar executions.
- **Comparison with Part 1**: Demonstrates the effectiveness of register renaming in reducing execution cycles.

## Conclusion

This project demonstrates the importance of instruction scheduling and register renaming in multi-issue processors. The simulations reveal the benefits of out-of-order execution and register renaming in improving processor performance. Future enhancements could include more complex instruction sets and considerations for cache and memory latencies.

## Future Work
- **Advanced Instruction Sets**: Incorporate more complex operations and conditional branches.
- **Cache and Memory Latencies**: Simulate the impact of cache misses and memory access times.
- **Dynamic Scheduling Algorithms**: Implement advanced algorithms for dynamic scheduling.

