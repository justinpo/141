
class Symbol:
    def __init__(self, char: str):
        self._char = char
        self._kind = None
        self.determineKind()
    
    def determineKind(self):
        if 'a' or 'b':
            self._kind = "character"
        elif 'U':
            self._kind = "union"
        elif "(":
            self._kind = "open"
        elif ")":
            self._kind = "close"
        elif "e":
            self._kind = "empty"
        else:
            self._kind = "invalid"
    
    def kind(self):
        return self._kind

    def char(self):
        return self._char

    def __str__(self):
        return self._char

class Expression:
    def __init__(self, testCase: str):
        self._string: str = testCase.replace(" ", "")
        self._symbols: [str] = []
        for char in self._string:
            self._symbols.append(Symbol(char))

# The following code is based on the URL below with slight modifications:
# https://www.geeksforgeeks.org/stack-set-2-infix-to-postfix/

class Conversion: 
    def __init__(self, expression): 
        self._expression = expression
        self._capacity = len(expression) 
        # This array is used a stack  
        self._array = [] 
        # Precedence setting 
        self._output = [] 
        self._precedence = {'*':3, 'o':2, 'U':1} 
        self.reformat()
        self.toPostfix()
      
    # check if the stack is empty 
    def isEmpty(self): 
        return True if len(self._array) == 0 else False
      
    # Return the value of the top of the stack 
    def top(self): 
        return self._array[-1] 
      
    # Pop the element from the stack 
    def pop(self): 
        if not self.isEmpty(): 
            return self._array.pop() 
        else: 
            return "$"
      
    # Push the element to the stack 
    def push(self, op): 
        self._array.append(op)  
  
    # A utility function to check is the given character 
    # is operand  
    def isOperand(self, ch): 
        return ch == 'a' or ch == 'b' or ch == 'e'
  
    # Check if the precedence of operator is strictly 
    # less than top of stack or not 
    def notGreater(self, i): 
        try: 
            a = self._precedence.get(i, 0)
            b = self._precedence.get(self.top(), 0)
            return True if a <= b else False
        except KeyError:  
            return False

    def reformat(self):
        newExpression: str = ""
        i: int = 0

        for ch in self._expression:
            if len(self._expression) > (i + 1):
                nxt = self._expression[i + 1]
                newExpression += ch
                if ch != "(" and nxt != ')' and nxt != 'U' and nxt != '*' and ch != 'U':
                    newExpression += 'o'

            i += 1
        
        self._expression = newExpression + self._expression[-1]
        self._capacity = len(self._expression)
              
    # The main function that converts given infix expression 
    # to postfix expression 
    def toPostfix(self): 
        # Iterate over the expression for conversion 
        for i in self._expression:
            # If the character is an operand,  
            # add it to output 
            if self.isOperand(i): 
                self._output.append(i) 
              
            # If the character is an '(', push it to stack 
            elif i  == '(': 
                self.push(i) 
  
            # If the scanned character is an ')', pop and  
            # output from the stack until and '(' is found 
            elif i == ')': 
                while( (not self.isEmpty()) and self.top() != '('): 
                    a = self.pop() 
                    self._output.append(a) 
                if (not self.isEmpty() and self.top() != '('): 
                    return -1
                else: 
                    self.pop() 

            # An operator is encountered 
            else: 
                while(not self.isEmpty() and self.notGreater(i)): 
                    self._output.append(self.pop()) 
                self.push(i) 

        # pop all the operator from the stack 
        while not self.isEmpty(): 
            self._output.append(self.pop())
        
    def __str__(self):
        return ("".join(self._output))

def tokenizeFile() -> [[str]]:
    with open("mpa2.in") as file:
        inputString: str = file.read()
        inputString = inputString.replace(" ", "")
        cases = inputString.split("\n")

        return cases

def main():
    tokens = tokenizeFile()
    for token in tokens:
        x = Conversion(token)
        print(x)

if __name__ == "__main__":
    main()