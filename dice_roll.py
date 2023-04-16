# For all code linked to dice rolling and calculation

import re
import random
import operations as op
import utility

DICE_REGEXP = r"(\d+)d(\d+)"    #TODO Add (NOT .) OR start condition
SPLIT_REGEXP = r"(\d+(?:\.\d+)?)"

def rollAndCalculate(expr:str) -> tuple:
    """Execute expression, first resolving all dice rolls, then calculating a result

    Args:
        expr (str): The expression to evaluate

    Returns:
        tuple: (The expression with dice replaced by their rolls, the result of the evaluation)
    """
    expr = rollDice(expr)
    val = calculate(expr)
    return (expr, val)

def rollDice(expr: str) -> str: 
    """Replaces all NdN parts of expr with a sum of dice roll values

    Args:
        expr (str): The expression to evaluate

    Returns:
        str: the expression with dice rolls subbed out for their results
    """
    return re.sub(DICE_REGEXP, lambda x: roll(x.group(1), x.group(2)), expr)

def roll(numberOfDice: int, limit:int) -> str:
    """Performs a dice roll and returns all roll values seperated by + and between parentheses

    Args:
        numberOfDice (int): Number of dice to throw
        limit (int): Value of said dice

    Returns:
        str: Rolls in the following format (v1 + v2 + ... + vn)
    """
    return '(' + ' + '.join(str(random.randint(1, limit)) for r in range(numberOfDice)) + ')'

def calculate(expr:str) -> float:
    """Takes a mathematical expression and calculates it. Recognises **, *, /, +, and - operations as well as parentheses

    Args:
        expr (str): The expression to evaluate

    Returns:
        float: The result of the calculation
    """
    
    # First evaluate sub-expressions
    
    subExpressions = getSubexpressionIndices(expr)
    for subStart, subEnd in subExpressions:
        expr[subStart:subEnd] = str(calculate(expr[subStart:subEnd]))
        
    # Split string into tokens and numbers. Convert the former to Operations and the latter to floats
    
    # Reverse the list so that we can go through the reversed list backwards.
    # We want to deal with operations from left to right in expr, but while avoiding changing the next indices 
    splitExpr = re.split(SPLIT_REGEXP)
    priorityToOp = {}
    previousOp = None
    for i in range(len(splitExpr)):
        t = toOperationOrFloat(splitExpr[i])
        splitExpr[i] = t
        if i % 2:           # t is op - we are assuming here that there is a number - op - number - ... alternation
            previousOp = t
            t.setLeftNumber(splitExpr[i-1])
            utility.addToDicList(priorityToOp, t.priority, t)
        elif previousOp:    # t is a number and not the first one
            previousOp.setRightNumber(t)
            
    
    # Execute the operations
    
    currentNumber = None
    for priority in range(op.HIGHEST_PRIORITY,op.LOWEST_PRIORITY):
        opList = priorityToOp[priority]
        for op in opList:            
            currentNumber = op.apply()
    
    # currentNumber is the last item left and also the result
    
    return currentNumber               
    
def getSubexpressionIndices(expr:str) -> list:
    """Finds the positions of any parts of the expression which are between brackets.
    Ignores nested parentheses, so that 5 + (2 * (3-6)) would only be considered to have 1 sub expression

    Args:
        expr (str): The expression which contains parentheses

    Raises:
        ValueError: If not all opening parentheses match a closing one and vice-versa

    Returns:
        list: containing the indices which enclose the parentheses of the subexpressions found
    """
    if '(' not in expr:
        return None
    openPs = 0
    subExpressions = []
    subStart = -1
    for i in range(len(expr)):
        c = expr[i]
        if c == '(':
            if openPs == 0:
                subStart = i
            openPs+=1
        elif c == ')':  
            openPs -= 1
            if openPs < 0:
                raise ValueError("')' found with no preceding '('") 
            elif openPs == 0:
                # i+1 to include ) in subexpression
                subExpressions.append((subStart, i+1))   
    
    if openPs != 0:
        raise ValueError("'(' not closed")
    
    return subExpressions       
            

def toOperationOrFloat(token:str) -> any:
    """Takes the input token and outputs the corresponding operation, 
    or converts the token to a float if none is found

    Args:
        token (str): Should be **,*,/,+,- or a number

    Returns:
        any: An op.Operation or a float
    """
    match token:
        #case 'd':
        #    return Roll()
        case '**':
            return op.Power()
        case '*':
            return op.Multiply()
        case '/':
            return op.Divide()
        case '+':
            return op.Add()
        case '-':
            return op.Substract()
        case _:
            return float(token)
        
