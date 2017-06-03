assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers



    twins_boxes=[]
    # get all boxes with 2 optional values 
    two_value_boxes = {box:values[box] for box in values.keys() if len(values[box]) == 2}
    #get twins : there are 2  boxes share same  2 optional values 
    for box in two_value_boxes:
        for t_box in two_value_boxes:
            if (t_box in peers[box]) and box != t_box and (two_value_boxes[box]==two_value_boxes[t_box]):
                twins_boxes.append([box,t_box])

    # print('twins',two_value_boxes,twins_boxes)      
    for box_ in twins_boxes:
        digit = values[box_[0]]
        for unit in units[box_[0]]:
            # print(unit)
            # find the unit with a pair twins inside
            if box_[1] in unit:
                
                for peer in unit:
                    
                    #iterate all other boxes in unit,remove digit of the twins
                    if values[peer] != digit:
                        value=values[peer]

                        value=value.replace(digit[0],'')
                        value=value.replace(digit[1],'')
                        
                        values=assign_value(values, peer, value)

    return values


    

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    p={'.':'123456789'}
    grid_word= {i:p.get(j,j)  for i,j in  zip(boxes,grid)}
    return grid_word


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    # print('before_eliminate')
    # display(values)
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            #remove solved_values from other peer
            value=values[peer].replace(digit,'')
            values=assign_value(values, peer, value)
    # print('after_eliminate')
    # display(values)
    return values

def only_choice(values):
    # print('before_only_one')
    # display(values)
    # print(unitlist)
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            #get the only_choice for a digit
            if len(dplaces) == 1:
                
                
                values=assign_value(values, dplaces[0], digit)
    # print('after_only_one')
    # display(values)
    return values



def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy

        
        values = eliminate(values)
        # check_failure(values,'eliminate')
        #naked twins
        

        values=naked_twins(values)
        # check_failure(values,'naked_twins')
        # Use the Only Choice Strategy
        values = only_choice(values)
        # check_failure(values,'only_choice')
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            print('='*50,'Failed earlier')
            return False
    return values
def check_failure(values,p):
    print('finish',p)
    display(values)
    if len([box for box in values.keys() if len(values[box]) == 0]):
        raise ValueError('Failed earlier,at '+p)
        print('='*50,'Failed earlier,at ',p)
    


def search(values):
    # print('search')
    # display(values)
    values = reduce_puzzle(values)
    
    
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    print('='*50,'start search')
    for value in values[s]:
        print('search',value ,'in',s)
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    
    values=grid_values(grid)
    
    values=search(values)

    return values


rows = 'ABCDEFGHI'
cols = '123456789'
r_cols = '987654321'

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# make diag_units
diag_units=[cross(rs, cs)[0] for rs, cs in zip(rows,cols)]
diag_units=[diag_units]
r_diag_units=[cross(rs, cs)[0] for rs, cs in zip(rows,r_cols)]
r_diag_units=[r_diag_units]
unitlist = row_units + column_units + square_units+diag_units+r_diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':



    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
