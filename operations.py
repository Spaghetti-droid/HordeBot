HIGHEST_PRIORITY = 1
LOWEST_PRIORITY = 3

class Number:
    def __init__(self, value:float) -> None:
        self.value = value

class Operation:
    priority = -1
    
    def __init__(self, leftNumber=None, rightNumber=None) -> None:
        self.leftNumber = self.setLeftNumber(leftNumber)
        self.rightNumber = self.setRightNumber(rightNumber)
    
    def setRightNumber(self, number:Number) -> None:
        if not number:
            return
        self.rightNumber = number
        number.leftOp = self
        
    def setLeftNumber(self, number:Number) -> None:
        if not number:
            return
        self.leftNumber = number
        number.rightOp = self
        
    def getNewValue(self) -> float:
        raise ValueError("Generic operation can't apply")
    
    def apply(self) -> Number:
        value = self.getNewValue()
        newLeftOp = self.leftNumber.leftOp
        newRightOp = self.rightNumber.rightOp
        newNumber = Number(value)
        if newLeftOp:
            newLeftOp.setRightNumber(newNumber)
        if newRightOp:
            newRightOp.setLeftNumber(newNumber)
        return newNumber
        
    
class Power(Operation):
    priority = 1
    
    def getNewValue(self, left:float, right:float) -> float:
        return left**right
    
class Multiply(Operation):
    priority=2
    
    def getNewValue(self, left:float, right:float) -> float:
        return left*right
    
class Divide(Operation):
    priority=2
    
    def getNewValue(self, left:float, right:float) -> float:
        return left/right
    
class Add(Operation):
    priority=3
    
    def getNewValue(self, left:float, right:float) -> float:
        return left+right
        
class Substract(Operation):
    priority=3
    
    def getNewValue(self, left: float, right: float) -> float:
        return left-right