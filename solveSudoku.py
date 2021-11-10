#Student name: Anshul Jain
#ID: 253756668
#UPI: ajai165

import copy

class evalue:
    def __init__(self):
        self.steps = 0
        self.solved = 0
sc = evalue()
"""
A sudoku is a 9x9 matrix where each item has domain {1,2,3,4,5,6,7,8,9}. 
A sudoku problem contains a incomplete grid where some squares are missing. The missing squares are denoted by 0.
                                8 0 0 0 2 0 0 0 0 
                                0 1 0 6 5 0 8 0 3 
                                0 0 5 0 0 0 2 0 0 
                                0 0 0 2 0 0 6 0 4 
                                0 0 3 0 0 0 0 0 0 
                                2 0 7 0 0 0 5 3 0 
                                5 0 1 4 0 0 0 0 0 
                                0 0 0 0 6 2 0 1 0 
                                0 0 0 0 1 0 4 0 0 

The target is to assign a value to each missing square, such that the following rules will not be violated:
    1. any row contains all values from {1,2,3,4,5,6,7,8,9}
    2. any column contains all values from {1,2,3,4,5,6,7,8,9}
    3. The grid can be divided into 9 3x3 blocks. Each block contains all values from {1,2,3,4,5,6,7,8,9}
    an example of sudoku: 
                                8 6 4 7 2 3 1 9 5 
                                9 1 2 6 5 4 8 7 3 
                                3 7 5 8 9 1 2 4 6 
                                1 5 9 2 3 7 6 8 4 
                                6 8 3 9 4 5 7 2 1 
                                2 4 7 1 8 6 5 3 9 
                                5 2 1 4 7 9 3 6 8 
                                4 3 8 5 6 2 9 1 7 
                                7 9 6 3 1 8 4 5 2 

"""


class point:
    """
        A "point" is a square in the sudoku grid. 
        x,y denotes the horizontal-vertical position of the square.
        "available" is a list of all candidate values for this position.
        "value" is the current value for the position. The dafault is 0.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.available = []
        self.value = 0


def rowNum(p, sudoku):
    """
    Return  current values in p's row.
    """
    row = set(sudoku[p.y * 9:(p.y + 1) * 9])
    row.remove(0)
    return row  # set type


def colNum(p, sudoku):
    """
    Return current values in p's column
    """
    col = []
    length = len(sudoku)
    for i in range(p.x, length, 9):
        col.append(sudoku[i])
    col = set(col)
    col.remove(0)
    return col  # set type


def blockNum(p, sudoku):
    """
    Return current values in p's block
    """
    block_x = p.x // 3
    block_y = p.y // 3
    block = []
    start = block_y * 3 * 9 + block_x * 3
    for i in range(start, start + 3):
        block.append(sudoku[i])
    for i in range(start + 9, start + 9 + 3):
        block.append(sudoku[i])
    for i in range(start + 9 + 9, start + 9 + 9 + 3):
        block.append(sudoku[i])
    block = set(block)
    block.remove(0)
    return block  # set type


def initPoint(sudoku):
    """
    Initialise the sudoku grid using the input, and return the candidate positions 
    """
    pointList = []
    length = len(sudoku)
    for i in range(length):
        if sudoku[i] == 0:
            p = point(i % 9, i // 9)
            for j in range(1, 10):
                if j not in rowNum(p, sudoku) and j not in colNum(p, sudoku) and j not in blockNum(p, sudoku):
                    p.available.append(j)
            pointList.append(p)
    return pointList
    

def ForwardCheck(pointList, sudoku):
    """
    Task 1: 
    Implement the forward checking algorithm that performs arc consistency checks
    :param pointList: a list which stores all currently unassigned variables. Each item here is a "point" entry.
    :param sudoku: current assignments. Each element denotes an assignment to the corresponding square.
    :return: an updated pointList that is the result of the arc consistency algorithm for sudoku
    """
    updatedList = []

    for p in pointList:
        if sudoku[p.y * 9 + p.x]  == 0:
            newpoint = point(p.x, p.y)
            newpoint.available = []
            for i in range(1, 10):
                if i not in rowNum(newpoint, sudoku) and i not in colNum(newpoint, sudoku) and i not in blockNum(newpoint, sudoku):
                    newpoint.available.append(i)
            updatedList.append(newpoint)

    return updatedList


def BacktrackCSP_frameWork(pointList, sudoku, select=None):
    """
    Task 2: Complete this method in the indicated code segments. 
    
    :param pointList: a list which stores all variables currently unassigned. Each item here is a "point" entry.
    :param sudoku: current assignments. Each element denotes an assignment to the corresponding square.
     Note: 0 denotes that this position has not been assigned.
    :return: True (if at least a solution can be find) or False(if no solution exists)
    """


    if len(pointList) <= 0:
        return True

    #1. Select the next unassigned variable
    if select == "default": #default function, just use it to support your understanding.
        pselected = select_unassigned_var(pointList, sudoku)
    elif select == "MRV":
        pselected = select_unassigned_var_MRV(pointList, sudoku)
    elif select == "New":
        pselected = select_unassigned_var_New(pointList, sudoku)
    else:
        print("select method undefined!")
        return False

    print("The point selected", vars(pselected))

    #2. Select first element from the domain of the selected point
    selected_value = pselected.available[0]
    print("Value selected", selected_value)

    
    #3. Make a copy of sudoku and update it with the selected value
    working_sudoku=copy.deepcopy(sudoku)
    x = pselected.x
    y = pselected.y

    print("Previous sudoku")
    showSudoku(working_sudoku)

    print("New sudoku")
    working_sudoku[y * 9 + x] = selected_value
    showSudoku(working_sudoku)


    #4. Re-calculate the pointlist using ForwardCheck, given the new working_sudoku has 1 updated value
    updatedPointList = ForwardCheck(pointList, working_sudoku)


    #Check there is no conflict
    conflict = False
    for p in updatedPointList:
        if len(p.available) == 0:
            conflict = True
            print("There is a conflict at", vars(p))

    if conflict == False:
        flag = False
        pointList = updatedPointList
        sudoku = working_sudoku
        BacktrackCSP_frameWork(pointList, sudoku, "MRV")

    else:
        #Remove the selected value from available list of pselected
        print("Conflict is",conflict)
        pselected.available.pop(0)

        if len(pselected.available) == 0:
            return False

            BacktrackCSP_frameWork(pointList, sudoku, "MRV")

        while len(pselected.available) > 0:

            selected_value = pselected.available.pop(0)
            print("Trying next value from Domain", selected_value)

            x = pselected.x
            y = pselected.y

            print("New sudoku")
            working_sudoku[y * 9 + x] = selected_value

            if not BacktrackCSP_frameWork(updatedPointList, working_sudoku, "MRV"):
                print("Let's try another value:")

            else:

                flag = True
                print("Seems like we found a valid solution") 

                break   

        if not flag:

            print("Gonna have to backtracka step")
            BacktrackCSP_frameWork(PointList, working_sudoku)



    return flag


def testSudoku(sudoku):
    """
    Task 3: Complete this method
    :param sudoku: current assignments. Each element denotes an assignment to the corresponding square.
    :return: True (if sudoku is a valid solution), False (otherwise)
    
    Note: If the input is not a valid solution, print out the row, column, or block where a conflict occurs
    """


    length = len(sudoku)
    for i in range(length):
        p = point(i % 9, i // 9)
        p.value = sudoku[i]

        if p.value == 0:
            print("Assignment is not complete. Value is 0 at ",p.x,p.y)
            return False
        elif p.value in rowNum(p, sudoku):
            print("Conflict in row",p.y)
            return False
        elif p.value in colNum(p, sudoku):
            print("Conflict in column",p.x)
            return False
        elif p.value in blockNum(p, sudoku):
            #TODO: What the hell is a block number?
            block_x = p.x // 3
            block_y = p.y // 3
            print("Conflict in block, block_x",block_x," ,block_y",block_y)
            return False

    return True

def select_unassigned_var(pointList, sudoku):
    """
    Given a partial assignment for the sudoku puzzle, choose the next unassigned variable, 
    return it and update the "pointList".
    Note: this is the default function for selecting the next unassigned variable.
    """

    return pointList.pop()


def select_unassigned_var_MRV(pointList, sudoku):
    """
    Task 4: 
    Given partial assignment sudoku, choose the next unassigned variable, 
    return it and update "pointList".
    For this task, you need to implement the MRV heuristic for selecting the next unassigned variable.
    :param pointList: a list which stores all variables currently unassigned. Each item here is a "point" entry.
    :param sudoku: current assignments. Each element denotes an assignment to the corresponding square.
    """

    min_available_values = 999
    pselected = None
    for point in pointList:
        available_values = len(point.available)

        if available_values == 0:
            print('Sudoku Unsolvable')
            return False

        if available_values < min_available_values:
            pselected = point
            min_available_values = available_values
            # print(point.value)
            # print(point.available)

    return pselected


def select_unassigned_var_New(pointList, sudoku):
    """
    Task 5:
    Given a partial assignment, choose the next unassigned variable, 
    return it and update "pointList".
    For this task you need to implement a different heuristic for selecting the next unassigned variable.     
    """

    return None



def checkRuleOut(sudoku, pointList):
    """
    Return the amount of ruled-out values
    :param sudoku:  The modified sudoku where exact a 0-position's value is filled.
    :param pointList: pointList before modification
    :return: Return the amount of ruled-out values
    """
    length = len(sudoku)
    count = 0
    for i in range(length):
        if sudoku[i] == 0:
            p = point(i % 9, i // 9)
            for j in range(1, 10):
                if j not in rowNum(p, sudoku) and j not in colNum(p, sudoku) and j not in blockNum(p, sudoku):
                    count += 1
    oldCount = 0
    for k in pointList:
        oldCount += len(k.available)

    return oldCount - count






def check(p, sudoku):
    """Check if position p's trial value violate rules, return True if not violated"""
    if p.value == 0:
        print('not assign value to point p!!')
        return False
    if p.value not in rowNum(p, sudoku) and p.value not in colNum(p, sudoku) and p.value not in blockNum(p, sudoku):
        return True
    else:
        return False


def showSudoku(sudoku):
    """Print the sudoku"""
    for j in range(9):
        for i in range(9):
            print('%d ' % (sudoku[j * 9 + i]), end='')
        print('')
    print("\n")



if __name__ == '__main__':
    
    sudoku = [
        8, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 9, 8, 0, 5, 0, 3,
        0, 1, 0, 0, 0, 0, 8, 0, 2,
        4, 0, 0, 1, 0, 0, 6, 7, 0,
        0, 3, 0, 6, 0, 0, 0, 2, 0,
        0, 0, 9, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 4, 5, 0, 0, 0,
        7, 2, 0, 0, 0, 1, 0, 6, 0,
        0, 0, 0, 0, 0, 0, 2, 0, 0,
    ]

    pointList = initPoint(sudoku)

    for p in pointList:
        BacktrackCSP_frameWork(pointList, sudoku, select='MRV')







