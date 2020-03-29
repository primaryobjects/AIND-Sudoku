
from utils import *
from math import floor

import os
os.environ['OPENBLAS_NUM_THREADS'] = '1' # https://stackoverflow.com/a/57549064
import numpy as np

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = []
skip_diagonal = False

# Create the diagonal units, starting from the top-left and top-right and working diagonal downwards.
col_index = 0
left_diagonal = []
right_diagonal = []
for index in range(0, len(rows)):
    left_diagonal.append(row_units[index][col_index])
    right_diagonal.append(row_units[index][len(row_units[index]) - col_index - 1])
    col_index = col_index + 1
diagonal_units.append(left_diagonal)
diagonal_units.append(right_diagonal)
diagonal_keys = [item for sublist in diagonal_units for item in sublist]

unitlist = row_units + column_units + square_units + diagonal_units

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)

def get_box_coordinates(row, col):
    """Calculate a 3x3 box origin location at the top-left."""
    boxX = floor(cols.index(col) / 3) * 3
    boxY = floor(rows.index(row) / 3) * 3

    return boxX, boxY

def set_values_by_hash_count(values, key, hash, count=1):
    """Find any hash counts with a score of 1 and set their value in the cell key."""
    for hashKey in hash.keys():
        if hash[hashKey]['count'] == count:
            setKey = hash[hashKey]['key']
            values[key] = hashKey

    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # Go through all cells in the grid.
    for row in range(0, len(rows)):
        for col in range(0, len(cols)):
            key = rows[row] + cols[col]
            value = values[key]

            # If this value has multiple digits, check for a naked twin.
            if len(value) == 2:
                # Check against all other cells in the row.
                count = 1
                inUnit = False # True if the current value is contained in this unit and a valid naked twin check.
                # Look for a match of this value in the remainder of the row.
                for colIndex in range(0, len(cols)):
                    indexKey = rows[row] + cols[colIndex]
                    if indexKey != key and values[indexKey] == value:
                        count = count + 1
                    elif indexKey == key:
                        inUnit = True
                if count == 2 and inUnit:
                    # We have a naked twin (two occurrences of the value exist in this unit).
                    # Go through all other cells in the unit and remove the digits contained in this value.
                    for colIndex in range(0, len(cols)):
                        indexKey = rows[row] + cols[colIndex]
                        if values[indexKey] != value:
                            # Remove the digits contained in this value from the current box's value.
                            for digit in [char for char in value]:
                                values[indexKey] = values[indexKey].replace(digit, '')

                # Check against all other cells in the column.
                count = 1
                inUnit = False # True if the current value is contained in this unit and a valid naked twin check.
                # Look for a match of this value in the remainder of the unit.
                for rowIndex in range(0, len(rows)):
                    indexKey = rows[rowIndex] + cols[col]
                    if indexKey != key and values[indexKey] == value:
                        count = count + 1
                    elif indexKey == key:
                        inUnit = True
                if count == 2 and inUnit:
                    # We have a naked twin (two occurrences of the value exist in this unit).
                    # Go through all other cells in the unit and remove the digits contained in this value.
                    for rowIndex in range(0, len(rows)):
                        indexKey = rows[rowIndex] + cols[col]
                        if values[indexKey] != value:
                            # Remove the digits contained in this value from the current box's value.
                            for digit in [char for char in value]:
                                values[indexKey] = values[indexKey].replace(digit, '')

                # Check against all other cells in the box.
                count = 1
                inUnit = False
                boxX, boxY = get_box_coordinates(key[0], key[1])

                # Look for a match of this value in the remainder of the unit.
                for y in range(boxY, boxY + 3):
                    for x in range(boxX, boxX + 3):
                        indexKey = rows[y] + cols[x]
                        if indexKey != key and values[indexKey] == value:
                            count = count + 1
                        elif indexKey == key:
                            inUnit = True
                if count == 2 and inUnit:
                    # We have a naked twin (two occurrences of the value exist in this unit).
                    # Go through all other cells in the unit and remove the digits contained in this value.
                    for y in range(boxY, boxY + 3):
                        for x in range(boxX, boxX + 3):
                            indexKey = rows[y] + cols[x]
                            if values[indexKey] != value:
                                # Remove the digits contained in this value from the current box's value.
                                for digit in [char for char in value]:
                                    values[indexKey] = values[indexKey].replace(digit, '')

                if not skip_diagonal:
                    # Check against all other cells in the diagonal.
                    count = 1
                    inUnit = False
                    # Look for a match of this value in the remainder of the unit.
                    for indexKey in diagonal_units[0]:
                        if indexKey != key and values[indexKey] == value:
                            count = count + 1
                        elif indexKey == key:
                            inUnit = True
                    if count == 2 and inUnit:
                        # We have a naked twin (two occurrences of the value exist in this unit).
                        # Go through all other cells in the unit and remove the digits contained in this value.
                        for indexKey in diagonal_units[0]:
                            if values[indexKey] != value:
                                # Remove the digits contained in this value from the current box's value.
                                for digit in [char for char in value]:
                                    values[indexKey] = values[indexKey].replace(digit, '')

                    # Check against all other cells in the diagonal.
                    count = 1
                    inUnit = False
                    # Look for a match of this value in the remainder of the unit.
                    for indexKey in diagonal_units[1]:
                        if indexKey != key and values[indexKey] == value:
                            count = count + 1
                        elif indexKey == key:
                            inUnit = True
                    if count == 2 and inUnit:
                        # We have a naked twin (two occurrences of the value exist in this unit).
                        # Go through all other cells in the unit and remove the digits contained in this value.
                        for indexKey in diagonal_units[1]:
                            if values[indexKey] != value:
                                # Remove the digits contained in this value from the current box's value.
                                for digit in [char for char in value]:
                                    values[indexKey] = values[indexKey].replace(digit, '')

    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """

     # Get a list of all cells with a single value in them.
    readKeys = {}
    for row in range(0, len(rows)):
        for col in range(0, len(cols)):
            key = rows[row] + cols[col]
            value = values[key]

            if len(value) == 1:
                readKeys[key] = value

    # Now go through the list of target keys and remove their value from all peers.
    for key in readKeys.keys():
        row = key[0]
        col = key[1]
        value = readKeys[key]

        # Remove this value from all cells in the row.
        for colIndex in range(0, len(cols)):
            indexKey = row + cols[colIndex]
            if not indexKey in readKeys.keys():
                values[indexKey] = values[indexKey].replace(value, '')

        # Remove this value from all cells in the column.
        for rowIndex in range(0, len(rows)):
            indexKey = rows[rowIndex] + col
            if not indexKey in readKeys.keys():
                values[indexKey] = values[indexKey].replace(value, '')

        if not skip_diagonal:
            # Remove this value from all cells in the diagonal.
            if key in diagonal_units[0]:
                # A single-digit key is in a diagonal, remove it from all other diagonal values.
                for indexKey in diagonal_units[0]:
                    if not indexKey in readKeys.keys():
                        values[indexKey] = values[indexKey].replace(value, '')

            # Remove this value from all cells in the diagonal.
            if key in diagonal_units[1]:
                # A single-digit key is in a diagonal, remove it from all other diagonal values.
                for indexKey in diagonal_units[1]:
                    if not indexKey in readKeys.keys():
                        values[indexKey] = values[indexKey].replace(value, '')

        # Remove this value from all cells in the 3x3 box.
        boxX, boxY = get_box_coordinates(row, col)

        for y in range(boxY, boxY + 3):
            for x in range(boxX, boxX + 3):
                indexKey = rows[y] + cols[x]
                if not indexKey in readKeys.keys():
                    values[indexKey] = values[indexKey].replace(value, '')

    return values

def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """

    # Go through all cells in the grid.
    for row in range(0, len(rows)):
        for col in range(0, len(cols)):
            key = rows[row] + cols[col]
            value = values[key]

            # If this value has multiple digits, check for an only-choice.
            if len(value) > 1:
                # Check against all other cells in the row.
                hash1 = {}
                # Go through each digit in the cell.
                for value1 in [char for char in value]:
                    # Check this digit against each value in the row.
                    for colIndex in range(0, len(cols)):
                        indexKey = rows[row] + cols[colIndex]
                        if values[indexKey].find(value1) != -1:
                            hashKey = str(value1)
                            hash1[hashKey] = { 'key': key, 'count': (hash1[hashKey]['count'] + 1 if hashKey in hash1 else 1) }

                # Check against all other cells in the column.
                hash2 = {}
                # Go through each digit in the cell.
                for value1 in [char for char in value]:
                    # Check this digit against each value in the column.
                    for rowIndex in range(0, len(rows)):
                        indexKey = rows[rowIndex] + cols[col]
                        if values[indexKey].find(value1) != -1:
                            hashKey = str(value1)
                            hash2[hashKey] = { 'key': key, 'count': (hash2[hashKey]['count'] + 1 if hashKey in hash2 else 1) }

                # Check against all other cells in the box.
                hash3 = {}
                # Remove this value from all cells in the 3x3 box.
                boxX, boxY = get_box_coordinates(key[0], key[1])

                # Go through each digit in the cell.
                for value1 in [char for char in value]:
                    # Check this digit against each value in the box.
                    for y in range(boxY, boxY + 3):
                        for x in range(boxX, boxX + 3):
                            indexKey = rows[y] + cols[x]
                            if values[indexKey].find(value1) != -1:
                                hashKey = str(value1)
                                hash3[hashKey] = { 'key': key, 'count': (hash3[hashKey]['count'] + 1 if hashKey in hash3 else 1) }

                # Check against all other cells in the diagonal.
                hash4 = {}
                if key in diagonal_units[0]:
                    # Go through each digit in the cell.
                    for value1 in [char for char in value]:
                        # Check this digit against each value in the diagonal.
                        for indexKey in diagonal_units[0]:
                            if values[indexKey].find(value1) != -1:
                                hashKey = str(value1)
                                hash4[hashKey] = { 'key': key, 'count': (hash4[hashKey]['count'] + 1 if hashKey in hash4 else 1) }

                # Check against all other cells in the diagonal.
                hash5 = {}
                if key in diagonal_units[1]:
                    # Go through each digit in the cell.
                    for value1 in [char for char in value]:
                        # Check this digit against each value in the diagonal.
                        for indexKey in diagonal_units[1]:
                            if values[indexKey].find(value1) != -1:
                                hashKey = str(value1)
                                hash5[hashKey] = { 'key': key, 'count': (hash5[hashKey]['count'] + 1 if hashKey in hash5 else 1) }

                # Find any hash counts with a score of 1 and set their value in the cell key.
                values = set_values_by_hash_count(values, key, hash1)
                values = set_values_by_hash_count(values, key, hash2)
                values = set_values_by_hash_count(values, key, hash3)
                if not skip_diagonal:
                    values = set_values_by_hash_count(values, key, hash4)
                    values = set_values_by_hash_count(values, key, hash5)

    return values

def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable
    """
    stalled = False
    count = 1

    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Your code here: Use the Naked Twins Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Stop looping if the puzzle is solved.
        if solved_values_after == len(values):
            stalled = True

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

        count = count + 1

    return values

def string2array(line):
    """Converts a sudoku solution in the form 123456789123456789... into 123456789\n123456789\n... a newline separated string every 9 digits.
    """
    result = ''
    parts = [line[i:i+9] for i in range(0, len(line), 9)]
    for part in parts:
        result += part + '\n'

    return result

def validate(sudoku):
    """Return True if grid is a valid Sudoku square, otherwise False, "Error".
    Input: {'A1': '2', 'A2': '6', 'A3': '7' ...}
    """
    # Convert a sudoku result into string.
    v = values2grid(sudoku)
    # Convert the grid of values to an array of strings.
    v = string2array(v)
    # Convert the array of strings to a grid of integers.
    grid = np.array([[int(i) for i in line] for line in v.split()])

    def find_duplicates(arr):
        """Returns an array of duplicate values found within the input array."""
        uniques, count = np.unique(arr, return_counts=True)
        return uniques[count > 1]

    for i in range(9):
        error = None
        # j, k index top left hand corner of each 3x3 tile
        j, k = (i // 3) * 3, (i % 3) * 3
        if len(set(grid[i,:])) != 9:
            error = 'Duplicate digit ' + str(find_duplicates(grid[i,:])) + ' found in row ' + str(i)
        elif len(set(grid[:,i])) != 9:
            error = 'Duplicate digit ' + str(find_duplicates(grid[:,i])) + ' found in column ' + str(i)
        elif len(set(grid[j:j+3, k:k+3].ravel())) != 9:
            error = 'Duplicate digit ' + str(find_duplicates(grid[j:j+3, k:k+3])) + ' found in box at position y=' + str(j) + ', x=' + str(k) + '\n' + str(grid[j:j+3, k:k+3])

        if error:
            return False, error

    if not skip_diagonal:
        # Validate diagonals.
        sum_1 = 0
        sum_2 = 0
        for i in range(9):
            diag_1_value = grid[i, i]
            diag_2_value = grid[8-i, 8-i]
            sum_1 += diag_1_value
            sum_2 += diag_2_value

        if sum_1 != 45:
            return False, 'Invalid diagonal from top-left to bottom-right.'
        elif sum_2 != 45:
            return False, 'Invalid diagonal from top-right to bottom-left.'

    return True, None

def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    is_all_single_digits = all(len(values[value]) == 1 for value in boxes) if values else False
    is_valid = False
    if is_all_single_digits:
        is_valid, err = validate(values)

    if not values:
        # Failed to find a solution.
        return False
    elif is_all_single_digits and is_valid:
        # Solved.
        return values
    else:
        # Choose one of the unfilled squares with the fewest possibilities
        fringe = {}

        # Collect all values with multiple values. These will be candidates for branching.
        for row in range(0, len(rows)):
            for col in range(0, len(cols)):
                key = rows[row] + cols[col]
                value = values[key]

                if len(value) > 1:
                    fringe[key] = value

        # Sort the choices by length.
        fringe_sorted = sorted(fringe.items(), key=lambda x: len(x[1]))

        # Select the next child to solve.
        if len(fringe_sorted) > 0:
            child = fringe_sorted.pop(0)
            key = child[0]
            value = child[1]

            # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
            # Add a child board for each potential value.
            for digit in [char for char in value] :
                # Replace the multi-values with the selected value to try.
                new_values = values.copy()
                new_values[key] = digit

                result = search(new_values)
                if result:
                    # Solved.
                    return result

    return False

def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values

if __name__ == "__main__":
    diag_sudoku_grid = '..7..5..2.......13.........9...8.7......7...5..2.......1..3.......54.......7....4'

    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    is_valid, err = validate(result)
    if not is_valid:
        print(err)
    else:
        print('Valid solution.')

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
