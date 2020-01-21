# Solve Sudoku with AI

## Synopsis

In this project, students will extend the Sudoku-solving agent developed in the classroom lectures to solve _diagonal_ Sudoku puzzles. A diagonal Sudoku puzzle is identical to traditional Sudoku puzzles with the added constraint that the boxes on the two main diagonals of the board must also contain the digits 1-9 in each cell (just like the rows, columns, and 3x3 blocks).

## Instructions

Follow the instructions in the classroom lesson to install and configure the AIND [Anaconda](https://www.continuum.io/downloads) environment. That environment includes several important packages that are used for the project.

**YOU ONLY NEED TO WRITE CODE IN `solution.py`.**


## Quickstart Guide

### Activate the aind environment (OS X or Unix/Linux)

    `$ source activate aind`

### Activate the aind environment (Windows)

    `> activate aind`

### Run the code & visualization

    `(aind)$ python solution.py`

### Run the local test suite

    `(aind)$ python -m unittest -v`

### Run the remote test suite & submit the project

    `(aind)$ udacity submit`


## Coding

You must complete the required functions in the 'solution.py' file (copy in code from the classroom where indicated, and add or extend with new code as described below). The `test_solution.py` file includes a few unit tests for local testing (See the unittest module for information on getting started.), but the primary mechanism for testing your code is the Udacity Project Assistant command line utility described in the next section.

YOU SHOULD EXPECT TO MODIFY OR WRITE YOUR OWN UNIT TESTS AS PART OF COMPLETING THIS PROJECT. The Project Assistant test suite is not shared with students. Writing your own tests leads to a deeper understanding of the project.

1. Run the following command from inside the project folder in your terminal to verify that your system is properly configured for the project. You should see feedback in the terminal about failed test cases -- which makes sense because you haven't implemented any code yet. You will reuse this command later to execute your **local** test cases.

    `$ python -m unittest -v`

1. Run the following command from inside the project folder in your terminal to verify that the Udacity-PA tool is installed properly. You should see a list of failed test cases -- which is good because you haven't implemented any code yet. You will reuse this command later to execute the **remote** test cases and complete the project.

    `$ udacity submit`

1. Add the two new diagonal units to the `unitlist` at the top of solution.py. Re-run the local tests with `python -m unittest` to confirm your solution.

1. Copy your code from the classroom for the `eliminate()`, `only_choice()`, `reduce_puzzle()`, and `search()` into the corresponding functions in the `solution.py` file.

1. Implement the `naked_twins()` function, and update `reduce_puzzle()` to call it (along with the other existing strategies). Re-run the local tests with `python -m unittest -v` to confirm your solution.

1. Write your own test cases to further test your code. Re-run the remote tests with `udacity submit` to confirm your solution. If any of the remote test cases fail, use the feedback to write new local test cases that you can use for debugging.


## Submission

To submit your code, run `udacity submit` from a terminal in the top-level directory of this project. You will be prompted for a username and password the first time the script is run. If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

The Udacity-PA CLI tool is automatically installed with the AIND conda environment provided in the classroom, but you can also install it manually by running `pip install udacity-pa`. You can submit your code for scoring by running `udacity submit`. The project assistant server has a collection of unit tests that it will execute on your code, and it will provide feedback on any successes or failures. You must pass all test cases in the project assistant to pass the project.

Once your project passes all test cases on the Project Assistant, submit the zip file created by the `udacity submit` command in the classroom to automatically receive credit for the project. NOTE: You will not receive personalized feedback for this project on submissions that pass all test cases, however, all other projects in the term do provide personalized feedback on both passing & failing submissions.


## Troubleshooting

Your classroom mentor may be able to provide some guidance on the project, but the [discussion forums](https://discussions.udacity.com/c/nd889-intro-sudoku) or [slack team](https://ai-nd.slack.com) (especially the #p-sudoku channel) should be your primary support resources. The instructors hold regularly scheduled office hours in the Slack community. (The schedule is posted in the description of the #office-hours channel.)

Contact ai-support@udacity.com if you don't have access to the forums or Slack team.


## Visualization

**Note:** The `pygame` library is required to visualize your solution -- however, the `pygame` module can be troublesome to install and configure. It should be installed by default with the AIND conda environment, but it is not reliable across all operating systems or versions. Please refer to the pygame documentation [here](http://www.pygame.org/download.shtml), or discuss among your peers in the slack group or discussion forum if you need help.

Running `python solution.py` will automatically attempt to visualize your solution, but you mustuse the provided `assign_value` function (defined in `utils.py`) to track the puzzle solution progress for reconstruction during visuzalization.

## Design and Implementation

This solution includes functionality for solving diagonal Sudoku boards, in addition to constraint propagation for naked-twin patterns on the board. The following sections detail the design of these features.

### How do we apply constraint propagation to solve the naked twins problem?

The naked-twins problem is a pattern on the Sudoku board where a unit (row, column, 3x3 grid, or diagonal) contains two instances of a box with the same two digit values. For example, a row might contain the possible values `23` and two instances of this value are located within the row. In such a case, it's clear that the two boxes must contain either the value `2` or the value `3`. Therefore, we can eliminate these two values from all other boxes in the row (or unit).

The solution for detecting and eliminating a naked-twin is implemented by first traversing all boxes on the board. If the box's value has two digits, we have a potential naked twin. We search across all unit types (row, column, 3x3 grid, diagonal) and check if the value exists within the unit and it is found exactly two times. If these conditions are true, we have a naked twin. We then iterate across all other boxes in the unit (skipping the two that comprise the naked-twin) and remove the naked-twin's digits from the other box values in the unit.

The following steps detail the algorithm.

1. Iterate over all boxes on the board.
2. If a box's value has exactly two digits, continue to step 3. Otherwise, go back to step 1.
3. Iterate over all boxes in each unit type (row, column, 3x3 grid, diagonal).
4. Count the number of occurrences of the value from step 2 in all other boxes within the unit.
5. After checking all boxes, if the count is exactly `2`, then continue to step 6. Otherwise, go back to step 1.
6. For all boxes in the unit type that have a different value than the one in step 2, remove step 2 box's digits from each box, thus eliminating those values from all other boxes in the unit.
7. Repeat the process on the next target box by going back to step 1.

### How do we apply constraint propagation to solve the diagonal sudoku problem?

To solve the diagonal problem in Sudoku, we must first make a list of all keys belonging to both the left and right diagonals. We can do this by starting from the first top-left box `A1` and the last top-right box `A9` and work our way downwards at a diagonal. To collect the key names that belong to each diagonal, we increment the row and increment/decrement the column, for the left and right diagonals respectively.

Once we have a list of the diagonal keys, we update the methods for `eliminate`, `only_choice`, and `naked_twins`. Originally, these methods contained constraint propogation for detecting row, column, and 3x3 grids. We now add additional constraint propogation for the left and right diagonals.

The constraint propogation for diagonals iterates over each key in the respective diagonal list and applies the designated logic for elimination, only-choice, and naked-twins as previously exists. For example, for the case of `eliminate`, as we iterate over each key in the respective diagonal, we check if a box already has a single value assigned, and if so, remove that value from all other boxes in the diagonal unit. We apply this process to both the left and right diagonals, removing single detected values from the peers.

An example of building the list of diagonal keys is shown below.

```python
diagonal_units = []

col_index = 0
left_diagonal = []
right_diagonal = []

# Build the list of the diagonal units, starting from the top-left and top-right and working diagonal downwards.
for index in range(0, len(rows)):
    left_diagonal.append(row_units[index][col_index])
    right_diagonal.append(row_units[index][len(row_units[index]) - col_index - 1])

    col_index = col_index + 1

# Build the list of diagonal keys as a list of [left_keys, right_keys].
diagonal_units.append(left_diagonal)
diagonal_units.append(right_diagonal)
diagonal_keys = [item for sublist in diagonal_units for item in sublist]
```
