import itertools

# The following code for Conversion is based on the URL below with slight modifications:
# https://www.geeksforgeeks.org/stack-set-2-infix-to-postfix/
class Conversion: 
    def __init__(self, expression): 
        self._expression = expression.replace(" ", "")
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

    def output(self):
        return self._output
        
    def __str__(self):
        return ("".join(self._output))

class State:
    def __init__(self, operation, characters):
        self._kind: str = ""
        self._validCharacters = characters
        self.determineKind(operation)
        if "e" in self._validCharacters and self._kind == "concat":
            self._validCharacters[0].replace("e", "")
        elif "e" in self._validCharacters and self._kind == "union":
            self._validCharacters.remove("e")

    def determineKind(self, operation):
        if operation == 'U':
            self._kind = "union"
        elif operation == "o":
            self._kind = "concat"
        else:
            self._kind = "invalid"
        
    def validate(self, char):
        if self._kind == "invalid":
            return False

        for x in self._validCharacters:
            for y in self._validCharacters:
                temp = list(itertools.chain.from_iterable(y))
                if char == "".join(temp):
                    return True
        
        return False

    def validCharacters(self):
        return self._validCharacters

    def kind(self):
        return self._kind

class Machine:
    def __init__(self, testCase: str):
        self._expression = Conversion(testCase).output()
        self._stateQueue: [State] = []
        self.createMachine()

    def createMachine(self):
        stack: [[str]] = []
        expression: [str] = []
        for x in self._expression:
            expression.append(x)

        while len(expression) > 0:
            symbol = expression[0]
            if symbol != "U" and symbol != "o":
                stack.append([symbol])
            elif symbol == "U":
                x = stack.pop()
                y = stack.pop()
                self._stateQueue.append(State("U", [x,y]))
                stack.append([x,y])
            elif symbol == "o":
                x = stack.pop()
                y = stack.pop()
                self._stateQueue.append(State("o", [y+x]))
                stack.append([y+x])

            expression.pop(0)

    def validate(self, testCase: str):
        expression: str = ("".join(self._expression))

        if 'U' not in self._expression:
            if testCase == expression.replace("o", ""):
                return True
            else:
                return False
        else:
            queue = []
            for x in self._stateQueue:
                queue.append(x)

            # boolean in case we want to skip an iteration
            skip = False

            while len(testCase) > 0:
                if skip == True:
                    skip == False
                    continue
            
                if len(queue) == 0:
                    break
                
                currState = queue.pop(0)

                if currState.kind() == "concat":
                    validCharacter = currState.validCharacters()[0][0] + currState.validCharacters()[0][1]
                    if len(validCharacter) == 2:
                        skip == True
                        if len(testCase) == 1:
                            return False
                        elif currState.validate(testCase[0] + testCase[1]) == False:
                            return False
                    elif len(validCharacter) == 1:
                        if currState.validate(testCase[0]) == False:
                            return False

                elif currState.kind() == "union":
                    if currState.validate(testCase[0]) == False:
                        return False

                elif currState.kind() == "invalid":
                    return False

                testCase = testCase[1:]

            if len(testCase) > 0:
                return False    

            return True

                    
def tokenizeFile() -> [[str]]:
    with open("mp3.in") as file:
        inputString: str = file.read()
        inputString = inputString.replace(" ", "")
        cases = inputString.split("\n")
        return cases

def main():
    file = open("po.out", "w+")
    tokens = tokenizeFile()
    testCases = int(tokens[0])
    tokens.pop(0)
    while testCases > 0:
        expression = tokens[0]
        tokens.pop(0)
        tests = int(tokens[0])
        tokens.pop(0)

        testCase = Machine(expression)

        while tests > 0:
            string = tokens[0]
            tokens.pop(0)
            if testCase.validate(string) == True:
                file.write("yes")
            else:
                file.write("no")
            file.write("\n")
            tests -= 1

        testCases -= 1
    file.close()

if __name__ == "__main__":
    main()